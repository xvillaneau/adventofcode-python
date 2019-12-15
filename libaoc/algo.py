from abc import ABC, abstractmethod
from collections import deque
from heapq import heappop, heappush
from typing import TypeVar, Callable, Set, Generic, Optional, List, Dict, Deque, Tuple

S = TypeVar("S")


def least_steps(initial: S, update: Callable[[S], Set[S]], is_final: Callable[[S], bool],
                distance_func: Callable[[S], float] = None):

    border = {initial: 0}
    visited = set([])
    not_final = object()

    while border:
        final_state = next((s for s in border if is_final(s)), not_final)
        if final_state is not not_final:
            result = border[final_state]
            break

        cur_state = min(border, key=(distance_func if distance_func else border.__getitem__))
        cur_steps = border.pop(cur_state)
        visited.add(cur_state)
        print(cur_state)
        next_states = update(cur_state) - visited - set(border)
        border.update({s: cur_steps + 1 for s in next_states})

    else:
        raise StopIteration("Couldn't find the final state")

    return result


def least_steps_both_ends(initial: S, final: S, update: Callable[[S], Set[S]]):
    border_ini, visited_ini, steps_ini = {initial: 0}, set(()), 0
    border_end, visited_end, steps_end = {final: 0}, set(()), 0
    visited_ini = set([])

    while border_ini and border_end:

        intersect = set(border_ini) & set(border_end)
        if intersect:
            return min(border_ini[s] + border_end[s] for s in intersect)

        try:
            ini_state = next(s for s, n in border_ini.items() if n == steps_ini)
        except StopIteration:
            steps_ini += 1
            print(steps_ini + steps_end)
            continue

        ini_steps = border_ini.pop(ini_state)
        visited_ini.add(ini_state)
        next_ini = update(ini_state) - visited_ini - set(border_ini)
        border_ini.update({s: ini_steps + 1 for s in next_ini})

        intersect = set(border_ini) & set(border_end)
        if intersect:
            return min(border_ini[s] + border_end[s] for s in intersect)

        try:
            end_state = next(s for s, n in border_end.items() if n == steps_end)
        except StopIteration:
            steps_end += 1
            print(steps_ini + steps_end)
            continue

        end_steps = border_end.pop(end_state)
        visited_end.add(end_state)
        next_end = update(end_state) - visited_end - set(border_end)
        border_end.update({s: end_steps + 1 for s in next_end})

    raise StopIteration("Couldn't find the final state")


T = TypeVar('T')


class Node(Generic[T]):

    def __init__(
        self, state: T, parent: Optional['Node'], cost: float = 0.0, heuristic: float = 0.0
    ):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic

    def __repr__(self):
        return f"<Node cost={self.cost} heuristic={self.heuristic} state={self.state!r}>"

    def __lt__(self, other: 'Node'):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

    def path(self) -> List[T]:
        node = self
        path = [node.state]
        while node.parent is not None:
            node = node.parent
            path.append(node.state)
        path.reverse()
        return path


class SearchABC(Generic[T], ABC):
    frontier = ()

    def __init__(
        self, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]],
    ):
        self.goal_test = goal_test
        self.successors = successors
        self.explored: Set[T] = set()

    @abstractmethod
    def frontier_add(self, node: Node[T]):
        pass

    @abstractmethod
    def frontier_pop(self) -> Node[T]:
        pass

    def check_child(self, child: T, current_node: Node[T]) -> Optional[Node[T]]:
        if child in self.explored:
            return None
        self.explored.add(child)
        return Node(child, current_node)

    def search(self) -> Optional[Node[T]]:
        while self.frontier:
            current_node = self.frontier_pop()
            current_state = current_node.state

            if self.goal_test(current_state):
                return current_node

            for child in self.successors(current_state):
                next_node = self.check_child(child, current_node)
                if next_node is not None:
                    self.frontier_add(next_node)

        return None


