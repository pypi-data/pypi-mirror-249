

class GraphCreationFailure(RuntimeError):
    pass


class GraphCreationVerticesNonUnique(GraphCreationFailure):
    pass


class GraphCreationMissingVertex(GraphCreationFailure):
    pass


class GraphAccessInvalid(RuntimeError):
    pass


class GraphInvalidVertex(GraphAccessInvalid):
    pass


class DirectedGraph:
    def __init__(self, *, vertices: list[int], edges: list[tuple[int, int]]):
        if len(set(vertices)) != len(vertices):
            raise GraphCreationVerticesNonUnique("Vertex list elements must be unique.")

        self._adj_lists = {v: [] for v in vertices}
        for src, dst in edges:
            if src not in vertices:
                raise GraphCreationMissingVertex(f"Vertex '{src}' present in edge list does not exist.")
            if dst not in vertices:
                raise GraphCreationMissingVertex(f"Vertex '{dst}' present in edge list does not exist.")
            self._adj_lists[src].append(dst)

    def vertices(self) -> list[int]:
        return list(self._adj_lists.keys())

    def adjacent(self, vert: int) -> list[int]:
        if vert not in self.vertices():
            raise GraphInvalidVertex(f"Vertex '{vert}' does not exist.")
        return self._adj_lists[vert]

    def _is_cyclic_impl(self, v, visited, rec_stack):

        # Mark current node as visited and
        # adds to recursion stack
        visited[v] = True
        rec_stack[v] = True

        # Recur for all neighbours
        # if any neighbour is visited and in
        # rec_stack then graph is cyclic
        for neighbour in self.adjacent(v):
            if not visited[neighbour]:
                if self._is_cyclic_impl(neighbour, visited, rec_stack):
                    return True
            elif rec_stack[neighbour]:
                return True

        # The node needs to be popped from
        # recursion stack before function ends
        rec_stack[v] = False
        return False

    def is_cyclic(self):
        vert_count = len(self.vertices())
        visited = [False] * (vert_count + 1)
        rec_stack = [False] * (vert_count + 1)
        for vert in range(vert_count):
            if not visited[vert]:
                if self._is_cyclic_impl(vert, visited, rec_stack):
                    return True
        return False


