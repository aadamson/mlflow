from mlflow.entities._mlflow_object import _MLflowObject
from mlflow.entities.metric_group_param import MetricGroupParam
from mlflow.protos.service_pb2 import MetricGroupEntry as ProtoMetricGroupEntry


class MetricGroupEntry(_MLflowObject):
    """
    Metric group entry object.
    """

    def __init__(self, params, value, timestamp):
        self._params = params
        self._value = value
        self._timestamp = timestamp

    @property
    def params(self):
        """List of :py:class:`mlflow.entities.MetricGroupParam` for the current entry."""
        return self._params

    @property
    def value(self):
        """Float value of the metric group entry."""
        return self._value

    @property
    def timestamp(self):
        """Metric group entry timestamp as an integer (milliseconds since the Unix epoch)."""
        return self._timestamp

    def to_proto(self):
        metric_group_entry = ProtoMetricGroupEntry()
        metric_group_entry.params.extend([p.to_proto() for p in self.params])
        metric_group_entry.value = self.value
        metric_group_entry.timestamp = self.timestamp
        return metric_group_entry

    @classmethod
    def from_proto(cls, proto):
        metric_group_entry = cls(
            [MetricGroupParam.from_proto(p) for p in proto.params],
            proto.value,
            proto.timestamp
        )
        return metric_group_entry

    @classmethod
    def _properties(cls):
        # TODO: Hard coding this list of props for now. There has to be a clearer way...
        return ["params", "value", "timestamp"]
