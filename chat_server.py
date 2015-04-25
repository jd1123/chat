import socket
import sys
import threading
import select
import signal


def signal_handler(signal, frame):
    print "SIGINT caught"
    s.close_conn()
    sys.exit(1)


class Server:
    def __init__(self, port):
        self.host = ''
        self.port = port
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []
        self.clients = []
        self.messages = []
        self.running = 0

    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setblocking(0)
            self.server.bind((self.host, self.port))
            self.server.listen(5)
        except socket.error, (value, message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)

    def broadcast_message(self):
        while self.running:
            for m in self.messages:
                print m
                self.messages.remove(m)
                for c in self.clients:
                    try:
                        c.client.send(m)
                    except:
                        self.clients.remove(c)

    def close_conn(self):
        print "closing connections"
        self.server.close()
        print "sevrer closed"
        self.running = 0
        for c in self.clients:
            c.join()

    def run(self):
        print "Chat Server with Threads"
        self.running = 1
        signal.signal(signal.SIGINT, signal_handler)
        self.open_socket()
        t = threading.Thread(target=self.broadcast_message)
        t.start()
        self.threads.append(t)

        input = [self.server, sys.stdin]
        while self.running:
            inputready, outputready, exceptready = select.select(input, [], [])

            for s in inputready:

                if s == self.server:
                    c = Client(self.server.accept(), self)
                    c.start()
                    self.clients.append(c)

                elif s == sys.stdin:
                    junk = sys.stdin.readline()
                    running = 0

        self.close_conn()


class Client(threading.Thread):

    def __init__(self, (client, address), server):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
        self.server = server

    def run(self):
        running = 1
        while running:
            data = self.client.recv(self.size)
            if data:
                print "Recieved data: " + data + " from: " + str(self.client.getpeername())
                self.client.send(data)
                self.server.messages.append(data)
            else:
                self.client.close()
                running = 0

if __name__ == '__main__':
    port = 8111
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    s = Server(port)
    s.run()
