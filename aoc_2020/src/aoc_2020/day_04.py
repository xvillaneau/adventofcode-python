import re
from typing import List


def make_checks():
    def byr(value):
        return 1920 <= int(value) <= 2002

    def iyr(value):
        return 2010 <= int(value) <= 2020

    def eyr(value):
        return 2020 <= int(value) <= 2030

    def hgt(value):
        if not (match := re.match("^([0-9]+)(cm|in)$", value)):
            return False
        num, unit = match.groups()
        lo, hi = (59, 76) if unit == "in" else (150, 193)
        return lo <= int(num) <= hi

    def hcl(value):
        return re.match("^#[0-9a-f]{6}$", value) is not None

    def ecl(value):
        return value in COLORS

    def pid(value):
        return re.match("^[0-9]{9}$", value) is not None

    def cid(_):
        return True

    return locals()


COLORS = set("amb blu brn gry grn hzl oth".split())
FIELDS_CHECKS = make_checks()
FIELDS_EXPECTED = set(FIELDS_CHECKS) - {"cid"}


def parse_passports(batch_data: List[str]):
    passport = {}
    for line in batch_data:
        if not line:
            yield passport
            passport = {}
            continue
        for pair in line.split():
            field, _, value = pair.partition(":")
            passport[field] = value
    yield passport


def passport_has_fields(passport):
    return all(key in passport for key in FIELDS_EXPECTED)


def fields_are_valid(passport):
    return all(FIELDS_CHECKS[k](v) for k, v in passport.items())


def count_valid_passports(passports):
    fields_ok, values_ok = 0, 0
    for passport in passports:
        fields_ok += (has_fields := passport_has_fields(passport))
        values_ok += (has_fields and fields_are_valid(passport))
    return fields_ok, values_ok


def main(data: str):
    passports = parse_passports(data.splitlines())
    yield from count_valid_passports(passports)
