import requests.session
import time
import urllib.parse
import hashlib
import hmac
import base64


class KrakenAPI:
    """Kraken.com cryptocurrency Exchange API."""

    def __init__(self, api_key='', api_secret=''):
        """Create an object with authentication information.

        :param api_key: (optional) key identifier for queries to the API
        :type api_key: str
        :param api_secret: (optional) actual private key used to sign messages
        :type api_secret: str
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = 'https://api.kraken.com'
        self.api_version = '0'
        self.session = requests.session()
        self.session.headers.update({
            'User-Agent': 'kraken/ (https://github.com/Cryptomamy/Cryptomamy_kraken_api)'
        })
        self.response = None
        self.json_options = {}

    def set_json_options(self, **kwargs):
        """Set keyword arguments to be passed to JSON deserialization.

        :param kwargs: passed to :py:meth:`requests.Response.json`
        :returns: this instance for chaining
        """
        self.json_options = kwargs
        return self

    def close(self):
        """Close the session."""
        self.session.close()

    def load_key(self, path):
        """Load key and secret from file.

        Expected file format is key and secret on separate lines.

        :param path: path to keyfile
        :type path: str
        """
        with open(path, 'r') as f:
            self.api_key = f.readline().strip()
            self.api_secret = f.readline().strip()

    def _query(self, url_path, data=None, headers=None, timeout=None):
        """Low-level query handling.

        .. note::
           Use :py:meth:`query_private` or :py:meth:`query_public`
           unless you have a good reason not to.

        :param url_path: API URL path sans host
        :type url_path: str
        :param data: API request parameters
        :type data: dict
        :param headers: (optional) HTTPS headers
        :type headers: dict
        :param timeout: (optional) if not ``None``, a :py:exc:`requests.HTTPError`
                        will be thrown after ``timeout`` seconds if a response
                        has not been received
        :type timeout: int or float
        :returns: :py:meth:`requests.Response.json`-deserialized Python object
        :raises: :py:exc:`requests.HTTPError`: if response status not successful
        """
        if data is None:
            data = {}
        if headers is None:
            headers = {}

        url = self.base_url + url_path

        self.response = self.session.post(url, data=data, headers=headers, timeout=timeout)

        self.response.raise_for_status()  # Raises an exception for non-successful responses

        return self.response.json(**self.json_options) if self.response.content else None

    def query_public(self, method, data=None, timeout=None):
        """Performs an API query that does not require a valid API key/secret pair.

        :param method: API method name
        :type method: str
        :param data: (optional) API request parameters
        :type data: dict
        :param timeout: (optional) if not ``None``, a :py:exc:`requests.HTTPError`
                        will be thrown after ``timeout`` seconds if a response
                        has not been received
        :type timeout: int or float
        :returns: :py:meth:`requests.Response.json`-deserialized Python object
        """
        if data is None:
            data = {}

        url_path = f'/{self.api_version}/public/{method}'

        return self._query(url_path, data, timeout=timeout)

    def query_private(self, method, data=None, timeout=None):
        """Performs an API query that requires a valid API key/secret pair.

        :param method: API method name
        :type method: str
        :param data: (optional) API request parameters
        :type data: dict
        :param timeout: (optional) if not ``None``, a :py:exc:`requests.HTTPError`
                        will be thrown after ``timeout`` seconds if a response
                        has not been received
        :type timeout: int or float
        :returns: :py:meth:`requests.Response.json`-deserialized Python object
        """
        if data is None:
            data = {}

        if not self.api_key or not self.api_secret:
            raise Exception('Either api_key or api_secret is not set! (Use `load_key()`).')

        data['nonce'] = self._generate_nonce()

        url_path = f'/{self.api_version}/private/{method}'

        headers = {
            'API-Key': self.api_key,
            'API-Sign': self._sign(data, url_path)
        }

        return self._query(url_path, data, headers, timeout=timeout)

    @staticmethod
    def _generate_nonce():
        """Generate a nonce value.

        :returns: an always-increasing unsigned integer (up to 64 bits wide)
        """
        return int(1000 * time.time())

    def _sign(self, data, url_path):
        """Sign request data according to Kraken's scheme.

        :param data: API request parameters
        :type data: dict
        :param url_path: API URL path sans host
        :type url_path: str
        :returns: signature digest
        """
        post_data = urllib.parse.urlencode(data)

        encoded = (str(data['nonce']) + urllib.parse.quote(post_data)).encode()
        message = url_path.encode() + hashlib.sha256(encoded).digest()

        signature = hmac.new(base64.b64decode(self.api_secret), message, hashlib.sha512)
        sig_digest = base64.b64encode(signature.digest())

        return sig_digest.decode()
