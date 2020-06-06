from html.parser import HTMLParser
from html.entities import name2codepoint
import json

class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        # print('<%s>' % tag)
        pass

    def handle_endtag(self, tag):
        # print('</%s>' % tag)
        pass

    def handle_startendtag(self, tag, attrs):
        # print('<%s/>' % tag)
        pass

    def handle_data(self, data):
        print(1, data)
        if data == 'html':
            print('自己处理咯')

    def handle_entityref(self, name):
        # print('&%s;' % name)
        pass

    def handle_charref(self, name):
        # print('&#%s;' % name)
        pass


parser = MyHTMLParser()
parser.feed('''<html>
<head></head>
<body>
<!-- test html parser -->
    <p>Some <a href=\"#\">html</a> HTML&nbsp;tutorial...<br>END</p>
</body></html>''')

print()


