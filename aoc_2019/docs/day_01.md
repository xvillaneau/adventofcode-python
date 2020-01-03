# Advent of Code 2019, day 1

https://adventofcode.com/2019/day/1

* [Part 1](#part-1)
* [Part 2](#part-2)
* [My Solution](#my-solution)

This is the first puzzle of the 2019 edition of Advent of Code. As per tradition, it's a relatively simple puzzle that's accessible to new programmers in look for a challenge. So I will be going a little deeper into the details this time.

## Part 1

### The maths

The first part involves:

1. take an input number,
2. divide it by three,
3. round down the result,
4. subtract two from the result,
5. apply this to all entries in our input,
6. sum all the results together.

Let's start with the division. In Python, you can divide numbers using the `/` operator. But this does not do what we want:

```python
>>> 4 / 2
2.0
>>> 3 / 2
1.5
>>> 14 / 3
4.666666666666667
```

That is because `/` is the "true" division which returns the approximated fraction as a floating point number. One way to round it down is to use the `floor` function from the `math` tools:

```python
>>> from math import floor
>>> floor(3 / 2)
1
>>> floor(14 / 3)
3
```

In some other languages (like Javascript), this would be the correct solution. But this is Python and there is a better way! Here are the results with different operator, `//`:

```python
>>> 4 // 2
2
>>> 3 // 2
1
>>> 14 // 3
4
```

The `//` operator is the "integral division" or the "floor division". It does precisely what we want in a single step (and it is more performant).

_Note_: If you are thinking "Wait, `3 / 2 == 1` used to work" that is because division in Python 2 behaved differently. Its behavior has been clarified in Python 3, for the better if you ask me. Also, at the time of writing this Python 2 has been deprecated since yesterday so it is about time to upgrade!

We can now write the fuel calculation. Let's write it as a function, so that we can re-use it later:

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

_Note_: You can also write `mass // 3 - 2` since the substraction operation has a [lower precedence](https://docs.python.org/3/reference/expressions.html#operator-precedence) than division. But leaving the parenthesis is perfectly fine if you think that is more readable.

### Reading the data

The second challenge for beginners here will be to read the puzzle input file. It is a plain-text list of 100 numbers with one number per line.

In my particular implementation of the Advent of Code solutions, I am using custom tooling that automatically takes care of reading the puzzle input file and passing its contents to the puzzle code. If you are working on Advent of Code without that then you will need to read the file first. File access is a vast topic that is out of the scope of what I want to teach, so here's how you do it:

```python
def read_input_data(filename):
    with open(filename, "r") as file:
        return file.read()
```

The data we are working with is provided as text. In this case, it will be a long string of digits with line breaks (`\n`) to separate numbers:

```python
>>> print("1\n23\n456")
1
23
456
```

Transforming this into usable input data for our problem will require two steps:
1. split the data into lines,
2. convert each line (a string of digits) into an actual number.

The first step can be done using the `.splitlines()` method of the string object:

```python
>>> string = "1\n23\n456"
>>> string.splitlines()
['1', '23', '456']
```

_Note_: `splitlines` will ignore the last `\n` if there is nothing after it, i.e. `"1\n23\n".splitlines() == ['1', '23']`. 

To convert a string of digits into a number, calling the `int` constructor does the job. It even works on numbers with whitespaces around them:

```python
>>> int("1234")
1234
>>> int("\t1234  \n")
1234
>>> int("a")
ValueError: invalid literal for int() with base 10: 'a'
```

Here is what the full code for reading the data looks like:

```python
def process_data(data):
    lines = data.splitlines()
    numbers = []
    for line in lines:
        number = int(line)
        numbers.append(number)
    return numbers
```

I have intentionally written this code to have each step on its own line, for demonstration purposes. More experienced Python developers will likely shorten this function using a list comprehension:

```python
def process_data(data):
    return [int(line) for line in data.splitlines()]
```

Both solutions work; pick the one that is the most readable for you. More readable code is **always** a good thing.

Alternatively, data science libraries like [Pandas](https://pandas.pydata.org/) have [built-in tools](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html) to read numeric data from files.

**Note:** I strongly recommend building your own library to read and parse common file formats and keep it around for Advent of Code! Many puzzles will take this kind of input.

### Running the whole thing

Now that we are able to read a list of numbers and compute the fuel required to launch a given mass, we can assemble the bits together and solve the puzzle!

This is a good time to write a function dedicated to the task, let's call it `part_1`. In this code, we will be using the functions we previously wrote. The only step left to go through all the numbers we parsed an add all the fuel consumptions together:

```python
def part_1(data):
    modules = process_data(data)
    total_fuel = 0
    for mass in modules:
        total_fuel += fuel_required(mass)
    print(total_fuel)
```

_Note_: I am assuming here that opening and reading the input file is done separately before calling `part_1`. 

Summing a sequence of numbers can generally be shortened using the `sum` built-in, if you prefer so:

```python
def part_1(data):
    modules = process_data(data)
    total_fuel = sum(fuel_required(mass) for mass in modules)
    print(total_fuel)
```

## Part 2

If you are new to Advent of Code, welcome to your first "part two"! This second half of the issue is always hidden until you solve (and submit your solution to) part one. Typically, part two introduces new details that take the problem a little further. If you are lucky, you might be able to re-use or adapt most of your code from part 1! If not, you could be in for a wild ride of re-factoring and optimization.

Here we are introduced to the harsh reality that fuel is heavy. Rockets (and planes) have to take extra fuel on board for the sole purpose of flying the fuel itself. The good news is that this extra fuel is calculated using the same method as before. What we need is a way to apply that calculation to its previous result repeatedly.

We cannot know in advance how many times we need to apply the calculation, but we do know when to stop it. This is great case for using a `while` loop. He is what the logic looks like:

1. We start like previously with the mass of our module; let's call it `mass`.
2. We apply the fuel calculation one first time on that mass; let's call the result `fuel`.
3. We also need to keep track of the total amount of fuel calculated so far; let's call that `total_fuel` and have it set to the value of `fuel` initially.
4. Now is where it becomes different. The fuel calculation is applied again, this time on `fuel`. We then replace `fuel` with that result.
5. If `fuel` is zero or negative, end the calculation.
6. Otherwise, add `fuel` to `total_fuel` and go back to step 4.

Here is this logic implemented:

```python
def total_fuel_required(mass):
    """Total amount of fuel needed to fly a module"""
    fuel = fuel_required(mass)
    total_fuel = fuel
    while True:
        fuel = fuel_required(fuel)
        if fuel <= 0:
            break
        total_fuel += fuel
    return total_fuel
```

We can also re-write this to have the end condition in the `while`, though this requires moving some bits around. In particular, we need to make sure that the test for `fuel > 0` is always before adding `fuel` to `total_fuel`:

```python
def total_fuel_required(mass):
    """Total amount of fuel needed to fly a module"""
    fuel = fuel_required(mass)
    total_fuel = 0
    while fuel > 0:
        total_fuel += fuel
        fuel = fuel_required(fuel)
    return total_fuel
```

You may have noticed that we did not re-write the fuel calculation explicitly. This is an example of code modularity: by putting the calculation into its own function in part 1, we are able to re-use it in part 2 without having to repeat ourselves.

The full implementation of part 2 is now very similar to that of part 1:

```python
def part_2(data):
    modules = process_data(data)
    total_fuel_2 = sum(total_fuel_required(mass) for mass in modules)
    print(total_fuel_2)
```

[Here is the full implementation of both parts](../src/aoc_2019_simple/day_01.py). You can run it with:

    ./run_aoc.py 2019 1 simple

The main differences with all the code we previously discussed are:

1. I've modified the `part_1` and `part_2` functions to return their result instead of printing it.
2. The `if __name__ == "__main__"` section at the end will only run the code in it if the script is executed directly. In this particular case, this structure allows you to test the script without going through my custom runner by calling it with `python` and specifying the path to the data file as a positional argument. For example (with fake answers):
   ```
   $ python aoc_2019/src/aoc_2019_simple/day_01.py aoc_2019/data/day_01.txt
   Aoc 2019, day 1, part 1: 123456789
   Aoc 2019, day 1, part 2: 987654321
   ```
   Using the runner is easier though. I will be keeping those "main" sections in the examples for clarity.

3. There is a `main` function that the `run_aoc.py` script depends on. Don't worry about it for now.

## My Solution

**DISCLAIMER**: My own solutions use custom internal libraries for common Advent of Code solving, and they sometimes cut corners in terms of readability and modularity. I would generally not consider this code "good practice".

[Here is my implementation](../src/aoc_2019/day_01.py). You can run this solution with:

    ./run_aoc.py 2019 1

This is roughly the same approach but much more concise (and less modular, which is arguably a bad practice). I'm also using my own tools to parse the input file.

The part 2 calculation is a quite different: instead of calculating the total fuel for each module and summing them separately, I sum the fuel weights in one pass. But the largest difference are the mechanics around the `fuel` variable in the loop:

```python
total_fuel = 0
for fuel in numbers:
    while (fuel := fuel // 3 - 2) > 0:
        total_fuel += fuel
```

I am using an assignment expression (`:=`) to set the fuel to its next value in the `while` loop. This is a relatively new Python 3.8 feature so it is normal if you are not familiar with it. The logic is the same as before but implemented differently.

Note that the parenthesis in the `while` line are important. Writing `fuel := fuel // 3 - 2 > 0` is syntaxically correct but evaluates all of `fuel // 3 - 2 > 0` and would set `fuel` to `True` or `False`. 

This saves a couple lines of code, and is somehow slightly faster. I also think this is a specific case where an assignment expression is appropriate and feels more elegant than writing the reassignment separately. But that is only my opinion; that language feature is frowned upon by some members of the Python community.

This solution runs in 100 μs (microseconds) on my laptop, compared to 250 μs for the example solution. Which is arguably not worth the loss of modularity and readability. I also had an [other solution](https://github.com/xvillaneau/adventofcode-python/blob/4bae9bb4bbd8a14d62a51071a0461cbf5e63cb79/aoc_2019/src/aoc_2019/day_01.py) where I tried to be clever by using generator functions, but it was much slower and had no benefit over using a loop.
