from nntplib import NNTP
from time import strftime, time, localtime
from email import message_from_string
import textwrap
import re
import requests

# In python3, we use requests to handle the task with network connection rather than urllib.

day = 24 * 60 * 60


def wrap(string, max=70):
    return '\n'.join(textwrap.wrap(string)) + '\n'


class NewsAgent:
    def __init__(self):
        self.sources = []
        self.destinations = []

    def addSource(self, source):
        self.sources.append(source)

    def addDestination(self, dest):
        self.destinations.append(dest)

    def distribute(self):
        items = []
        for source in self.sources:
            items.extend(source.getItems())
        for dest in self.destinations:
            dest.receiveItems(items)


class NewsItem:
    def __init__(self, title, body):
        self.title = title
        self.body = body


class NNTPSource:
    def __init__(self, servename, group, window):
        self.servername = servename
        self.group = group
        self.window = window

    def getItems(self):
        start = localtime(time() - self.window*day)
        date = strftime('%y%m%d', start)
        hour = strftime('%H%M%S', start)

        server = NNTP(self.servername)

        ids = server.newnews(self.group, date)[1]
        for id in ids:
            lines = server.article(id)[3]
            message = message_from_string('\n'.join(lines))
            title = message['subject']
            body = message.get_payload()
            if message.is_multipart():
                body = body[0]

            yield NewsItem(title, body)

        server.quit()


class SimpleWebSource:
    def __init__(self, url, titlePattern, bodyPattern):
        self.url = url
        self.titlePattern = re.compile(titlePattern)
        self.bodyPattern = re.compile(bodyPattern)

    def getItems(self):
        text = requests.get(self.url).text
        titles = self.titlePattern.findall(text)
        bodies = self.bodyPattern.findall(text)
        for title, body in zip(titles, bodies):
            yield NewsItem(title, wrap(body))


class PlainDestination:
    @staticmethod
    def receiveItems(items):
        for item in items:
            print(item.title)
            print('-'*len(item.title))
            print(item.body)

class HTMLDestination:
    def __init__(self, filename):
        self.filename = filename

    def receiveItems(self, items):
        out = open(self.filename, 'w')
        out.write("""
        <html>
          <head>
            <title>Today's News</title>
          </head>
          <body>
          <h1>Today's News</h1>
        """)

        out.write('<ul>')
        id = 0
        for item in items:
            id += 1
            out.write('<li><a href="#%i">%s</a></li>' % (id, item.title))
        out.write('</ul')

        id = 0
        for item in items:
            id += 1
            out.write('<h2><a name="%i">%s</a></li>' % (id, item.title))
            out.write('<pre>%s</pre>' % item.body)

        out.write("""
          </body>
        </html>
        """)

    def runDefaultSetup(self):
        agent = NewsAgent()

        bbc_url = 'http://news.bbc.co.uk/text_only.stm'
        bbc_title = r'(?s)a href="[^"]*">\s*<b>\s*(.*?)\s*</b>'
        bbc_body = r'(?s)</a>\s*<br />\s*(.*?)\s*<'
        bbc = SimpleWebSource(bbc_url, bbc_title, bbc_body)

        agent.addSource(bbc)

        clpa_server = 'news.foo.bar'
        clpa_group = 'comp.land.python.announce'
        clpa_window = 1
        clpa = NNTPSource(clpa_server, clpa_group, clpa_window)

        agent.addSource(clpa)

        agent.addDestination(PlainDestination())
        agent.addDestination(HTMLDestination('news.html'))

        agent.distribute()

    if __name__ == '__main__':
        runDefaultSetup()
