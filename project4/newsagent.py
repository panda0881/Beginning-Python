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