class DFSearch(SearchABC):
    def __init__(
        self, initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]],
    ):
        super().__init__(goal_test, successors)
        self.frontier: List[Node[T]] = [Node(initial, None)]
        self.explored: Set[T] = {initial}

    def frontier_add(self, node: Node[T]):
        self.frontier.append(node)

    def frontier_pop(self) -> Node[T]:
        return self.frontier.pop()


class BFSearch(SearchABC):
    def __init__(
        self, initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]],
    ):
        super().__init__(goal_test, successors)
        self.frontier: Deque[Node[T]] = deque([Node(initial, None)])
        self.explored: Set[T] = {initial}

    def frontier_add(self, node: Node[T]):
        self.frontier.append(node)

    def frontier_pop(self) -> Node[T]:
        return self.frontier.popleft()


class AStarSearch(SearchABC):
    def __init__(
        self,
        initial: T,
        goal_test: Callable[[T], bool],
        successors: Callable[[T], List[T]],
        heuristic: Callable[[T], float],
    ):
        super().__init__(goal_test, successors)
        self.heuristic = heuristic
        self.frontier: List[Node[T]] = [Node(initial, None, heuristic(initial))]
        self.explored: Dict[T, float] = {initial: 0.0}

    def frontier_add(self, node: Node[T]):
        heappush(self.frontier, node)

    def frontier_pop(self) -> Node[T]:
        return heappop(self.frontier)

    def check_child(self, child: T, current_node: Node[T]) -> Optional[Node[T]]:
        new_cost = current_node.cost + 1.0
        if child in self.explored and self.explored[child] <= new_cost:
            return None
        self.explored[child] = new_cost
        heuristic = self.heuristic(child)
        return Node(child, current_node, new_cost, heuristic)


class CostAStarSearch(SearchABC):
    def __init__(
        self,
        initial: T,
        goal_test: Callable[[T], bool],
        successors: Callable[[T], List[Tuple[T, float]]],
    ):
        super().__init__(goal_test, successors)
        self.frontier: List[Node[T]] = [Node(initial, None, 0.0)]
        self.explored: Dict[T, float] = {initial: 0.0}

    def frontier_add(self, node: Node[T]):
        heappush(self.frontier, node)

    def frontier_pop(self) -> Node[T]:
        return heappop(self.frontier)

    def search(self) -> Optional[Node[T]]:
        while self.frontier:
            current_node = self.frontier_pop()
            current_state = current_node.state

            if self.goal_test(current_state):
                return current_node

            for child, cost in self.successors(current_state):
                new_cost = current_node.cost + cost
                if child in self.explored and self.explored[child] <= new_cost:
                    continue
                self.explored[child] = new_cost
                self.frontier_add(Node(child, current_node, new_cost))

        return None


class HighestCostSearch(Generic[T]):
    def __init__(
        self,
        initial: T,
        goal_test: Callable[[T], bool],
        successors: Callable[[T], List[T]],
    ):
        self.goal_test = goal_test
        self.successors = successors
        self.frontier: List[Node[T]] = [Node(initial, None, 0.0)]
        self.explored: Dict[T, float] = {initial: 0.0}

    def search(self):
        highest = None
        while self.frontier:
            current_node = self.frontier.pop()
            current_state = current_node.state

            if self.goal_test(current_state):
                if highest is None or current_node.cost > highest.cost:
                    highest = current_node
                continue

            new_cost = current_node.cost + 1.0
            for child in self.successors(current_state):
                if child in self.explored and self.explored[child] >= new_cost:
                    continue
                self.explored[child] = new_cost
                self.frontier.append(Node(child, current_node, new_cost))

        return highest


def sorted_search(sorted_list: List[T], elem: T):
    a, b = 0, len(sorted_list) - 1
    while a <= b:
        pivot = (a + b) // 2
        p_val = sorted_list[pivot]
        if p_val == elem:
            return True
        elif p_val > elem:
            b = pivot - 1
        else:
            a = pivot + 1
    return False
