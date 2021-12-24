from libaoc.algo import CostAStarSearch

COST = {"A": 1, "B": 10, "C": 100, "D": 1000}
ROOMS = {"A": 2, "B": 4, "C": 6, "D": 8}
ENTRANCES = {i: c for c, i in ROOMS.items()}

State = tuple[str, str, str, str, str, str, str, str, str, str, str]


def load_init(data: str, part_2=False) -> State:
    init = [c for c in data if c in ROOMS]
    state: list = [""] * 11
    state[2] = init[4] + "DD" * part_2 + init[0]
    state[4] = init[5] + "BC" * part_2 + init[1]
    state[6] = init[6] + "AB" * part_2 + init[2]
    state[8] = init[7] + "CA" * part_2 + init[3]
    return tuple(state)


def _traverse(state: State, indices):
    indices = iter(indices)
    i = next(indices)
    room = state[i]
    val = room[-1:]

    for j in indices:
        elem = state[j]
        if j in ENTRANCES:
            # Move shell directly to the other room if possible
            if val and ROOMS[val] == j and all(x == val for x in elem):
                yield (val, i, j)
        elif not elem:
            # Can move shell in the hallway
            if val:
                yield (val, i, j)
        else:
            # Found shell in the hallway, move them into this room if
            # possible then stop searching (hallway is blocked)
            if ROOMS[elem] == i and all(x == elem for x in room):
                yield (elem, j, i)
            return


def candidate_moves(state: State):
    for i in ENTRANCES:
        yield from _traverse(state, range(i, -1, -1))
        yield from _traverse(state, range(i, 11))


def apply_move(state: State, value, source, dest, size=2) -> tuple[State, int]:
    state = list(state)
    dist = abs(dest - source)

    if source in ENTRANCES:
        room = state[source]
        dist += 1 + size - len(room)
        state[source] = room[:-1]
    else:
        state[source] = ""
    if dest in ENTRANCES:
        dist += size - len(state[dest])
        state[dest] += value
    else:
        state[dest] = value
    return tuple(state), dist * COST[value]


def smallest_cost(data, part_2=False):
    initial_state = load_init(data, part_2)
    n = 4 if part_2 else 2
    final = ("", "", "A" * n, "", "B" * n, "", "C" * n, "", "D" * n, "", "")

    def next_states(state):
        return [
            apply_move(state, *mov, size=n)
            for mov in candidate_moves(state)
        ]

    search = CostAStarSearch(initial_state, (lambda s: s == final), next_states)
    results = search.search()
    return results.cost


def main(data: str):
    yield smallest_cost(data)
    yield smallest_cost(data, part_2=True)
