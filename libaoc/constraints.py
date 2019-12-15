from abc import ABC, abstractmethod
from itertools import count
from typing import Generic, TypeVar, Dict, List, Optional

V = TypeVar("V")
D = TypeVar("D")


class Constraint(Generic[V, D], ABC):
    def __init__(self, variables: List[V]):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]):
        pass


class IntegralCSP(Generic[V]):
    def __init__(self, variables: List[V]):
        self.variables = variables
        self.constraints: Dict[V, List[Constraint[V, int]]] = {}
        for variable in self.variables:
            self.constraints[variable] = []

    def add_constraint(self, constraint: Constraint[V, int]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError(
                    f"Variable {variable!r} in constraint {constraint!r} not in CSP"
                )
            self.constraints[variable].append(constraint)

    def consistent(self, variable: V, assignment: Dict[V, int]) -> bool:
        return all(
            constraint.satisfied(assignment)
            for constraint in self.constraints[variable]
        )

    def backtracking_search(
        self, assignment: Dict[V, int] = None
    ) -> Optional[Dict[V, int]]:
        _assign: Dict[V, int] = (assignment or {}).copy()

        try:
            first = next(v for v in self.variables if v not in _assign)
        except StopIteration:
            return _assign

        for value in count():
            _assign[first] = value
            if self.consistent(first, _assign):
                return self.backtracking_search(_assign)
