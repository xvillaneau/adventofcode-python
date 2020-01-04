# Advent of Code 2019, day 4

https://adventofcode.com/2019/day/4

- [Part 1](#part-1)
- [Part 2](#part-2)
- [My Solution](#my-solution)

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
2. there is the same digit twice in a row at least once.

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
        elif left == right:
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

## Part 2

The idea for part 2 is generally the same as part 1, but now only _strict_ pairs of digits are accepted. In other words, having a digit three or more times in a row bars it from counting as a pair. The increasing digits order condition from before is still in effect.

This significantly complicates the pair checking logic. We can no longer mark the pair condition as fullfilled the moment a digit repeat; instead we need to track how many times the digit repeats until and only consider a pair detected if that count was two.

Let's modify our loop by adding a `streak` variable counting how many times in a row the current left digit has occurred:

```python
def check_password_2(number):
    has_strict_pair = False
    streak = 1

    digits = to_digits(number)
    for left, right in zip(digits, digits[1:]):
        if left > right:
            return False
        elif left == right:
            streak += 1
        else:  # left < right
            if streak == 2:
                has_strict_pair = True
            streak = 1
    ...
```

This code does not work quite yet though. If the only strict pair is in the last two digits, then the number will not pass the test. Try walking through the code above with `11` as input to see for yourself. One way to work around this is to check `streak` one last time after the loop ends:

```python
def check_password_2(number):
    has_strict_pair = False
    streak = 1

    digits = to_digits(number)
    for left, right in zip(digits, digits[1:]):
        if left > right:
            return False
        elif left == right:
            streak += 1
        else:  # left < right
            if streak == 2:
                has_strict_pair = True
            streak = 1

    if streak == 2:
        has_strict_pair = True

    return has_strict_pair
```

[Here is the full implementation of both parts](../src/aoc_2019_simple/day_04.py). You can run it with:

    ./run_aoc.py 2019 4 simple

You will notice in there a bit of code that I have not talked about. The `parse_input_range` function's role is to convert the range input from a string like `"138241-674034"` to the `start` and `stop` arguments as integers. It is not essential to solving the problem.

Finally, if you think looping through the numbers twice is wasteful then you are not alone! It is possible (and relatively easy, give it a try!) to combine the logic for both parts into one loop, halving the run time of the code. We can do much better though…

## My Solution

[Here is my approach to solving the puzzle](../src/aoc_2019/day_04.py). You can run it with:

    ./run_aoc.py 2019 4

This solution was built from the observation that the ordering constraint on the digits is _very_ discriminating. On my input range, more than 99.5% of the tested numbers do not meet that condition! 

This means that our `sum(... for code in range(...))` is looping over _many_ numbers that could be ignored much earlier. For example, of all numbers between 900,000 and 999,999 only one is in the correct order (999,999). Yet our loop will test all 10,000 numbers in that range.

So this approach builds the possible codes gradually, starting with the right digit. More significant digits are then added one by one, but only picked from the digits allowed by the ordering constraint. For example, if the number I have built so far is `578`, then I only need to consider the digits from 0 to 5 at the next step. In this case, it saves me from exploring 400 invalid codes without processing a single one of them!

I decided to implement my solution recursively. This means that the function in charge of adding a digit to the code calls itself to add the next digits. And once it reaches 6 digits, the final correctness checks are made before counting the code as valid.

The implementation details of this are a little opaque. Instead of splitting the code into its digits, I keep it as a single number at all times. My recursion also tracks how many digits have been added so far using `magnitude`, which is the power of ten corresponding to the current layer (100,000 being the last). Doing so simplifies the math a little. Otherwise, the logic for the other checks (pairs, strict pairs, streak…) is roughly the same but adapted to the recursive implementation.

While we are here, I would like to point your attention to the use of `yield from` and `yield` in the recursive inner functions. These are not just recursive functions, they are recursive _generators_! I think those work astonishingly well with "wide" recursive algorithms. Recursion has a bad reputation in Python but I think that is not always justified. It is a very powerful tool, although a potentially dangerous one. It is worth understanding when to and not to use it.

In the end, all this complexity pays off! The simple solution runs in 1.1 seconds on my laptop (without the combined loops optimization), and my solution runs in between 3 ms and 5 ms. That's 200× to 300× faster! I am quite happy with that.
