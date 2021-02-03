import urllib.parse as urllib
from lxml import html as lxml_html
import json


class Parser:
    """
    Parsing a page.

    parser = Parser(content={'url': 'http://google.com'})
    parser.pars_html(html='<h1>Example</h1>')
    print(parser.result)
    """
    def __init__(self, content: bytes):
        self.byte_content: bytes = content
        self.url: str = str()
        self.urllib_url = None
        self.error: dict = dict()   # The developer can check errors before parsing html
        self._tree = None
        self.result: dict = {
                            'keywords': [],
                             'company':
                                {'domain': str(),
                                 'name': str(),
                                 'icon': str()
                                 },
                             'site': {}
                             }

        self.decode_content()

    def decode_content(self) -> None:
        """
        Decoding json into dict and finding the link.
        """
        request_json: dict = json.loads(str(self.byte_content.decode('utf-8')))
        try:
            self.url = request_json['url']
            self.urllib_url = urllib.urlparse(self.url)
        except KeyError:
            self.error = {'Error': 'Not found key url'}

    def pars_html(self, html) -> None:
        """
        Init lxml and start parser
        :param html:
        """
        self._tree = lxml_html.fromstring(html)
        self._parser()

    def _parser(self) -> None:
        """
        Core parser.
        """
        """ Main data. """
        self.result['site']['url'] = self.urllib_url.geturl()
        self.result['site']['title'] = self._tree.xpath('//title')[0].text_content().strip()
        try:
            self.result['site']['description'] = self._tree.xpath('//meta[@name="description"]')[0].get('content').strip()
        except IndexError:
            pass
        try:
            keywords = self._tree.xpath('//meta[@name="keywords"]')[0].get('content')
        except IndexError:
            pass
        else:
            for key in keywords.split(', '):
                self.result['keywords'].append(key.strip())

        """ OG data. """
        try:
            self.result['site']['og_url'] = self._tree.xpath('//meta[@property="og:url"]')[0].get('content')
        except IndexError:
            pass
        try:
            self.result['site']['og_title'] = self._tree.xpath('//meta[@property="og:title"]')[0].get('content').strip()
        except IndexError:
            pass
        try:
            self.result['site']['og_description'] = self._tree.xpath('//meta[@property="og:description"]')[0].get('content').strip()
        except IndexError:
            pass
        try:
            self.result['site']['og_type'] = self._tree.xpath('//meta[@property="og:type"]')[0].get('content').strip()
        except IndexError:
            pass
        try:
            self.result['site']['og_image'] = self._tree.xpath('//meta[@property="og:image"]')[0].get('content')
        except IndexError:
            pass

        """ Company data. """
        self.pars_icon()
        self.result['company']['domain'] = self.urllib_url.hostname
        try:
            self.result['company']['name'] = self._tree.xpath('//meta[@property="og:site_name"]')[0].get('content').strip()
        except IndexError:
            pass

    def pars_icon(self) -> None:
        """
        Parser icon site
        """
        try:
            icon = self._tree.xpath('//link[@rel="icon"]')[0].get('href')
            if len(icon) > 5:
                self.result['company']['icon'] = icon
        except IndexError:
            self.result['company']['icon'] = self.urllib_url.hostname + '/favicon.ico'
