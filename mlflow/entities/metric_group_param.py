from mlflow.entities._mlflow_object import _MLflowObject
from mlflow.protos.service_pb2 import MetricGroupParam as ProtoMetricGroupParam


class MetricGroupParam(_MLflowObject):
    """
    Metric group parameter object.
    """

    def __init__(self, key, value):
        self._key = key
        self._value = value

    @property
    def key(self):
        """String key corresponding to the metric group parameter name."""
        return self._key

    @property
    def value(self):
        """String value of the metric group parameter."""
        return self._value

    def to_proto(self):
        metric_group_param = ProtoMetricGroupParam()
        metric_group_param.key = self.key
        metric_group_param.value = self.value
        return metric_group_param

    @classmethod
    def from_proto(cls, proto):
        return cls(proto.key, proto.value)

    @classmethod
    def _properties(cls):
        # TODO: Hard coding this list of props for now. There has to be a clearer way...
        return ["key", "value"]
