import time

import requests

from mlflow.utils.logging_utils import eprint
from mlflow.utils.string_utils import strip_suffix


RESOURCE_DOES_NOT_EXIST = 'RESOURCE_DOES_NOT_EXIST'


def http_request(hostname, endpoint, retries=3, retry_interval=3, **kwargs):
    """
    Makes an HTTP request with the specified method to the specified hostname/endpoint. Retries
    up to `retries` times if a request fails with a server error (e.g. error code 500), waiting
    `retry_interval` seconds between successive retries. Parses the API response (assumed to be
    JSON) into a Python object and returns it.

    :param headers: Request headers to use when making the HTTP request
    :param req_body_json: Dictionary containing the request body
    :param params: Query parameters for the request
    :return: Parsed API response
    """
    cleaned_hostname = strip_suffix(hostname, '/')
    url = "%s%s" % (cleaned_hostname, endpoint)
    for i in range(retries):
        response = requests.request(url=url, **kwargs)
        if response.status_code >= 200 and response.status_code < 500:
            return response
        else:
            eprint("API request to %s failed with code %s != 200, retrying up to %s more times. "
                   "API response body: %s" % (url, response.status_code, retries - i - 1,
                                              response.text))
            time.sleep(retry_interval)
    raise Exception("API request to %s failed to return code 200 after %s tries" % (url, retries))
