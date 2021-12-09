from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional

D = TypeVar("D")
V = TypeVar("V")


class Constraint(Generic[V, D], ABC):
    def __init__(self, variables: list[V]):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment: dict[V, D]) -> bool:
        pass


class Solver(Generic[V, D]):
    def __init__(self, variables: list[V], domains: dict[V, list[D]]):
        assert all(v in domains for v in variables)
        self.variables = variables
        self.domains = domains
        self.constraints: dict[V, list[Constraint[V, D]]] = {}
        for v in variables:
            self.constraints[v] = []

    def add_constraint(self, constraint: Constraint[V, D]):
        assert all(v in self.domains for v in constraint.variables)
        for var in constraint.variables:
            self.constraints[var].append(constraint)

    def consistent(self, variable: V, assignment: dict[V, D]):
        return all(
            c.satisfied(assignment) for c in self.constraints[variable]
        )

    def solve(self, assignment: dict[V, D] = None) -> Optional[dict[V, D]]:
        assignment = assignment or {}
        if len(assignment) == len(self.variables):
            return assignment

        unassigned = [v for v in self.variables if v not in assignment]
        var = unassigned[0]
        for value in self.domains[var]:
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(var, new_assignment):
                if (result := self.solve(new_assignment)) is not None:
                    return result

        return None


class UniqueConstraint(Constraint[V, D]):

    def satisfied(self, assignment: dict[V, D]) -> bool:
        seen = set()
        for value in assignment.values():
            if value in seen:
                return False
            seen.add(value)
        return True
