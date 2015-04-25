import threading
import socket
import curses
import select
import signal
import sys
import random
import string

# Client object
class Client():
    def __init__(self, port=8111):
        self.userid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        self.running = 1
        self.host = ''
        self.port = port
        self.server = None
        self.incoming_messages = []
        self.outgoing_messages = []
        self.threads = []
        self.screen = None

    def add_screen(self, screen):
        self.screen = screen

    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.host = socket.gethostname()
            self.server.connect((self.host, self.port))
        except Exception as e:
            print "Cannot connect", e
            self.server.close()
            sys.exit(1)


    def send_message(self, message):
        self.outgoing_messages.append(message)
        for m in self.outgoing_messages:
            try:
                self.server.send(m)
                self.outgoing_messages.remove(m)
            except Exception as e:
                print "Could not send message: ", e

    def process_message(self, message):
        self.screen.addstr(2,1,message)
        self.screen.refresh()

    def poll_server(self):
        serv = [self.server]
        while self.running:
            inputready, outputready, errorready = select.select(serv, [], [], 1)
            for r in inputready:
                msg = self.server.recv(1024)
                self.process_message(msg)


    def run(self):
        self.open_socket()
        t = threading.Thread(name='poll_server', target = self.poll_server)
        self.threads.append(t)
        t.start()

    def clean_up(self):
        self.running = 0
        self.server.close()
        for t in self.threads:
            t.join()

# end of Client object


def sigint_handler(signal,frame):
    print 'SIGINT caught. Exiting...'
    c.clean_up()
    sys.exit(0)


def setup_curses():
    curseobj = curses.initscr()
    curseobj.border(0)
    curseobj.addstr(1, 1, "Chat Client!")
    curseobj.refresh()
    return curseobj

def main():
    signal.signal(signal.SIGINT, sigint_handler)
    threads = []
    c.run()
    screen = setup_curses()
    c.add_screen(screen)
    while c.running:
        screen.refresh()
        inp = screen.getstr(25,25,25)
        c.send_message(inp)

if __name__ == '__main__':
    port = 8111
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    c = Client(port)
    main()
    sys.exit(0)
