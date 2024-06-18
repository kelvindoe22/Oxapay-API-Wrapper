import requests
import json
from oxapay.error import ConnectionError, InvalidResponseError, APIError, ParamRequiredError



class SuperClient(object):
    def __init__(self):
        self.session = self._build_session()
    
    def _build_session(self):
        session =  requests.session()
        session.headers.update({'Content-Type' : 'application/json'})
        return session
    
    def prices(self):
        return self._general_request("https://api.oxapay.com/api/prices", 'post')
    
    def exchange_rate(self, **kwargs):
        if 'fromCurrency' in kwargs:
            raise ParamRequiredError('fromCurrency', 'check exchange rate')
        if 'toCurrency' in kwargs:
            raise ParamRequiredError('toCurrency', 'check exchange rate')
        return self._general_request("https://api.oxapay.com/exchange/rate")
    
    def exchange_calculate(self, **kwargs):
        if 'fromCurrency' in kwargs:
            raise ParamRequiredError('fromCurrency', 'calculate exchange rate')
        if 'toCurrency' in kwargs:
            raise ParamRequiredError('toCurrency', 'calculate exchange rate')
        if 'amount' in kwargs:
            raise ParamRequiredError('amount', 'calculate exchange rate')
        return self._general_request("https://api.oxapay.com/exchange/calculate", 'post', **kwargs)
    
    def exchange_pairs(self):
        return self._general_request("https://api.oxapay.com/api/pairs", 'post')
    
    def supported_currencies(self):
        return self._general_request("https://api.oxapay.com/api/currencies", 'post')
    
    def supported_fiat_currencies(self):
        return self._general_request("https://api.oxapay.com/api/fiats", 'post')
    
    def supported_networks(self):
        return self._general_request("https://api.oxapay.com/api/networks", 'post')
    
    def system_status(self):
        """
        Checks the current state of the Oxapay API
        Returns True if active else False
        """
        try:
            return self.session.post("https://api.oxapay.com/monitor").content.decode() == 'OK'
        except:
            return False
    
    @staticmethod
    def _check_params(params, action, kwargs):
        for p in params:
            if p not in kwargs:
                raise ParamRequiredError(p, action)
        
    def _general_request(self,url, method, **kwargs):
        try:
            if not kwargs:
                response = getattr(self.session, method)(url)
            else:
                response = getattr(self.session, method)(url, data = json.dumps(kwargs))
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
        except requests.exceptions.JSONDecodeError:
            raise InvalidResponseError()

    
    def exchange_rate(self):
        try:
            response = self.session.post("https://api.oxapay.com/exchange/rate")
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
        except requests.exceptions.JSONDecodeError:
            raise InvalidResponseError()