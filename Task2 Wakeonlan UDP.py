import socket

mes = bytes.fromhex('FF')*6+bytes.fromhex('30 35 ad a6 3a 4e')*16 #MAC будимого
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#socket.socket()создает объект сокета UDP
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.sendto(mes, ('255.255.255.255',9))
s.close()
#SO_BROADCAST: разрешает отправку и прием широковещательных UDP-пакетов; подробности см. в следующем разделе.
