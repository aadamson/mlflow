from mlflow.entities._mlflow_object import _MLflowObject
from mlflow.entities.metric_group_entry import MetricGroupEntry
from mlflow.protos.service_pb2 import MetricGroup as ProtoMetricGroup


class MetricGroup(_MLflowObject):
    """
    MetricGroup object.
    """

    def __init__(self, key, entries):
        self._key = key
        self._entries = entries

    @property
    def key(self):
        """String key corresponding to the metric group name."""
        return self._key

    @property
    def entries(self):
        """List of entries of the metric group"""
        return self._entries

    def to_proto(self):
        metric_group = ProtoMetricGroup()
        metric_group.key = self.key
        metric_group.entries.extend([e.to_proto() for e in self.entries])
        return metric_group

    @classmethod
    def from_proto(cls, proto):
        return cls(proto.key, [MetricGroupEntry.from_proto(e) for e in proto.entries])

    @classmethod
    def _properties(cls):
        # TODO: Hard coding this list of props for now. There has to be a clearer way...
        return ["key", "entries"]
