import requests
import json
from oxapay.utils import check_uri_security
from oxapay.error import APIError, ConnectionError, InvalidResponseError
from oxapay.api_resources import SuperClient


class Client(SuperClient):
    """
    API client for Oxapay *Exchange* API
    Entry Point for making request to the Oxapay *Enchange* API
    Full API docs available here: https://docs.oxapay.com/api-reference/exchange-request
    """
    BASE_API_URI = "https://api.oxapay.com/exchange/"
    def __init__(self, api_key, base_api_uri = None, timeout = None):
        super().__init__()
        self._api_key = api_key
        self.base_api_uri = check_uri_security(base_api_uri or self.BASE_API_URI)
        self.timeout = timeout
    
    def _make_url(self, endpoint):
        return self.base_api_uri + endpoint
    
    def exchange_request(self, **kwargs):
        endpoint = '/request'
        return self._request('post', endpoint, required_params=['toCurrency', 'fromCurrency', 'amount'], action= "initiate currency conversion",**kwargs)
    
    def exchange_history(self, *kwargs):
        endpoint = '/list'
        return self._request('post', endpoint, **kwargs)
    
    def _request(self, method, endpoint, required_params = None, action = None, **kwargs):
        kwargs['key'] = self._api_key
        if required_params:
            Client._check_params(required_params, action, kwargs)
        try:
            response = getattr(self.session, method)(self._make_url(endpoint), timeout = self.timeout, data = json.dumps(kwargs))
        except Exception as e:
            raise ConnectionError(e)
        try:
            js = response.json()
            if js['result'] != 100:
                raise APIError(
                    js['result'],
                    response.content.decode('utf-8'),
                    js
                )
            else:
                return js
        except requests.exceptions.JSONDecodeError as e:
            raise InvalidResponseError()