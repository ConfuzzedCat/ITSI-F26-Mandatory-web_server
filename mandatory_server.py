#!/usr/bin/python3

"""
Importerer metoder fra Socket API'en:
.bind(), .listen(), .accept(), .connect(), 
.recv(), .close() .connect_ex(), .send(), .socket()
"""

import socket 

def make_http_response(payload, status=200):
    response = ""
    response = f"HTTP/1.1 {status}\r\n"
    response += "content-type: text/html\r\n"
    response += "\r\n"
    response += payload
    response += "\r\n"
    return response

def parse_request(req_payload, conn):
    payload_split = req_payload.split("\r\n")
    #print(http_method, http_resource, http_version, sep=",")
    req_list = payload_split[0].split()
    if len(req_list) > 3:
        conn.send(make_http_response("", status=400))

"""
Opretter to globale variabler for HOST og PORT, man kunne segmenterer det 
ind i en start_server funktion, men i forhold til opgavens scope giver det mening 
at oprette dem som globale variabler.
"""
#Så vidt jeg har forstået kan man "bare" sige at host'en skal være på 0.0.0.0, 
#hvis ville have at den skal tilgås af andre netværksinterfaces.
HOST = "127.0.0.1"

#Porte under nummer 1024 er privilgerede, så valget på 6767 er vilkårligt. 
PORT = 7178

"""
contextmanaer bvlabvla
"""

"""
Nu opretter vi så en socket/dør, ved at bruge socketfunktionaliteter,
socket.AF_INET betyder:
AF - "Address Family", basically hvilke addresser socketen kommer til at bruge.
INET - "Internet", betyder 'bare' at det er internet addresser, som vores HOST, socketen
kommer til at benytte sig af.
SOCK_STREAM indikerer at vi i vores socket vil benytte os af TCP. Hvis vi for eksempel
ville bruge UDP, så ville vi benytte os af socket.SOCK_DGRAM
"""
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""
Herefter benytter vi os af .bind() funktionaliteten, hvor vi
gør at socketen skal benytte sig af vores HOST og PORT variabel.
bind() funktionen expecter én tuple.
"""
server_socket.bind((HOST, PORT))

"""
Nu kan vi indikerer hvor mange forbindelser der må tilgå vores server
ved at bruge .listen() - Den kan tage et int som argument, i forhold til
hvor mange forbindelser der maximalt på tilknyttes vores server. Til
at starte med indikerer vi bare én.
"""
server_socket.listen(1)
print("Serveren lytter fra port: ", PORT)

"""
Herefter opretter vi en ny socket "connection" til at kommunikerer med klienten,
og får klientens ipadresse og port i "address" ved at bruge .accept()
"""
connection, address = server_socket.accept()

"""
Nu kan vi så finde ud af hvad der bliver requestet af klienten ved at bruge .recv()
Vi indikerer at requesten kan læse op til 1024 bytes fra socketen, hvis HTTP requesten
skulle være mere end det skal man vidst loope det igennem flere .recv() calls. 
.decode() omskriver requesten til en string.
"""
request = connection.recv(1024).decode()
#print("Klienten har sendt: ", request)

def find_html_file(path):
    if path == "/":
        path = "/index.html"
    
    if path.startswith("/"):
        path = path[1:]
    
    try:
        with open(path, "r") as file:
            lines = file.readlines()
            text_content = "".join(lines)
    except:
        return ""
    return text_content

http_method, http_resource, http_version = parse_request(request)

http_response = ""

file_content = find_html_file(http_resource)
if file_content == "":
    http_response = make_http_response("", status=404)
else:
    http_response = make_http_response(file_content)

connection.send(http_response.encode())


connection.close()
server_socket.close()

