from typing import (
    Any,
    Callable,
    Generic,
    Hashable,
    Iterable,
    Iterator,
    Optional as Opt,
    Sequence,
    TypeVar,
)
import attr


S = TypeVar("S")
T = TypeVar("T", bound=Hashable)


@attr.s(slots=True)
class TraverseResult:
    """
    Attributes
    ----------
    sequence_index: int | None
        Number of matching sequence elements. None if it's the whole sequence.
    node: Node
        Node.
    node_prefix_index: int | None
        Number of matching elements in the :attr:`Node.node_prefix`. None if the entire prefix
        matched.
    """

    sequence_index: "int | None" = attr.ib()
    node: "ANode" = attr.ib()
    node_prefix_index: "int | None" = attr.ib()


@attr.s(slots=True)
class VisitFrame(Generic[T]):
    node: "ANode[T]" = attr.ib()
    children: "list[ANode[T]]" = attr.ib(factory=list)
    iterator = attr.ib(default=None)


def default_enter(stack, frame):
    frame.children.extend(frame.node.node_children.values())
    return ()


def default_exit(stack, frame):
    return ()


class ANode(Generic[T]):
    """
    Abstract class implementing a node. You probably want to subclass the concrete class
    :class:`Node`.

    You must subclass this to customize the information stored in a Node. Avoid using the prefixes
    "node_" and "_node_" for methods or attributes in your subclass as it may lead to future name
    clashes.

    Don't forget to use ``@attr.s(slots=True, eq=False)``
    """

    node_parent: "ANode[T] | None"
    node_prefix: tuple[T, ...]
    node_children: "dict[T, ANode[T]]"

    @staticmethod
    def _node_match_prefix(key, child_prefix, key_start: int = 0) -> int:
        i = 0
        n_prefix = len(child_prefix)
        n_key = max(len(key) - key_start, 0)
        n = min(n_prefix, n_key)
        if not n:
            return 0
        for i in range(n):
            if key[i + key_start] != child_prefix[i]:
                return i
        return n

    def _node_new(self, parent: "Opt[ANode[T]]", prefix: Sequence[T]) -> "ANode[T]":
        node = type(self)(node_prefix=tuple(prefix))  # type: ignore
        node.node_reparent(parent)
        return node

    def node_traverse(self, sequence: Sequence[T], sequence_start_index: int = 0) -> TraverseResult:
        """
        Mostly internal method. Starting at *node*, follow the path of *sequence* by looking
        at children and their children's children and so on.
        """
        node = self
        _match_prefix = self._node_match_prefix
        n = len(sequence)
        i = sequence_start_index
        while i < n:
            key_i = sequence[i]
            child = node.node_children.get(key_i)
            if child is None:
                return TraverseResult(sequence_index=i, node_prefix_index=None, node=node)
            else:
                prefix = child.node_prefix
                matching = _match_prefix(sequence, prefix, key_start=i)
                i += matching
                if matching == len(prefix):
                    # full match
                    node = child
                else:
                    # key does not match prefix and prefix is longer than the matching part
                    return TraverseResult(
                        sequence_index=i if i < n else None,
                        node_prefix_index=matching,
                        node=child,
                    )

        return TraverseResult(sequence_index=None, node_prefix_index=None, node=node)

    def node_force(self, sequence: Sequence[T], **kw) -> "ANode[T]":
        """
        Alias for :meth:`get` with ``create=True``.
        """
        return self.node_get(sequence, create=True, **kw)  # type: ignore

    def node_get(
        self, sequence: Sequence[T], *, create: bool = False, remove: int = 0
    ) -> "Opt[ANode[T]]":
        node = self

        if remove < 0:
            raise ValueError("remove < 0")

        while remove > 0:
            n = len(node.node_prefix)
            if remove >= n:
                remove -= n
                node = node.node_parent  # type: ignore
                if node is None:
                    raise IndexError(f"attempted to remove past root, {remove} left")
            else:  # remove < n
                sequence = node.node_prefix[:-remove] + tuple(sequence)
                node = node.node_parent  # type: ignore
                remove = 0

        r = node.node_traverse(sequence)

        seq_index = r.sequence_index
        prefix_index = r.node_prefix_index

        if seq_index is None and prefix_index is None:
            return r.node  # full exact match
        elif not create:
            return None

        if prefix_index is None:
            # need to create a new node
            return self._node_new(parent=r.node, prefix=sequence[seq_index:])
        else:
            # we cut the node in two
            # "node -> child" becomes "node -> mid -> child"
            child = r.node
            node = child.node_parent  # type: ignore[assignment]
            child.node_reparent(None)
            prefix = child.node_prefix
            mid = self._node_new(parent=node, prefix=prefix[:prefix_index])
            if seq_index is None:
                result = mid
            else:
                result = self._node_new(parent=mid, prefix=sequence[seq_index:])
            child.node_prefix = prefix[prefix_index:]
            child.node_reparent(mid)
            return result

    def node_find_closest_nodes(self, sequence: Sequence[T]) -> "Iterator[tuple[int, ANode[T]]]":
        """
        Yield pairs (longest_common_prefix, node) in descending order.
        """
        r = self.node_traverse(sequence)
        i = r.sequence_index
        j = r.node_prefix_index

        if i is None:
            i = len(sequence)
        if j is None:
            j = len(r.node.node_prefix)

        # enumerate everything under the node that was returned
        yield i, r.node

        # now enumerate all the "uncle" nodes
        current = r.node
        i -= j
        while True:
            child = current
            if child is self:
                break
            current = child.node_parent  # type: ignore

            for sibling in current.node_children.values():
                if sibling is not child:
                    yield i, sibling

            i -= len(current.node_prefix)

    def node_find(self, has_data: bool = True) -> "Iterator[ANode[T]]":
        """
        Recursively iterate through every child node. By default, only yield nodes that have
        data (where :attr:`Node.node_should_prune` is false).
        """
        active = [self]
        while active:
            node = active.pop()
            active.extend(node.node_children.values())
            if not has_data or not node.node_should_prune:
                yield node

    def node_visit(
        self,
        enter: Callable[[list[VisitFrame], VisitFrame], Iterable[S]] = default_enter,
        exit: Callable[[list[VisitFrame], VisitFrame], Iterable[S]] = default_exit,
        frame_class=VisitFrame,
    ) -> Iterator[S]:
        """
        Visit nodes recursively. Call ``enter(stack, frame)`` before recursing down a node's
        children, and call ``exit(stack, frame)`` after the node and its children have all
        been visited.

        The *enter* function must modify :attr:`VisitFrame.children` (initially an empty list)
        and add to it the subset of child nodes that should be visited.

        Both *enter* and *exit* must return an iterable. The values from this iterable will be
        yielded from this generator.

        Example::

            def _enter(stack, frame):
                frame.children.extend(frame.node.node_children.values())
                yield ("enter", frame.node)

            def _exit(stack, frame):
                yield ("exit", frame.node)

            for action, node in t.node_visit(enter=_enter, exit=_exit):
                print(action, node)
        """
        stack: list[VisitFrame] = []
        next_child = self
        frame: VisitFrame

        if False:
            frame = None  # exists only to prevent a linter warning below

        while True:
            if next_child is None:
                # done with this frame
                yield from exit(stack, frame)
                stack.pop()
                if not stack:
                    break
                frame = stack[-1]
            else:
                frame = frame_class(next_child)
                stack.append(frame)
                yield from enter(stack, frame)
                frame.iterator = iter(frame.children)

            next_child = next(frame.iterator, None)  # type: ignore

    def node_reparent(self, parent: "ANode[T] | None") -> None:
        """
        Change the parent of this node. If you need to add a hook that runs before or after a
        change of parent, a great way is to override this method and use ``super().node_reparent``.
        """
        old = self.node_parent
        if old is parent:
            return

        key = self.node_prefix[0]

        if old is not None:
            child = old.node_children.pop(key)
            assert child is self

        self.node_parent = None

        if parent is not None:
            assert key not in parent.node_children
            parent.node_children[key] = self
            self.node_parent = parent

    @property
    def node_should_prune(self):
        """
        Should this node be pruned whenever possible? Default implementation always returns false.
        """
        return False

    def node_prune_maybe(self) -> None:
        """
        Try to prune this node if possible and if :attr:`node_should_prune` is true.
        """
        n = len(self.node_children)
        if n <= 1 and self.node_should_prune and self.node_parent is not None:
            if n == 0:
                self.node_reparent(None)
            elif n == 1:
                self._node_replace_with_child()

    def _node_replace_with_child(self):
        parent = self.node_parent
        self.node_reparent(None)
        [child] = self.node_children.values()
        child.node_reparent(None)
        child.node_prefix = self.node_prefix + child.node_prefix
        child.node_reparent(parent)

    def node_prune(self, enter=default_enter) -> None:
        """
        Recursively prune the tree.
        """

        def _exit(stack, frame):
            frame.node.node_prune_maybe()
            return ()

        for _ in self.node_visit(enter=enter, exit=_exit):
            pass

    @property
    def node_sequence(self) -> tuple[T, ...]:
        lst = []
        node: Opt[ANode] = self
        while node is not None:
            lst.append(node.node_prefix)
            node = node.node_parent
        return tuple(x for xs in reversed(lst) for x in xs)

    @property
    def node_sequence_offset(self) -> int:
        return sum(len(node.node_prefix) for node in self.node_parents)

    @property
    def node_parents(self):
        x = self.node_parent
        while x is not None:
            yield x
            x = x.node_parent

    def node_debug_string(self, indent="  ", initial_indent="") -> str:
        def _enter(stack, frame):
            yield initial_indent
            yield from (indent for _ in range(1, len(stack)))
            node = frame.node
            yield from node.node_debug_string_prefix()
            this = node.node_debug_string_data()
            if this:
                yield " "
                yield from this
            yield "\n"
            default_enter(stack, frame)

        lst = list(self.node_visit(enter=_enter))
        lst.pop()  # discard last newline
        return "".join(lst)

    def node_debug_string_prefix(self):
        return (repr(list(self.node_prefix)),)

    def node_debug_string_data(self):
        return (repr(self),)


