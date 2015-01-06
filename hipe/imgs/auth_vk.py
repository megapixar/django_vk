import mimetypes

__author__ = 'Antatoly'
import urllib2, cookielib, urlparse
from urllib import urlencode
from HTMLParser import HTMLParser


class AuthVk(object):
    attr = {
        'APP_ID': 4032235,
        'PERMISSIONS': 'messages,photos,groups,status,wall,offline',
        'REDIRECT_URI': 'https://oauth.vk.com/blank.html',
        # 'REDIRECT_URI': 'http://motomaniak.pro',
        'API_VERSION': 5.27
    }

    url = 'https://oauth.vk.com/authorize?client_id={APP_ID}&scope={PERMISSIONS}' \
          '&redirect_uri={REDIRECT_URI}&response_type=token&v={API_VERSION}&display=page&lang=en'

    def get_auth_url(self):
        return self.url.format(**self.attr)

    def open_login_page(self):
        self.opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(cookielib.CookieJar()),
            urllib2.HTTPRedirectHandler()
        )

        return self.opener.open(self.get_auth_url())

    def autorisation(self, email, password):
        open_login = self.open_login_page()
        html = open_login.read()
        open_login.close()

        parser = ParserAuthVk()
        parser.feed(html)
        parser.params['email'] = email
        parser.params['pass'] = password

        open_auth = self.opener.open(parser.url, urlencode(parser.params.items()))

        # parse =  urlparse.parse_qsl(urlparse.urlparse(open_auth.geturl()).fragment)
        # url_attr = dict((k, v) for k, v in parse)
        token = self._get_access_token(open_auth.geturl())
        if token:
            return token
        else:
            auth_html = open_auth.read()
            open_auth.close()

            par = ParserAuthVk()
            par.feed(auth_html)
            sub_auth = self.opener.open(par.url)
            # auth_html = sub_auth.read()
            sub_auth.close()

            return self._get_access_token(sub_auth.geturl())

    def _get_access_token(self, url):
        parse =  urlparse.parse_qsl(urlparse.urlparse(url).fragment)
        url_attr = dict((k, v) for k, v in parse)

        if 'access_token' in url_attr and url_attr['access_token']:
            return url_attr['access_token']
        else:
            return None


class ParserAuthVk(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.params = {}
        self.in_form = False
        self.method = 'GET'
        self.url = None

    def handle_starttag(self, tag, attrs):
        _attrs = dict((k, v) for k, v in attrs)

        if tag == "form":
            self.in_form = True
            self.method = _attrs['method']
            self.url = _attrs['action']

        if tag == 'input' and _attrs['type'] in ('text', 'hidden', 'password') and self.in_form == True:
            self.params[_attrs['name']] = _attrs['value'] if "value" in _attrs else ""

    def handle_endtag(self, tag):
        if tag == "form":
            self.in_form = False
            return