from cmd import Cmd
from os import path
from random import choice
from string import ascii_lowercase
from server import Node, UNHANDLED
from threading import Thread
from time import sleep
from xmlrpc.client import ServerProxy, Fault
import sys

HEAD_START = 0.1  # Seconds
SECRET_LENGTH = 100


def randomString(length):
    chars = []
    letters = ascii_lowercase[:26]
    while length > 0:
        length -= 1
        chars.append(choice(letters))
    return ''.join(chars)


class Client(Cmd):
    prompt = '> '

    def __init__(self, url, dirname, urlfile):
        Cmd.__init__(self)
        self.secret = randomString(SECRET_LENGTH)
        n = Node(url, dirname, self.secret)
        t = Thread(target=n._start)
        t.setDaemon(1)
        t.start()

        sleep(HEAD_START)
        self.server = ServerProxy(url)
        urlfile = path.join(dirname, urlfile)
        for line in open(urlfile):
            line = line.strip()
            self.server.hello(line)

    def do_fetch(self, arg):
        try:
            self.server.fetch(arg, self.secret)
        except Fault as f:
            if f.faultCode != UNHANDLED: raise
            print("Couldn't find the file", arg)

    def do_exit(self, arg):
        print()
        sys.exit()

    do_EOF = do_exit


def main():
    urlfile, directory, url = sys.argv[1:]
    client = Client(url, directory, urlfile)
    client.cmdloop()


if __name__ == '__main__': main()
