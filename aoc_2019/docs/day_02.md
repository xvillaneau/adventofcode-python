# Advent of Code 2019, day 2

https://adventofcode.com/2019/day/2

* [Part 1](#part-1)
* [Part 2](#part-2)
* [Implementations](#implementations)
* [Trivia](#trivia)

Today we are introduced to the cornerstone of the entire 2019 event: the Intcode computer! Nearly half this year's puzzles depend on it, so it is important to get it right. For now, we will only implementing a few basic features of this computer.

## Part 1

This part is pretty much the meat of today's puzzle since we need to implement a working basic computer. Let's walk through the description of the computer and parse the implementation details. I'll be adding comments detailing my train of thoughts as we go along.

> An Intcode program is a list of integers separated by commas (like 1,0,0,3,99).

The "separated by commas" information is telling us how to parse the input. It seems that our best bet is to model the program in Python as a list of integers.

> To run one, start by looking at the first integer (called position 0). Here, you will find an opcode - either 1, 2, or 99. The opcode indicates what to do; for example, 99 means that the program is finished and should immediately halt. Encountering an unknown opcode means something went wrong.

Secondly, we learn that we will be reading from that list at a given position and doing things depending on what number is there. The halting code could be implemented in different ways, we'll come back to it later. The easiest way to implemented could be an `if ... elif ... else` structure with one test per opcode and an exception at the end.

> Opcode 1 adds together numbers read from two positions and stores the result in a third position. The three integers immediately after the opcode tell you these three positions - the first two indicate the positions from which you should read the input values, and the third indicates the position at which the output should be stored. [...] Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them.

This is important. We learn that opcodes are followed by arguments (three in this case) which are _not_ opcodes but _addresses_ to read and write to. Since we decided to model our program as a list and positions start at zero, accessing a value in our code will be done with `code[position]`. We also learn that our program is not static and will modify its own code over time. Finally, we now know what all our currently known opcodes do.

> Once you're done processing an opcode, move to the next one by stepping forward 4 positions.

This is logical, since our operations take three arguments (so four positions including the code itself). The halting 99 code is an exception, but the program ends at that code so we can ignore it. It seems that this property may change in future implementations, if opcodes with fewer or more than three arguments are introduced.

Let's summarize. We need:
1. a function to convert a text with decimal numbers separated by commas into a list of integers;
2. a variable to keep track of which position we are looking at, starting with 0 and incremented by 4 after each step;
3. a conditional statement that decided whether to run addition or multiplication based on the opcode;
4. logic to read the arguments following the current position, read the first two values at the given addresses, and write the result at the third address;
5. a loop to run the computer, terminated in some way if the code 99 is reached.

### Reading the program

Here's my implementation of a function that handles the first point above:

```python
def parse_program(filename):
    with open(filename, "r") as file:
        return [int(num) for num in file.read().split(",")]
```

In this code, I'm using:
1. `file.read()` to get the entire contents of the file at once as a single string;
2. `.split()` (a method of `str`) to divide that string at all commas, turning it into a list of strings;
3. a list comprehension that takes each element from the split, converts it into an integer, and builds a list with all these numbers, all in a single line of code.

This is a little dense, but arguably as readable as:

```python
numbers = []
with open(filename, "r") as file:
    full_program = file.read()
    for num in full_program.split(","):
        numbers.append(int(num))
```

You can read more on list comprehensions at [Real Python's excellent tutorial](https://realpython.com/list-comprehension-python/).

### The computer itself

Let's write the computer now, step by step.

In this example, I have decided to implement the computer inside a function. The program is passed as a list of integers named `code`. Because we will be mutating (modifying) that code, the first thing we need to do is to create a copy of the input so that running the program does not have any unintended side-effects. 

_Note:_ This is not strictly necessary, but users our our function will likely not expect the list they passed to be modified. In general, functions that mutate their inputs are a bad practice in Python unless the context makes it clear that it is the intended behavior.

```python
def run_computer(code):
    memory = code.copy()
```

Now we need our position variable. Let's call it `pointer`.

```python
    pointer = 0
```

Then we need a loop. The easiest approach here is likely to loop forever and have code 99 break out of it from inside, which we'll implement next. The first step of that loop is always to read the current opcode.

```python
    while True:
        opcode = memory[pointer]
```

At this point, we can use that information to break out of the loop and terminate the computer.

```python
        if opcode == 99:
            break
```

Then, since both the other opcodes take three arguments, let's read them now.

```python
        arg_1 = memory[pointer + 1]
        arg_2 = memory[pointer + 2]
        arg_3 = memory[pointer + 3]
```

Now we can implement addition if the code is 1. Do not forget that the arguments we read are addresses.

```python
        if opcode == 1:
            memory[arg_3] = memory[arg_1] + memory[arg_2]
```

And we can do the same for multiplication.

```python
        elif opcode == 2:
            memory[arg_3] = memory[arg_1] * memory[arg_2]
```

If the opcode is something else, now is a good time to crash in a controlled way.

```python
        else:
            raise ValueError(f"Got unknown opcode {opcode}")
```

Let's end the loop by moving our pointer to the next instruction.

```python
        pointer += 4
```

Finally, we are out of the loop and the program will end (this place in the code is only reached after opcode 99). Since our memory was modified we need to return it, otherwise we will never know what the program did…

```python
    return memory
```

And we are done! Here is the fully-assembled code:

```python
def run_computer(code):
    memory = code.copy()
    pointer = 0
    while True:
        opcode = memory[pointer]
        if opcode == 99:
            break
        arg_1 = memory[pointer + 1]
        arg_2 = memory[pointer + 2]
        arg_3 = memory[pointer + 3]
        if opcode == 1:
            memory[arg_3] = memory[arg_1] + memory[arg_2]
        elif opcode == 2:
            memory[arg_3] = memory[arg_1] * memory[arg_2]
        else:
            raise ValueError(f"Got unknown opcode {opcode}")
        pointer += 4
    return memory
```

### Solving the puzzle

In this particular problem, we also need two specific steps:
1. write the noun and verb to addresses 1 and 2 respectively at the start,
2. read and return the value at address 0 at the end.

The better approach here is to re-use the function we just wrote:

```python
def gravity_assist(code, noun, verb):
    code[1], code[2] = noun, verb
    return run_computer(code)[0]
```

Note that this function mutates the code, but in our use case that's acceptable (and it saves us from copying the code twice). This is a fixable problem though.

Alternatively, we can modify the `run_computer` function to specifically fit our needs. Here's how that might look:

```python
def gravity_assist(code, noun, verb):
    memory = code.copy()
    memory[1], memory[2] = noun, verb

    pointer = 0
    while True:
        opcode = memory[pointer]
        if opcode == 99:
            return memory[0]
        arg_1, arg_2, arg_3 = memory[pointer + 1 : pointer + 4]
        if opcode == 1:
            memory[arg_3] = memory[arg_1] + memory[arg_2]
        elif opcode == 2:
            memory[arg_3] = memory[arg_1] * memory[arg_2]
        else:
            raise ValueError(f"Got unknown opcode {opcode}")
        pointer += 4
```

Here are the modifications I made:
1. Addresses 1 and 2 are initialized to the noun and verb values right after the input is copied. I did this using the "unpacking" syntax, which allows multiple assignments to be made in a single line.
2. The same was done for reading the arguments, but the other way around (unpacking three memory addresses into three variables). Note the end index `p + 4`, used here so that `p + 3` is included.
3. Since all that happen after breaking out of the loop was to end the program, `break` has been replaced by `return memory[0]`.

The code above is probably the easiest to write for this particular puzzle, but the problem description makes it clear that we will be re-using our intcode computer. We might as well keep it separate now.

## Part 2

In part 1, we were asked to run the program using the inputs `noun = 12` and `verb = 2`. Now, we are asked to run the program for many different inputs until we found the answer we wanted. This can be implemented using two nested loops:

```python
def find_input_values(code, result):
    for noun in range(100):
        for verb in range(100):
            if gravity_assist(code, noun, verb) == result:
                return noun * 100 + verb
```

At this point, our decision to write the code for part 1 inside functions helps us again. Also, our decision to not modify the code (not too much at least, only noun and verb are mutated) allows us to simplify the implementation.

Here's an alternative implementation using a generator expression, which I think is more readable (and I believe slightly faster):

```python
def find_input_values(code, target):
    """Find which input returns the given target. The hard way."""
    return next(
        noun * 100 + verb
        for noun in range(100)
        for verb in range(100)
        if gravity_assist(code, noun, verb) == target
    )
```

[Here is the full code](../src/aoc_2019_standalone/day_02.py) where everything we studied above is assembled together. You can run it with:

    ./run_aoc.py 2019 2 standalone

## Implementations

### Simple implementation

Just like day 1, a simple main that expects the path to the input file as argument was implemented. Otherwise the code is the same. 

Despite how heavy part 2 might seem (the intcode computer has to run thousands of times), this implementation easily runs under a second. The timings I get are around 50 ms.

### My implementation

[Here is my own "final" code for the puzzle](../src/aoc_2019/day_02.py). You can run this solution using:

    ./run_aoc.py 2019 2

Here are the notable differences. First, I am using my full implementation of the intcode computer, imported from [its own module](../src/aoc_2019/intcode.py) It is much more complicated than our code here; I will explain how it works later, once all the intcode concepts have been introduced. All you need to know here is that:

* The `CodeRunner` object is instantiated by passing the parsed code, and it initially does nothing.
* It has a `code` attribute that represents the current memory, which we use here to manually set our input.
* The `run_full()` method just runs the computer until the halt instruction is reached.

Secondly, my part 2 implementation uses a very different approach than the "brute" one. I have observed that the output (for the code I was given) was a linear combination of the inputs. In other words we can write `output = constant + dn * noun + dv * verb`, therefore by computing those constants we can predict our input values for a given output with only very few runs of the intcode computer (three exactly).

This approach is _much_ faster (around 100×) since we need only three runs instead of thousands. If the problem had been in a larger input space (say 10,000 x 10,000), the brute-force approach would have been impractical. In this particular case that's a little overkill, but I wouldn't settle for anything that ran over a millisecond…

The drawback of the approach is that it makes a lot of assumptions. Maybe I'll try to find input from other people and try it out.

## Trivia

This puzzle has several interesting Apollo program references.

The 1202 program alarm was raised when the scheduler of the Apollo Guidance Computer (AGC) overflowed. In practice, this (very roughly) meant that low-priority tasks were being dropped in favor of high-priority real-time jobs. This alarm famously occurred during the lunar landing of Apollo 11. 

The terms "noun" and "verb" are also AGC terminology. This was the system by which the Apollo crew interacted with the computer, where they would need to enter numbers to run commands, change the mission status, etc. In the case of Apollo 14, those commands were even used to directly modify bits in memory to save the mission.

Some related documents:
* [_Apollo 11's "1202 Alarm" Explained_](https://youtu.be/kGD0zEbiDPQ) (video) by Vintage Space.
* [_The Computer Hack That Saved Apollo 14_](https://youtu.be/wSSmNUl9Snw), a great video by Scott Manley on the details of how the noun/verb syntax was used to trick the AGC to not accidentally abort the landing.
* [A gentle introduction to the AGC](https://www.ibiblio.org/apollo/ForDummies.html) by Virtual AGC.