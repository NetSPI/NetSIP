import socket
import ssl
import time
import hashlib
import uuid
import os
from datetime import datetime


def main(request_bytes, host, port, password, tls_enabled, main_window=None):
    ### Automagically fix the "Proxy-Authorization" or "Authorization" header ###
    # normalize the \n & \r\n
    # update content length
    if(password != ""):
        request = request_bytes.decode("utf-8")
        request = request.replace("\r\n", "\n").replace("\n", "\r\n")
        # Strip all trailing newlines before appending
        request = request.rstrip("\r\n")
        request += "\r\n\r\n"
        # get the Proxy-Authorization line
        request_lines = request.split("\r\n")
        final_request_lines = []
        response_field = ""
        first_line = True
        # Go through each header
        for line in request_lines:
            if(first_line):
                method = line.split(" ")[0]
                first_line = False
            #update the authorization or proxy authorization header
            elif("Proxy-Authorization: " in line or "Authorization: " in line):
                if("Proxy-Authorization: " in line):
                    auth_line = line.replace("Proxy-Authorization: ","").replace("'",'"').split(",")
                else:
                    auth_line = line.replace("Authorization: ","").replace("'",'"').split(",")
                username = ""
                realm = ""
                uri = ""
                nonce = ""
                nc = ""
                qop = ""
                cnonce = ""
                for entry in auth_line:
                    if("username=" in entry.replace(" ","")):
                        username = entry.replace(" ","").split("username=")[-1].replace('"',"")
                    elif("realm=" in entry.replace(" ","")):
                        realm = entry.replace(" ","").split("realm=")[-1].replace('"',"")
                    elif("uri=" in entry.replace(" ","")):
                        uri = entry.replace(" ","").split("uri=")[-1].replace('"',"")
                    elif("nonce=" in entry.replace(" ","") and "cnonce=" not in entry.replace(" ","")):
                        nonce = entry.replace(" ","").split("nonce=")[-1].replace('"',"")
                    elif("nc=" in entry.replace(" ","")):
                        nc = entry.replace(" ","").split("nc=")[-1].replace('"',"")
                    elif("qop=" in entry.replace(" ","")):
                        qop = entry.replace(" ","").split("qop=")[-1].replace('"',"")
                    elif("cnonce=" in entry.replace(" ","")):
                        cnonce = entry.replace(" ","").split("cnonce=")[-1].replace('"',"")
                    elif("response=" in entry.replace(" ","")):
                        response_field_old = entry.replace(" ","").split("response=")[-1].replace('"',"")
                # hash the fields for the "response" field
                response_field = proxy_auth(username, realm, password, method, uri, nonce, nc, qop, cnonce)
                # update the "response" field
                line = line.replace(response_field_old, response_field)
            
            # update content length
            elif("Content-Length: " in line):
                content_length = 0
                try:
                    content_length = len(request.split("\r\n\r\n")[1])# + 4
                except:
                    pass
                line = "Content-Length: " + str(content_length)

            final_request_lines.append(line)

        # normalize the \n & \r\n
        request_bytes_string = ""
        for i in final_request_lines:
            request_bytes_string += i + "\r\n"
        request_bytes_string = request_bytes_string.replace("\r\n", "\n").replace("\n", "\r\n")
        if not request_bytes_string.endswith("\r\n\r\n"):
            request_bytes_string += "\r\n\r\n"
        
        # update the UI
        if(main_window):
            main_window.tab1_modifier_request_content.setPlainText(request_bytes_string)

        # update the original request_bytes
        request_bytes = request_bytes_string.encode("utf-8")

    ##########################################################

    def log_to_file(label, content):
        try:
            # Rotate logs daily by using local date in filename
            local_date = datetime.now().strftime("%Y%m%d")
            log_filename = f"sip_tester_{local_date}.log"
            log_path = os.path.join(os.path.dirname(__file__), log_filename)
            # Use local ISO timestamp for each entry
            timestamp = datetime.now().isoformat()
            with open(log_path, 'a', encoding='utf-8') as lf:
                lf.write(f"==== {label} {timestamp} ====\n")
                lf.write(content)
                lf.write('\n\n')
        except Exception:
            # Don't let logging interfere with main functionality
            pass

    context = ssl.create_default_context()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    response = ""
    if(tls_enabled):
        wrapped_sock = context.wrap_socket(sock, server_hostname=host)
        wrapped_sock.settimeout(2.0)
        print("\n[*] Sending TLS request:\n" + request_bytes.decode("utf-8"))
        log_to_file('SENT TLS', request_bytes.decode("utf-8"))
        wrapped_sock.sendall(request_bytes)
        while True:
            try:
                data = wrapped_sock.recv(4096).decode("utf-8")
                if not data:
                    break
                print("\n[*] Received TLS response:\n" + data)
                # Log each received chunk (helps debugging streaming responses)
                log_to_file('RECEIVED TLS CHUNK', data)
                response += data + "\n___________________\n"
            except socket.timeout:
                break
      
        wrapped_sock.close()
    else:
        sock.settimeout(2.0)
        print("\n[*] Sending request:\n" + request_bytes.decode("utf-8"))
        log_to_file('SENT', request_bytes.decode("utf-8"))
        sock.sendall(request_bytes)
        while True:
            try:
                data = sock.recv(4096).decode("utf-8")
                if not data:
                    break
                print("\n[*] Received response:\n" + data)
                #log_to_file('RECEIVED CHUNK', data)
                response += data + "\n___________________\n"
            except socket.timeout:
                break

        sock.close()

    # Log the full aggregated response once before returning
    try:
        log_to_file('FULL RESPONSE', response)
    except Exception:
        pass
    return response


def proxy_auth(username, realm, password, method, uri, nonce, nc, qop, cnonce=uuid.uuid4().hex[:16]):
    ha1 = hashlib.md5((username + ":" + realm + ":" + password).encode()).hexdigest()
    ha2 = hashlib.md5((method + ":" + uri).encode()).hexdigest()
    response = hashlib.md5((ha1 + ":" + nonce + ":" + nc + ":" + cnonce + ":" + qop + ":" + ha2).encode()).hexdigest()
    return response

if(__name__ == '__main__'):
    request_bytes = '''
OPTIONS sip:6001@sip.siptesting234123413.com SIP/2.0
Via: SIP/2.0/TLS 127.0.0.1:12345
Max-Forwards: 70
From: <sip:6001@sip.siptesting234123413.com:5061>;tag=98765
To: <sip:sip.siptesting234123413.com>
Contact: <sip:dummy@sip.siptesting234123413.com:5061>
Call-ID: 1234567@sip.siptesting234123413.com:5061
CSeq: 132 OPTIONS
Accept: application/sdp
User-Agent: NetSIP
Proxy-Authorization: Digest username="6001", realm="sip.siptesting234123413.com", nonce="68e76091083ba367", uri="sip:6001@sip.siptesting234123413.com", response="bbae29b429c8a3a732349be7aaea3c7a", algorithm=MD5, cnonce="84899f15ae86461abf352bdc69b6ec97", opaque="30b7c2dc684bf2fa", qop=auth, nc=00000001
Content-Length: 0
'''.encode()
    host = 'sip.siptesting234123413.com'
    port = 5061
    password = "test"
    tls_enabled = True
    main(request_bytes, host, port, password, tls_enabled)
    
    proxy_auth(username='6001', realm='sip.siptesting234123413.com', password='<REDACTED>',
          method='INVITE', uri='sip:1@sip.siptesting234123413.com', nonce='68e76091083ba367',
          nc='00000001', qop='auth', cnonce='84899f15ae86461abf352bdc69b6ec97')



