import socket
import select
import sys

buffer_size = 4096
forward_to = ('localhost', 5555)
forward_to2 = ('localhost', 5556)

class Forward:

    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        self.forward.connect((host, port))
        return self.forward
class Forward2:

    def __init__(self):
        self.forward2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host2, port2):
        self.forward2.connect((host2, port2))
        return self.forward2



class TheServer:

    input_list = []
    channel = {}

    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(20)

    def main_loop(self):

        self.input_list.append(self.server)

        while 1:

            inputready, outputready, exceptready = select.select(self.input_list, [], [])

            for self.s in inputready:
                if self.s == self.server:
                    self.on_accept()
                    break

                self.data = self.s.recv(buffer_size)

                if len(self.data) == 0:
                    self.on_close()
                    break
                else:
                    self.on_recv()

    def on_accept(self):

        forward = Forward().start(forward_to[0], forward_to[1])     # socket conn to server
        clientsock, clientaddr = self.server.accept()               # proxy connects to client

        if forward:
            print(clientaddr, "connected")
            self.input_list.append(clientsock)
            self.input_list.append(forward)
            self.channel[clientsock] = forward
            self.channel[forward] = clientsock

        else:
            print("Can't establish connection with remote server.",)
            print("Closing connection with client side", clientaddr)
            clientsock.close()

    def on_close(self):

        self.input_list.remove(self.s)
        self.input_list.remove(self.channel[self.s])
        out = self.channel[self.s]
        self.channel[out].close()
        self.channel[self.s].close()
        del self.channel[out]
        del self.channel[self.s]

    def on_recv(self):
        data = self.data
        print(data.decode())
        self.channel[self.s].send(data)


if __name__ == '__main__':
        server = TheServer('localhost', 9090)

        try:

            server.main_loop()

        except KeyboardInterrupt:
            print("Ctrl C - Stopping server")
            sys.exit(1)
