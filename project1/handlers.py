class Handler:

    def callback(self, prefix, name, *args):
        method = getattr(self, prefix+name, None)
        if callable(method):
            return method(*args)

    def start(self, name):
        self.callback('start_', name)

    def end(self, name):
        self.callback('end_', name)

    def sub(self, name):
        def substitution(match):
            result = self.callback('sub_', name, match)
            if not result:
                result = match.group(0)
            return result
        return substitution


class HTMLRenderer(Handler):

    @staticmethod
    def start_document():
        print('<html><head><title>...</title></head><body>')

    @staticmethod
    def end_document():
        print('</body></html>')

    @staticmethod
    def start_paragraph():
        print('<p>')

    @staticmethod
    def end_paragraph():
        print('</p>')

    @staticmethod
    def start_heading():
        print('<h2>')

    @staticmethod
    def end_heading():
        print('</h2>')

    @staticmethod
    def start_list():
        print('<ul>')

    @staticmethod
    def end_list():
        print('</ul>')

    @staticmethod
    def start_listitem():
        print('<li>')

    @staticmethod
    def end_listitem():
        print('</li>')

    @staticmethod
    def start_tile():
        print('<h1>')

    @staticmethod
    def end_title():
        print('</h1>')

    @staticmethod
    def sub_emphasis(match):
        return '<em>%s</em>' % match.group(1)

    @staticmethod
    def sub_url(match):
        return '<a href="%s">%s</a>' % (match.group(1), match.group(1))

    @staticmethod
    def sub_mail(match):
        return '<a href="mailto:%s">%s</a>' % (match.group(1), match.group(1))

    @staticmethod
    def feed(data):
        print(data)