@attr.s(slots=True, eq=False)
class Node(ANode, Generic[T]):
    """
    You must subclass this to customize the information stored in a Node. Avoid using the prefixes
    "node_" and "_node_" for methods or attributes in your subclass as it may lead to future name
    clashes.

    Don't forget to use ``@attr.s(slots=True, eq=False)``
    """

    node_parent: "ANode[T] | None" = attr.ib(init=False, default=None, repr=False)
    node_prefix: tuple[T, ...] = attr.ib(converter=tuple, default=(), repr=False)
    node_children: "dict[T, ANode[T]]" = attr.ib(factory=dict, repr=False)


@attr.s(slots=True, eq=False)
class RawDataNode(Node):
    raw_data = attr.ib(default=None)

    @property
    def node_should_prune(self) -> bool:
        return not self.raw_data

    def node_debug_string_data(self):
        x = self.raw_data
        return (repr(x),) if x else ()


@attr.s(slots=True, eq=False)
class SetNode(RawDataNode):
    """
    Node which holds a set in :attr:`data`. This attribute is initialized lazily.
    """

    @property
    def data(self):
        raw_data = self.raw_data
        if raw_data is None:
            self.raw_data = raw_data = set()
        return raw_data

    def add(self, x):
        self.data.add(x)

    def update(self, xs):
        self.data.update(xs)

    def discard(self, x):
        if self.raw_data:
            self.data.discard(x)

    def remove(self, x):
        self.data.remove(x)

    def clear(self):
        self.data.clear()

    def __iter__(self):
        return iter(self.raw_data or ())

    def __contains__(self, x):
        return x in (self.raw_data or ())
