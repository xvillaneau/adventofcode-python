from aoc_2020.day_19 import Rule8, StrRule, count_full_matches, parse_input

EXAMPLE_1 = """
0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"

aab
aba
""".strip()

EXAMPLE_2 = """
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
""".strip()

A, B = StrRule("a"), StrRule("b")


def test_parse_input_1():
    rules, messages = parse_input(EXAMPLE_1)
    assert rules == A + (A + B | B + A)
    assert messages == ["aab", "aba"]


def test_parse_input_2():
    rules, messages = parse_input(EXAMPLE_2)
    r3 = A + B | B + A
    r2 = A + A | B + B
    r1 = r2 + r3 | r3 + r2
    assert rules == A + r1 + B


def test_match_1():
    rules, _ = parse_input(EXAMPLE_1)
    assert list(rules.matches("aab")) == [3]
    assert list(rules.matches("aabaaa")) == [3]
    assert list(rules.matches("abaa")) == [3]
    assert list(rules.matches("bbaa")) == []
    assert list(rules.matches("aa")) == []


def test_count_matches():
    rules, messages = parse_input(EXAMPLE_2)
    assert count_full_matches(rules, messages) == 2


EXAMPLE_3 = """
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
""".strip()


def test_rule_8():
    r8 = Rule8(A)
    assert list(r8.matches('a')) == [1]
    assert set(r8.matches('aa')) == {1, 2}
    assert set(r8.matches('aaa')) == {1, 2, 3}

    r8 = Rule8(A + B | B + A)
    assert set(r8.matches('a')) == set()
    assert set(r8.matches('abbabb')) == {2, 4}


def test_with_loops():
    assert count_full_matches(*parse_input(EXAMPLE_3)) == 3

    rule, messages = parse_input(EXAMPLE_3, with_loops=True)
    assert 30 in list(rule.matches("babbbbaabbbbbabbbbbbaabaaabaaa"))
    assert count_full_matches(rule, messages) == 12
