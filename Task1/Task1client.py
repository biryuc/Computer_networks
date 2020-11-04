import socket

while True:
    msg = input()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 9090))
    sock.send(msg.encode())

    msg = sock.recv(1024) #получаем  по 1 кб
    print('message from server: ' + msg.decode())
   
