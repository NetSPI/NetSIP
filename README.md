# NetSIP

### Overview

NetSIP is a Python-powered SIP repeater that lets you craft, replay, and inspect SIP traffic. It is written in Python and includes a desktop app which leverages PyQt6. On the left side of the screen are the inputs for the request, and the right side of the screen shows the responses from the server seperated by a "___________". 

Most of the fields are intuitive except "Password". In this case password refers to your password on the SIP server you are testing. Your "username" will be in the Proxy-Authorization or Authorization header and is usually your extension. If you leave "Password" blank the request will not automagically update the Proxy-Authorization or Authorization header.

Inputs: host, port, password (Proxy-Authorization/Authorization header), Enable TLS, Request

Outputs: Response(s) from the server. Sometimes the server returns multiple responses in a row. Responses usually take ~5 seconds to show up in the UI because we need to wait to make sure we get everything from the server.

<img width="1168" height="598" alt="image" src="https://github.com/user-attachments/assets/f4dc3783-f0ab-4af2-891b-5f3d1ae4c257" />

<img width="1168" height="598" alt="image" src="https://github.com/user-attachments/assets/afd4cca3-929a-4461-b1d4-45732bd39ee3" />

<img width="1168" height="598" alt="image" src="https://github.com/user-attachments/assets/9ff0100b-ef98-4e73-838f-8e2caeab0c32" />

### Installation

Download this repo 

Install PyQt6 which is the 3rd party library used for the UI
```
python3 -m pip install PyQt6
```

### Usage

To leverage our UI
```
python3 NetSIP_ui.py
```

Or if you'd prefer not using the UI and modifying python yourself
```
python3 NetSIP.py
```

Requests and responses are logged in the console and recorded in daily logs which are automatically rotated and stored in the project directory. 

### Software Bill of Materials

* PyQt6
* hashlib
* uuid
* socket
* ssl
* time
* os
* datetime

### Code Layout

* **NetSIP_ui.py**: The parent UI script which creates the window, icon, title.
* **tab1_modifier.py**: The UI and event handling for the first tab called "SIP Modifier". This setup is so we can add more tabs in the future for additional functionality.
* **NetSIP.py**: The logic behind sending SIP requests to the server and auto magically updating some of the headers.
