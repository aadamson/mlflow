import base64
from json import loads

from mlflow.utils.logging_utils import eprint
from mlflow.utils.rest_utils import http_request


RESOURCE_DOES_NOT_EXIST = 'RESOURCE_DOES_NOT_EXIST'


def _fail_malformed_databricks_auth(profile):
    raise Exception("Got malformed Databricks CLI profile '%s'. Please make sure the Databricks "
                    "CLI is properly configured as described at "
                    "https://github.com/databricks/databricks-cli." % profile)


def get_databricks_http_request_kwargs_or_fail(profile=None):
    """
    Reads in configuration necessary to make HTTP requests to a Databricks server. This
    uses the Databricks CLI's ConfigProvider interface to load the DatabricksConfig object.
    This method will throw an exception if sufficient auth cannot be found.

    :param profile: Databricks CLI profile. If not provided, we will read the default profile.
    :return: Dictionary with parameters that can be passed to http_request(). This will
             at least include the hostname and headers sufficient to authenticate to Databricks.
    """
    from databricks_cli.configure import provider

    if not hasattr(provider, 'get_config'):
        eprint("Warning: support for databricks-cli<0.8.0 is deprecated and will be removed"
               " in a future version.")
        config = provider.get_config_for_profile(profile)
    elif profile:
        config = provider.ProfileConfigProvider(profile).get_config()
    else:
        config = provider.get_config()

    hostname = config.host
    if not hostname:
        _fail_malformed_databricks_auth(profile)

    auth_str = None
    if config.username is not None and config.password is not None:
        basic_auth_str = ("%s:%s" % (config.username, config.password)).encode("utf-8")
        auth_str = "Basic " + base64.standard_b64encode(basic_auth_str).decode("utf-8")
    elif config.token:
        auth_str = "Bearer %s" % config.token
    else:
        _fail_malformed_databricks_auth(profile)

    headers = {
        "Authorization": auth_str,
    }

    verify = True
    if hasattr(config, 'insecure') and config.insecure:
        verify = False

    return {
        'hostname': hostname,
        'headers': headers,
        'verify': verify,
    }


def databricks_api_request(endpoint, method, json=None):
    final_endpoint = "/api/2.0/%s" % endpoint
    request_params = get_databricks_http_request_kwargs_or_fail()
    response = http_request(endpoint=final_endpoint, method=method, json=json, **request_params)
    return loads(response.text)
