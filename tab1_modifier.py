import PyQt6.QtCore as QtCore
import PyQt6.QtWidgets as QtWidgets
import PyQt6.QtGui as QtGui
import NetSIP

def tab1_modifier(self):
    ### CHILDREN
    # left layout
    left_layout = QtWidgets.QVBoxLayout()
    
    self.tab_example_button = QtWidgets.QPushButton("Send Request")
    self.tab_example_button.clicked.connect(lambda: buttonRefresh(self))
    left_layout.addWidget(self.tab_example_button)

    self.tab1_modifier_request_host_port = QtWidgets.QLineEdit("sip.siptesting234123413.com:5060")
    left_layout.addWidget(QtWidgets.QLabel("<host>:<port>"))
    left_layout.addWidget(self.tab1_modifier_request_host_port)
    self.tab1_modifier_request_password = QtWidgets.QLineEdit("")
    left_layout.addWidget(QtWidgets.QLabel("If Using Proxy Authorization Header Enter Password"))
    left_layout.addWidget(self.tab1_modifier_request_password)
    self.tab1_modifier_request_enable_tls = QtWidgets.QCheckBox("Enable TLS")
    left_layout.addWidget(self.tab1_modifier_request_enable_tls)

    self.tab_example_label = QtWidgets.QLabel("Request")
    left_layout.addWidget(self.tab_example_label)

    start_request = '''OPTIONS sip:6001@sip.siptesting234123413.com SIP/2.0
Via: SIP/2.0/TLS 127.0.0.1:12345
Max-Forwards: 70
From: <sip:6001@sip.siptesting234123413.com:5061>;tag=98765
To: <sip:sip.siptesting234123413.com>
Contact: <sip:dummy@sip.siptesting234123413.com:5061>
Call-ID: 1234567@sip.siptesting234123413.com:5061
CSeq: 132 OPTIONS
Accept: application/sdp
User-Agent: NetSIP
Proxy-Authorization: Digest username="6001", realm="sip.siptesting234123413.com", nonce="68e76091083ba367", uri="sip:6001@sip.siptesting234123413.com", response="b7ae29b429c8a7a772249be7daea3c76", algorithm=MD5, cnonce="84899f15ae86461abf352bdc69b6ec97", opaque="30b7c2dc684bf2fa", qop=auth, nc=00000001
Content-Length: 0
'''

    self.tab1_modifier_request_content = QtWidgets.QTextEdit()
    self.tab1_modifier_request_content.setPlainText(start_request)
    left_layout.addWidget(self.tab1_modifier_request_content)
    left_widget = QtWidgets.QWidget()
    left_widget.setLayout(left_layout)
    left_widget.setMinimumWidth(200)
 
    # right layout
    right_layout = QtWidgets.QVBoxLayout()
    self.tab1_modifier_response_content = QtWidgets.QLabel("response")
    self.tab1_modifier_response_content.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
    self.tab1_modifier_response_content.setTextFormat(QtCore.Qt.TextFormat.RichText)  # Enable HTML
    scroll_area = QtWidgets.QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(self.tab1_modifier_response_content)
    right_layout.addWidget(scroll_area)
    right_widget = QtWidgets.QWidget()
    right_widget.setLayout(right_layout)
    right_widget.setMinimumWidth(200)

    # Create the splitters so you can make each section
    # larger or smaller in the UI
    vert_splitter = QtWidgets.QSplitter()
    vert_splitter.addWidget(left_widget)
    vert_splitter.addWidget(right_widget)
    vert_splitter.setSizes([50, 50])
    vert_splitter.setMinimumHeight(300)
    

    ### PARENT
    # the main layout for tab1
    tab2_layout = QtWidgets.QHBoxLayout()
    # Adds 5 px space around the outside
    tab2_layout.setContentsMargins(5,5,5,5)
    # Adds 5 px between each widget
    tab2_layout.setSpacing(5)
    # Add the widgets to our tab1_layout
    tab2_layout.addWidget(vert_splitter)
    tab2_widget = QtWidgets.QWidget()
    # if you don't do this then the background color of the tab is gray
    tab2_widget.setAutoFillBackground(True)
    tab2_widget.setLayout(tab2_layout)

    return tab2_widget

################ REFRESH BUTTON #######################
class buttonRefreshThread(QtCore.QThread):
    finished = QtCore.pyqtSignal()

    def run(self, main_window):
        main_window.tab1_modifier_response_content.setText("")
        try:
            request_bytes = main_window.tab1_modifier_request_content.toPlainText()
            request_bytes = request_bytes.replace("\r\n", "\n").replace("\n", "\r\n")
            if not request_bytes.endswith("\r\n\r\n"):
                request_bytes += "\r\n\r\n"
            request_bytes = request_bytes.encode("utf-8")
            host = main_window.tab1_modifier_request_host_port.text().split(":")[0]
            port = int(main_window.tab1_modifier_request_host_port.text().split(":")[1])
            password = main_window.tab1_modifier_request_password.text()
            tls_enabled = main_window.tab1_modifier_request_enable_tls.isChecked()
            # Call our code to actually send the SIP request
            response = NetSIP.main(request_bytes, host, port, password, tls_enabled, main_window)
            
            # Add style for fade effect
            style = """
                <style>
                    .highlight {
                        background-color: rgba(200, 200, 200, 0.3);
                        transition: background-color 1.5s ease;
                    }
                    .highlight.fade {
                        background-color: transparent;
                    }
                </style>
            """
            
            # Convert response to HTML with subtle highlighting
            html_response = []
            for line in response.split('\n'):
                if line == "___________________":
                    html_response.append(line)
                else:
                    # Wrap each line in a span with transition effect
                    html_response.append(f'<span class="highlight">{line}</span>')
            
            # Join with line breaks and set as HTML
            html_content = style + '<br>'.join(html_response)
            main_window.tab1_modifier_response_content.setText(html_content)
            
            # Start a timer to add fade class after a brief delay
            QtCore.QTimer.singleShot(100, lambda: main_window.tab1_modifier_response_content.setText(
                style + '<br>'.join(line.replace('class="highlight"', 'class="highlight fade"') 
                for line in html_response)))
            
            # Create and start the highlight animation
            animation = QtCore.QPropertyAnimation(main_window.tab1_modifier_response_content, b"styleSheet")
            animation.setDuration(1000)  # 1 second animation
            animation.setStartValue("background-color: #e6ffe6;")  # Light green start
            animation.setEndValue("background-color: transparent;")  # Fade to default
            animation.start()
        except Exception as e:
            print(e)
             
        self.finished.emit()

def buttonRefresh(self):
    try:
        # Start a thread so the UI isn't hanging
        self.buttonRefreshWorker = buttonRefreshThread()
        self.buttonRefreshWorker_thread = QtCore.QThread()

        self.buttonRefreshWorker.moveToThread(self.buttonRefreshWorker_thread)
        self.buttonRefreshWorker.finished.connect(lambda: buttonRefreshFinished(self))
        
        self.buttonRefreshWorker_thread.started.connect(lambda: self.buttonRefreshWorker.run(self))
        self.buttonRefreshWorker_thread.start()

    except Exception as e:
        pass

def buttonRefreshFinished(self):
    # When the Refresh button is finished close the thread properly
    self.buttonRefreshWorker_thread.quit()
    self.buttonRefreshWorker_thread.wait()

class Color(QtWidgets.QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(color))
        self.setPalette(palette)

