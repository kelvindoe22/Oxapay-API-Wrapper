import requests
import json
import hmac
import hashlib
from oxapay.utils import check_uri_security
from oxapay.error import APIError, ConnectionError, InvalidResponseError
from oxapay.api_resources import SuperClient

class Client(SuperClient):
    """
    API client for Oxapay *Payout* API
    Entry Point for making request to the Oxapay *PAYOUT* API
    Full API docs available here: https://oxapay.com/payout-api
    """
    BASE_API_URI = "https://api.oxapay.com/api/"
    def __init__(self, api_key, base_api_uri = None, timeout = None):
        super().__init__()
        self._api_key = api_key
        self.timeout = timeout
        self.base_api_uri = check_uri_security(base_api_uri or self.BASE_API_URI)
    
    def _make_url(self, endpoint):
        return self.base_api_uri + endpoint
    
    def create_payout(self, **kwargs):
        endpoint = '/send'
        return self._request('post', endpoint, required_params=['currency', 'amount', 'address'], action="send payout", **kwargs)
        
    def payout_information(self, **kwargs):
        endpoint = '/inquiry'
        return self._request('post', endpoint,required_params=['trackId'], action = "retrieve payout information", **kwargs)

    def payout_balance(self, **kwargs):
        endpoint = '/list'
        return self._request('post', endpoint, **kwargs)

    def account_balance(self, **kwargs):
        endpoint = '/balance'
        return self._request('post', endpoint, **kwargs)
    
    def verify_webhook(self, post_data, hmac_header):
        return hmac_header == hmac.new(self._api_key.encode(), post_data, hashlib.sha512).hexdigest()

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
