
from functools import partial, reduce
from operator import and_, or_


def get_groups(groups):
    group = []
    for line in groups:
        if not line:
            yield group
            group = []
            continue
        group.append(line)
    yield group


def group_answers(op, data):
    def reduce_group(grp):
        return ''.join(sorted(reduce(op, (set(s) for s in grp))))

    return list(map(reduce_group, get_groups(data)))


group_any_answer = partial(group_answers, or_)
group_all_answers = partial(group_answers, and_)


def main(data: str):
    data = data.splitlines()
    yield sum(len(ans) for ans in group_any_answer(data))
    yield sum(len(ans) for ans in group_all_answers(data))
