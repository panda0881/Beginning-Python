from os.path import join, isfile, abspath
from xmlrpc.client import Fault
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
from urllib.parse import urlparse
import sys

MAX_HISTORY_LENGTH = 6

UNHANDLED     = 100
ACCESS_DENIED = 200

class UnhandleQuery(Fault):
    def __init__(self, message="Couldn't handle the query"):
        Fault.__init__(self, UNHANDLED, message)

class AccessDenied(Fault):
    def __init__(self, message="Acces denied"):
        Fault.__init__(self, ACCESS_DENIED, message)

def inside(dir, name):
    dir = abspath(dir)
    name = abspath(name)
    return name.startswith(join(dir, ''))

def getPort(url):
    '在URL中提取端口'
    name = urlparse(url)[1]
    parts = name.split(':')
    return int(parts[-1])

class Node:
    """
    P2P网络中的节点。
    """
    def __init__(self, url, dirname, secret):
        self.url = url
        self.dirname = dirname
        self.secret = secret
        self.known = set()

    def query(self, query, history=[]):
        """
        查询文件，可能会向其他已知节点请求帮助。讲文件作为字符串返回。
        """
        print('in function query')
        try:
            content = self._handle(query)
        except:
            history = history + [self.url]
            print('in funciton query, history : %s' % history)
            if len(history) >= MAX_HISTORY_LENGTH: raise
            content = self._broadcast(query, history)
        return content

    def hello(self, other):
        """
        用于将节点介绍给其他节点。
        """
        self.known.add(other)
        return 0

    def fetch(self, query, secret):
        """
        用于让节点找到文件并且下载。
        """
        print(query)
        print(secret)
        if secret != self.secret: raise AccessDenied
        result = self.query(query)
        print(result)
        f = open(join(self.dirname, query), 'w')
        f.write(result)
        f.close()
        return 0

    def _start(self):
        """
        内部使用，用于启动XML_RPC服务器。
        """
        s = SimpleXMLRPCServer(("", getPort(self.url)))
        s.register_instance(self)
        s.serve_forever()

    def _handle(self, query):
        """
        内部使用，用于处理请求。
        """
        dir = self.dirname
        name = join(dir, query)
        print('in function _handle, file name : %s' % name)
        if not isfile(name): raise UnhandleQuery
        if not inside(dir, name): raise AccessDenied
        return open(name).read()

    def _broadcast(self, query, history):
        for other in self.known.copy():
            print('other: %s' % other)
            if other in history: continue
            try:
                s = ServerProxy(other)
                return s.query(query, history)

            except Fault as f:
                if f.faultCode == UNHANDLED: pass
                else: self.known.remove(other)
            except:
                self.known.remove(other)
        raise UnhandleQuery

def main():
    url, directory, secret = sys.argv[1:]
    n = Node(url, directory, secret)
    n._start()

if __name__ == '__main__': main()