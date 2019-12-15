from operator import attrgetter

from libaoc.algo import CostAStarSearch
from aoc_2015.day_22 import make_initial, _State, SETTINGS

def test_hard_mode():
    SETTINGS.DEBUG = False
    ini = make_initial(50, 500, 51, 9, hard=True)
    search = CostAStarSearch(ini, attrgetter('won'), _State.successors)
    result = search.search()
    assert result.cost < 1242
