from pure_radix import SetNode


def node_to_elementary(node: "SetNode"):
    d = {
        value.node_prefix: node_to_elementary(value)
        for key, value in sorted(node.node_children.items())
    }
    if node.raw_data:
        d[()] = node.data
    return d
