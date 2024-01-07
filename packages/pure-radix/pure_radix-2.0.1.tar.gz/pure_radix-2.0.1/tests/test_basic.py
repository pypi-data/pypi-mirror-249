from pure_radix import SetNode

from .conftest import node_to_elementary


def make_tree():
    return SetNode()


def test_remove():
    t = make_tree()
    n1 = t.node_force([11, 12, 13, 14, 15])
    n1.add(1)
    t.node_force([11, 21, 22, 23]).add(2)
    n2 = n1.node_force([31, 32, 33], remove=4)

    assert n1.node_sequence == (11, 12, 13, 14, 15)
    assert n2.node_sequence == (11, 31, 32, 33)

    n3 = n1.node_force([41, 42], remove=1)
    assert n3.node_sequence == (11, 12, 13, 14, 41, 42)


def test_basic():
    t = make_tree()
    t.node_force([11, 12, 13, 14, 15]).add(1)

    assert node_to_elementary(t) == {
        (11, 12, 13, 14, 15): {(): {1}},
    }

    t.node_force([11, 12, 13, 20, 21]).add(2)

    assert 2 in t.node_get((11, 12, 13)).node_get((20, 21))

    assert node_to_elementary(t) == {
        (11, 12, 13): {
            (14, 15): {(): {1}},
            (20, 21): {(): {2}},
        }
    }

    assert t.node_get([11, 12]) is None
    assert t.node_get([11, 12, 13, 14]) is None
    assert t.node_get([11, 12, 13, 14, 15, 16]) is None

    t.node_get([11, 12, 13]).add(3)

    assert node_to_elementary(t) == {
        (11, 12, 13): {
            (): {3},
            (14, 15): {(): {1}},
            (20, 21): {(): {2}},
        }
    }

    t.node_get((11, 12, 13, 14, 15)).remove(1)

    assert node_to_elementary(t) == {
        (11, 12, 13): {
            (): {3},
            (14, 15): {},
            (20, 21): {(): {2}},
        }
    }

    t.node_prune()

    assert node_to_elementary(t) == {
        (11, 12, 13): {
            (): {3},
            (20, 21): {(): {2}},
        }
    }

    t.node_get([11, 12, 13]).remove(3)
    t.node_force((11, 12, 13, 14, 15)).add(-1)

    assert node_to_elementary(t) == {
        (11, 12, 13): {
            (14, 15): {(): {-1}},
            (20, 21): {(): {2}},
        }
    }

    t.node_get([11, 12, 13, 20, 21]).remove(2)
    t.node_prune()

    assert node_to_elementary(t) == {(11, 12, 13, 14, 15): {(): {-1}}}


def test_find_closest_nodes_and_find():
    t = make_tree()

    t.node_force("banana").add(1)
    t.node_force("babana").add(2)
    t.node_force("banat").add(3)
    t.node_force("bane").add(4)
    t.node_force("apple").add(5)

    assert t.node_get("ban").node_get("bana", remove=1) == t.node_get("babana")

    word = "banana"
    for i in range(1, len(word)):
        assert t.node_get(word).node_get("", remove=i) == t.node_get(word[:-i])

    assert list(t.node_find_closest_nodes("banaba")) == [
        (4, t.node_get("bana")),
        (3, t.node_get("bane")),
        (2, t.node_get("babana")),
        (0, t.node_get("apple")),
    ]

    assert list(t.node_find_closest_nodes("pizza")) == [
        (0, t.node_get("")),
    ]

    assert list(t.node_find_closest_nodes("albatross")) == [
        (1, t.node_get("apple")),
        (0, t.node_get("ba")),
    ]

    assert list(t.node_find_closest_nodes("bin")) == [
        (1, t.node_get("ba")),
        (0, t.node_get("apple")),
    ]

    assert list(t.node_get("ba").node_find_closest_nodes("nan")) == [
        (3, t.node_get("banana")),
        (2, t.node_get("banat")),
        (1, t.node_get("bane")),
        (0, t.node_get("babana")),
    ]

    node = t.node_get("banana")
    assert node.node_sequence_offset + len(node.node_prefix) == 6

    assert set(list(n.data)[0] for n in t.node_get("ba").node_find()) == {1, 2, 3, 4}

    assert set(list(n.data)[0] for n in t.node_get("ban").node_find()) == {1, 3, 4}
