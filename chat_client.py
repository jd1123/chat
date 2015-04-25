import socket
import select
import threading
import sys
import curses

def check_server(sock):
    mysock = [sock]
    running = 1
    while running:
        inputr, outputr, error = select.select(mysock, [], [])
        for s in inputr:
            msg = sock.recv(1024)
            print msg

def get_user_input(prompt=":>>"):
    data = raw_input(prompt)
    return (data, data.rstrip())

def main():
    messages = []

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        s.connect((host, 8111))
        threads = []
        t = threading.Thread(target=check_server, args=(s,))
        threads.append(t)
        t.start()
    except:
        print "cannot connect!"
        sys.exit(1)

    while True:
        data = get_user_input()
        if data[1] == ':e':
            for t in threads:
                t.join()
            break
        elif dat[1]=='print':
            print 'got it'
        else:
            messages.append(data[0])
            for m in messages:
                print "message sent"
                s.send(m)
                messages.remove(m)
    s.close()

if __name__ == '__main__':
    main()
