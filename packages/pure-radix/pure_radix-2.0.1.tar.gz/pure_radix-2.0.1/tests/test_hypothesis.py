import pytest

from pure_radix import SetNode

from .conftest import node_to_elementary

try:
    import hypothesis
    from hypothesis import strategies as st
except ImportError:
    pytest.skip("hypothesis not installed, skipping", allow_module_level=True)


def generate(sequences, delete, output):
    """
    First add a bunch of sequences, then delete a subset of them. Do it in different orders to try
    to expose bugs in the radix tree code.
    """
    sequences = tuple(tuple(x) for x in sequences)

    def _list(x, n):
        return st.lists(x, min_size=n, max_size=n)

    @hypothesis.given(
        creation=st.permutations(range(len(sequences))),
        deletion=st.permutations(delete),
        creation_prune=_list(st.booleans(), len(sequences)),
        deletion_prune=_list(st.booleans(), len(delete)),
    )
    def test_it(creation, deletion, creation_prune, deletion_prune):
        t = SetNode()
        for i in creation:
            seq = sequences[i]
            t.node_get(seq)  # this should not raise an exception
            t.node_force(seq).add(i)
            if creation_prune[i]:
                t.node_prune()

        for i, prune in zip(delete, deletion_prune):
            seq = sequences[i]
            t.node_get(seq).remove(i)
            if prune:
                t.node_prune()

        t.node_prune()

        assert node_to_elementary(t) == output

    return test_it


test_seq1 = generate(
    [
        (10,),
        (10, 11),
        (10, 11),
        (10, 12),
        (10, 11, 12),
        (10, 11, 12, 13, 14),
        (10, 11, 12, 13, 14),
        (10, 11, 12, 13, 14, 15),
        (10, 11, 12, 13, 20, 21),
        (60,),
        (70,),
    ],
    [0, 1, 3, 5, 6, 8, 9],
    {
        (10, 11): {
            (): {2},
            (12,): {
                (): {4},
                (13, 14, 15): {
                    (): {7},
                },
            },
        },
        (70,): {(): {10}}
    },
)

