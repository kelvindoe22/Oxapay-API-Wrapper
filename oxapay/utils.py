import warnings
from urllib.parse import urlparse

def uri_security_check(uri):
    """Warns if the URL is insecure."""
    if urlparse(uri).scheme != 'https':
        warning_message = (
            'WARNING: this client is sending a request to an insecure '
            'API endpoint. Any API request you make may expose your API key '
            'and secret to third parties. Consider using the default '
            'endpoint:\n\n '
            '{}\n'.format(uri)
        )
        warnings.warn(warning_message, UserWarning)
    return uri