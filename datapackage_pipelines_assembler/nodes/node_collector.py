from .basic_nodes import DerivedCSVProcessingNode, DerivedJSONProcessingNode, \
    NonTabularProcessingNode, DerivedPreviewProcessingNode

ORDERED_NODE_CLASSES = [
    NonTabularProcessingNode,
    DerivedCSVProcessingNode,
    DerivedPreviewProcessingNode,
    DerivedJSONProcessingNode,
]


def collect_artifacts(artifacts, outputs):
    for cls in ORDERED_NODE_CLASSES:
        node = cls(artifacts, outputs)
        ret = list(node.get_artifacts())
        artifacts.extend(ret)
        yield from ret
