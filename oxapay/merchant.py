import requests
import json
import hmac
import hashlib
from oxapay.utils import check_uri_security
from oxapay.error import APIError, ConnectionError, InvalidResponseError
from oxapay.api_resources import SuperClient

class Client(SuperClient):
    """
    API Client for Oxapay Merchant API
    Entry Point for making request to the Oxapay *MERCHANT* API
    Full API docs available here: https://oxapay.com/merchant-api
    """
    BASE_API_URI = "https://api.oxapay.com/merchants"
    def __init__(self, api_key, base_api_uri = None, timeout = None):
        super().__init__()
        self._api_key = api_key
        self.base_api_uri = check_uri_security(base_api_uri or self.BASE_API_URI).strip('/')
        self.timeout = timeout
    
    def _make_url(self, endpoint):
        return self.base_api_uri + endpoint
    
    def _build_session(self):
        session =  requests.session()
        session.headers.update({'Content-Type' : 'application/json'})
        return session
    
    def create_invoice(self, **kwargs):
        endpoint = '/request'
        return self._request('post', endpoint, required_params=['amount'], action='create invoice', **kwargs)
    
    def create_white_label_payment(self, **kwargs):
        endpoint = '/request/whitelabel'   
        return self._request('post', endpoint, required_params = ['payCurrency', 'amount'], action = 'create white label payment', **kwargs)
    
    def create_static_wallet(self, **kwargs):
        endpoint = '/request/staticaddress'
        return self._request('post', endpoint, required_params=['currency'], action='create static wallet', **kwargs)
    
    def revoke_static_wallet(self, **kwargs):
        endpoint = '/revoke/staticaddress'
        return self._request('post', endpoint, required_params=['address'], action='revoke static wallet', **kwargs)
    
    def payment_information(self, **kwargs):
        endpoint = '/inquiry'
        return self._request('post', endpoint, required_params=['trackId'], action='retrieve payment information', **kwargs)
    
    def payment_history(self, **kwargs):
        endpoint = '/list'
        return self._request('post', endpoint, **kwargs)
    
    def accepted_coins(self):
        endpoint = '/allowedCoins'
        return self._request('post', endpoint)
    
    def verify_webhook(self, post_data, hmac_header):
        return hmac_header == hmac.new(self._api_key.encode(), post_data, hashlib.sha512).hexdigest()
    
    def _request(self, method, endpoint, required_params = None, action =None , **kwargs):
        kwargs['merchant'] = self._api_key
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
    
    def close(self):
        self.session.close()

    def __exit__(self):
        self.close()
    