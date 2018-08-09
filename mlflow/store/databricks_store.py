from mlflow.store.rest_store import RestStore

class DatabricksStore(RestStore):
    """
    A specific type of RestStore which includes authentication information to Databricks.
    :param http_request_kwargs arguments to add to rest_utils.http_request for all requests.
                               'hostname', 'headers', and 'secure_verify' are required.
    """
    def __init__(self, http_request_kwargs):
        if http_request_kwargs['hostname'] is None:
            raise Exception('hostname must be provided to DatabricksStore')
        if http_request_kwargs['headers'] is None:
            raise Exception('headers must be provided to DatabricksStore')
        if http_request_kwargs['verify'] is None:
            raise Exception('verify must be provided to DatabricksStore')
        super(DatabricksStore, self).__init__(http_request_kwargs)
