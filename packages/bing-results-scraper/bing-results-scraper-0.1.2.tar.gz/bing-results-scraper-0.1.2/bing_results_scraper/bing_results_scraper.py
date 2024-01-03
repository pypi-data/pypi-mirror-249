# Importing required modules
import requests
from bs4 import BeautifulSoup as bs
import urllib

# Mapping HTTP response status codes to their meanings
httpResponseStatusCodes = {
    100 : 'Continue',
    101 : 'Switching Protocol',
    102 : 'Processing (WebDAV)',
    103 : 'Early Hints',
    200 : 'Success',
    201 : 'Created',
    202 : 'Accepted',
    203 : 'Non-Authoritative Information',
    204 : 'No Content',
    205 : 'Reset Content',
    206 : 'Partial Content',
    207 : 'Multi-Status (WebDAV)',
    208 : 'Already Reported (WebDAV)',
    226 : 'IM Used (HTTP Delta encoding)',
    300 : 'Multiple Choice',
    301 : 'Moved Permanently',
    302 : 'Found',
    303 : 'See Other',
    304 : 'Not Modified',
    305 : 'Use Proxy',
    306 : 'Unused',
    307 : 'Temporary Redirect',
    308 : 'Permanent Redirect',
    400 : 'Bad Request',
    401 : 'Unauthorized',
    402 : 'Payment Required',
    403 : 'Forbidden',
    404 : 'Not Found',
    405 : 'Method Not Allowed',
    406 : 'Not Acceptable',
    407 : 'Proxy Authentication Required',
    408 : 'Request Timeout',
    409 : 'Conflict',
    410 : 'Gone',
    411 : 'Length Required',
    412 : 'Precondition Failed',
    413 : 'Payload Too Large',
    414 : 'URI Too Long',
    415 : 'Unsupported Media Type',
    416 : 'Range Not Satisfiable',
    417 : 'Expectation Failed',
    418 : 'I am a teapot',
    421 : 'Misdirected Request',
    422 : 'Unprocessable Entity (WebDAV)',
    423 : 'Locked (WebDAV)',
    424 : 'Failed Dependency (WebDAV)',
    425 : 'Too Early',
    426 : 'Upgrade Required',
    428 : 'Precondition Required',
    429 : 'Too Many Requests',
    431 : 'Request Header Fields Too Large',
    451 : 'Unavailable For Legal Reasons',
    500 : 'Internal Server Error',
    501 : 'Not Implemented',
    502 : 'Bad Gateway',
    503 : 'Service Unavailable',
    504 : 'Gateway Timeout',
    505 : 'HTTP Version Not Supported',
    506 : 'Variant Also Negotiates',
    507 : 'Insufficient Storage (WebDAV)',
    508 : 'Loop Detected (WebDAV)',
    510 : 'Not Extended',
    511 : 'Network Authentication Required'
}

# Class for Bing Search Scraper
class BingScraper():
    # Default headers for the scraper
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
    
    def __init__(self,headers=headers):
        """
        Constructor to initialize the BingScraper object.

        :param headers: Optional headers for the HTTP requests.
        """
        self.headers = headers

    def get_results(self, q, headers=None):
        """
        Method to fetch Bing search results for a given query.

        :param q: Query string for the Bing search.
        :param headers: Optional headers for the HTTP request.

        :return: Dictionary containing search results and status information.
        """
        if not headers:
            headers = self.headers
            
        q_encode=urllib.parse.quote_plus(f"{q}")
        url = ('https://www.bing.com/search?q='+q_encode)
        res = requests.get(url, headers=headers)

        results = {'query':url, 'organic_results':list(dict()), 'status':httpResponseStatusCodes.get(res.status_code)}
        if res.status_code == 200:
            soup = bs(res.content, "html.parser")
            if soup.find('ol',id="b_results"):
                for pos, elm in enumerate(soup.find('ol',id="b_results").find_all('li',class_='b_algo')):
                    source = elm.find('div',class_="tptt").text
                    title = elm.find('h2').text
                    link = elm.find('h2').find('a')['href']
                    summary = elm.find('p').text
                    results['organic_results'].append({'position':pos+1, 'source':source, 'title':title, 'link':link, 'summary':summary})
            results['number_of_results'] = len(results['organic_results'])
        return results