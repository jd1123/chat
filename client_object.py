import socket
import select
import threading
import sys
import signal
import curses

def get_user_input(prompt=":>>"):
    data = raw_input(prompt)
    return (data, data.rstrip())


def signal_handler(signal, frame):
    print "you pressed ctrl-c. Exiting"
    c.running = 0
    sys.exit(1)


class ChatClient():

    def __init__(self, port=8111):
        self.running = 1
        self.server = None
        self.messages = []
        self.host = ''
        self.port = port
        self.threads = []

    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.host = socket.gethostname()
            self.server.connect((self.host, self.port))
        except Exception as e:
            print "cannot connect!", e
            sys.exit(1)

    def check_server(self, sock):
        inputs = [sock]
        while self.running:
            inputr, outputr, error = select.select(inputs, [], [], 1)
            for s in inputr:
                msg = sock.recv(1024)
                print ">> " + msg

    def run(self):
        signal.signal(signal.SIGINT, signal_handler)
        self.open_socket()
        t = threading.Thread(
            name='check_server', target=self.check_server, args=((self.server,)))
        self.threads.append(t)
        t.start()

        while self.running:
            data = get_user_input()
            if data[1] == ':e':
                for t in self.threads:
                    t.join()
                break

            elif data[1] == 'print':
                print 'got it'

            else:
                self.messages.append(data[0])
                for m in self.messages:
                    self.server.send(m)
                    self.messages.remove(m)

        self.server.close()

def main():
    while c.running:
        print "working"
        myscreen = curses.initscr()
        myscreen.border(0)
        myscreen.addstr(12,25, "Chat Client")
        myscreen.refresh()
        inp = myscreen.getstr(1,1,25)

if __name__ == '__main__':
    port = 8111
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    c = ChatClient(port)
    c.run()
    main()
