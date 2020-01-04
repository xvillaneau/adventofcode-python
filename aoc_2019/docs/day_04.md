# Advent of Code 2019, day 3

https://adventofcode.com/2019/day/4

## Part 1

In this problem, we are asked to count how many numbers within a given range verify certain properties. This is typically the genre of puzzle where I will directly try to implement an over-complicated solution that takes me hours to get working. Let's not do that (yet).

The most straightforward way to approach this problem is to go through _all_ the numbers in the input range, and check each one. Therefore, the core of our solution will be a function that takes a number as input and outputs whether it verifies the required properties.

### Splitting the digits

We will need one extra tool before that; since the problem operates on the individual digits of our number, it is likely most convenient to work on a list of said digits instead of the full number.

Python already provides us with a base 10 representation of numbers when printed as strings. We can use that to extract the digits:

```python
def to_digits(number):
    digits = str(number)
    return [int(digit) for digit in digits]
```

Alternatively, we can do some maths. The modulo of a number by 10 is its rightmost digit, so progressively taking that digit then dividing (integrally) the number by 10 gets us to the same result, although it requires the digits to be reversed at the end. This is slightly faster, and can be adapted to bases other than 10:

```python
def to_digits(number):
    digits = []
    while number:
        digits.append(number % 10)
        number //= 10
    return digits[::-1]
```

### The core logic

As a reminder, our passwords must fullfill these two properties:

1. the digits are in increasing order (left to right),
2. there's the same digit twice in a row at least once.

This can be checked by comparing each pair of consecutive digits in the number:

1. if the right digit is smaller than the left, then the number is invalid,
2. if both digits are equal, then we have found a pair (but we cannot conclude that the number is valid).

Because we need to work with pairs of digits, the start of the loop requires some special attention. If we looped on all digits, then there would be no previous digit to compare the first digit to. One way to solve this is to put the first digit aside as the "previous" one, and start the loop from the second digit:

```python
def check_password(number):
    digits = to_digits(number)
    previous = digits[0]
    for digit in digits[1:]:
        ...  # Logic
        previous = digit
```

Another approach is to use Python's `zip` built-in over the list of digits and an offset copy of itself. When applied to two iterators, `zip` will yield pairs of elements from both. The implementation is:

```python
def check_password(number):
    digits = to_digits(number)
    for left, right in zip(digits, digits[1:]):
        ...  # Logic
```

The second solution would be considered more "Pythonic", and is more concise. In this particular case though, the first implementation runs slightly faster. So pick the structure you prefer (but keep in mind that premature optimization is the root of all evil).

For the first check, finding any right digit smaller than the previous results in immediate elimination of the number. Since we're in a function, we can use `return False` to break out of the loop and the function at once:

```python
def check_password(number):
    digits = to_digits(number)
    for left, right in zip(digits, digits[1:]):
        if left > right:
            return False
        ...  # More logic
```

If we reach the end of the loop, that must mean all digits are in order. So the only test check to perform is whether there is a repeated digit in the number. Since there already is a loop over the pairs of digits, we might as well run that test at the same time:

```python
def check_password(number):
    has_pair = False
    digits = to_digits(number)
    for left, right in zip(digits, digits[1:]):
        if left > right:
            return False
        if left == right:
            has_pair = True
    return has_pair
```

### Counting the passwords

With this, the password check is fully implemented! We can now solve part 1:

```python
def part_1(start, stop):
    valid_codes = 0
    for code in range(start, stop + 1):
        if check_password(code):
            valid_codes += 1
    return valid_codes
```

This can be simplified a lot, because Booleans in Pythons _are_ numbers! In fact, `True` is equal to `1` and `False` is equal to `0`. And since we are summing numbers, this loop can be replaced with a `sum` expression:

```python
def part_1(start, stop):
    return sum(check_password(code) for code in range(start, stop + 1))
```