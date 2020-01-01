# Advent of Code 2019, day 1

https://adventofcode.com/2019/day/1

* [Part 1](#part-1)
* [Part 2](#part-2)
* [Implementations](#implementations)

This is the first puzzle of the 2019 edition of Advent of Code. As per tradition, it's a relatively simple puzzle that's accessible to new programmers in look for a challenge. So I will be going a little deeper into the details this time.

## Part 1

### The maths

The first part involves:

1. take an input number,
2. divide it by three,
3. round down the result,
4. subtract two from the result.

This can be done in Python with:

```python
def fuel_required(mass):
    return (mass // 3) - 2
```

This seems to work as expected based on the examples:

```python
>>> fuel_required(14)
2
>>> fuel_required(1969)
654
>>> fuel_required(100756)
33583
```

The `//` operator here is the integral division, as opposed to `/` which is the floating-point division:

```python
>>> 3 // 2
1
>>> 3 / 2
1.5
```

We need to round down the result, so the integral division is ideal since it does that for us. Other programming languages may not have that feature built-in, in which case the common solution is to use a maths library. For example in JavaScript:

```js
fuel = Math.floor(mass / 3) - 2
```

**Extra note:** Integral division also rounds down the result when dealing a negative factor. While this doesn't apply here, you might want to keep this in mind.

### Reading the data

The second challenge for beginners here will be to read the puzzle input file. It is a plain-text list of 100 numbers with one number per line. Here's a working (and relatively safe) solution:

```python
def read_input_data(filename):
    """Read the list of module masses"""
    data = []
    with open(filename, "r") as file:
        for line in file:  # Iterating over a file object yields its lines
            line = line.strip()  # Removes the trailing \n if present
            if line:  # Check that the line is not empty
                data.append(int(line))  # Convert the line into a number
    return data
```

There are ways to shorten the code above, but this implementation should safely handle cases where your list of numbers is terminated by one of more blank lines.

**Note:** The `int` constructor will safely ignore blank spaces around a number, but will raise an error if called on something that's not a number:

```python
>>> int("1234")
1234
>>> int("\t1234  \n")
1234
>>> int("")
ValueError: invalid literal for int() with base 10: ''
```

Alternatively, data science libraries like [Pandas](https://pandas.pydata.org/) have [built-in tools](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html) to read numeric data from files.

**Note:** I strongly recommend building your own library to read and parse simple files and keep it around for Advent of Code! Many puzzles will take this kind of input.

### Running the whole thing

Now that we are able to read a list of numbers and compute the fuel required to launch a given mass, we can assemble the bits together and solve the puzzle!

Assuming you saved your input file as `aoc_2019_day_01_data.txt`, you can run this:
```python
>>> data = read_input_data("aoc_2019_day_01_data.txt")
>>> total_fuel = 0
>>> for mass in data:
...     total_fuel += fuel_required(mass)
...
>>> total_fuel  # Will be your answer, not necessarily that
123456789
```

Since we're adding numbers together, a more elegant way would be:
```python
total_fuel = sum(fuel_required(mass) for mass in data)
```

## Part 2

If you are new to Advent of Code, welcome to your first "part two"! This second half of the issue is always hidden until you solve (and submit your solution to) part one. Typically, part two introduces new details that take the problem a little further. If you're lucky, you might be able to re-use most of your code from part 1! If not, you might be in for a wild ride of re-factoring and optimization…

Here we are introduced to the harsh reality that fuel is heavy. Rockets (and planes) have to take extra fuel on board for the sole purpose of flying the fuel itself. The good news is that this extra fuel uses the same calculation as before, applied as many times as necessary until the result is zero or negative.

Here is an implementation using a loop:

```python
def total_fuel_required(mass):
    """Total amount of fuel needed to fly a module"""
    total_fuel = 0
    fuel = fuel_required(mass)  # Fuel for flying the module mass
    while fuel > 0:  # Check if we're done
        total_fuel += fuel  # Add the current result to the total
        fuel = fuel_required(fuel)  # Compute the fuel needed to fly that fuel
    return total_fuel
```

You may have noticed that I did not re-write the fuel calculation explicitly. This is an example of code modularity put to good use! By making the part 1 solution into its own function, we are able to re-use it in part 2 without having to repeat ourselves. And if this was "real" code, then only one part of the code would need to be modified if we ever wanted to compute the fuel differently.

Similarly to what we did in part 1, this function can then be applied to each line in the input to get the total fuel required

## Implementations

### Simple implementation

[Here is a full Python implementation to solve this puzzle](../src/aoc_2019_standalone/day_01.py). You can run it with:

    ./run_aoc.py 2019 1 standalone

It is a composition of all the code discussed previously, with each chunk made into its own function. The main differences with all the code we previously discussed are:
1. The `read_input_data` function no longer takes a file name as input but the file contents directly. That's because my custom Advent of Code framework takes care of finding the data and reading it.
2. There is a `main` function is where all the logic is wired together. You may not be familiar with the `yield` keyword I'm using, but don't worry too much about it. The idea is that the first `yield` sends the answer for the first part back the caller, and the second sends the one for the second part.
3. The `if __name__ == "__main__"` section at the end allows the `main` to run if the file is executed directly. In this particular case, this structure allows you to test the script directly (without going through my custom runner) by calling it with `python` and specifying the path to the data file as a positional argument. Using the runner is easier though. I will be keeping those "main" sections in the examples for clarity.

### My implementation

_Note:_ My "own" solutions use custom internal libraries for common Advent of Code solving, as well as some magic convenience tools to run the problem. I would also not consider this code "good practice".

[Here is my own "final" implementation](../src/aoc_2019/day_01.py). You can run this solution with:

    ./run_aoc.py 2019 1

This is roughly the same approach, with a few cosmetic differences. Generally speaking, I've made the code more concise (and less modular, which is arguably a bad practice). I'm also using my own tools to parse the input file.

The part 2 calculation is a quite different: instead of calculating the total fuel for each module and summing them separately, I sum the fuel weights in one pass. But what's likely most confusing here are the mechanics around the `fuel` variable in the loop:

```python
total_fuel = 0
for fuel in numbers:
    while (fuel := fuel // 3 - 2) > 0:
        total_fuel += fuel
```

I am using an assignment expression (`:=`) to set the fuel to its next value in the `while` loop. This is a relatively new Python 3.8 feature so it is normal if you are not familiar with it. The way it works is as follows:

1. The outer `for` loop goes through the values in `numbers` (a list of integers). So at the start of every iteration, `fuel` holds the weight of a module. Let's say for example that `fuel` is set to 1969.
2. We are now inside the outer loop and reach the test for the inner loop. First the right side of the assignment expression (`fuel // 3 - 2`) is evaluated using the current value of `fuel`, so the result is 654.
3. `fuel` is reassigned to that value, _and_ the value is returned to the outer expression.
4. The inner `while` loop tests against the new evaluated value. Here `654 > 0` is true so the loop runs.
5. `total_fuel` is incremented by the new value `fuel` is assigned to, so 654.
6. Back the the `while` line, operations from step 2. are repeated.
7. The loop runs with the consecutive values of `fuel` (216, 70, 21, 5) and eventually reaches a terminating value (here `5 // 3 - 2 == -1`). The `while` loop is exited.
8. We go back to the outer `for` which assigns the next value in `numbers` to `fuel`, and the entire cycle repeats.

Note that the parenthesis in the `while` line are important. Writing `fuel := fuel // 3 - 2 > 0` is syntaxically correct but evaluates all of `fuel // 3 - 2 > 0` and would set `fuel` to `True` or `False`. 

This saves a couple lines of code, and is somehow slightly faster. I also think this is a specific case where an assignment expression is appropriate and feels more elegant than writing the reassignment separately. But that's only my opinion, that tool is frowned upon by some in the Python community.

This solution runs in 100 μs on my laptop, compared to 200 μs for the example solution. Which is arguably not worth the loss of modularity and readability. I also had an [other solution](https://github.com/xvillaneau/adventofcode-python/blob/4bae9bb4bbd8a14d62a51071a0461cbf5e63cb79/aoc_2019/src/aoc_2019/day_01.py) where I tried to be clever by using generator functions, but it was much slower and had no benefit over using a loop.
