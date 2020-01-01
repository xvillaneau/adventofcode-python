# Advent of Code 2019, day 3

https://adventofcode.com/2019/day/3

Today's puzzle is a relatively classic early AoC puzzle, where we need to apply move instructions in 2D space.

## Part 1

As usual, the first step of the challenge is to transform our input into usable data. The simplest approach is often to split the raw data into a tuple, in this case tuples of one letter (U, L, D, R) and one number. For example:

```python
>>> data = "R8,U5,L5,D3"
>>> segments = []
>>> for move in data.split(","):
...     segment = move[0], int(move[1:])
...     segments.append(segment)
>>> segments
[('R', 8), ('U', 5), ('L', 5), ('D', 3)]
```

This can be written with a list comprehension as well:

```python
def parse_wire(data):
    return [(word[0], int(word[1:])) for word in data.split(",")]
```

Now we need a strategy to solve the problem. The simplest is most likely to:

1. compute the coordinates of every single point on each wire,
2. intersect the two sets of coordinates to get all the intersections,
3. find which of these intersections has the lowest distance to the origin.

The first step of this process is arguably the most complicated. A good approach is to process segment by segment using the last position of a segment as the start for the next.

Let's model a position by a `(x, y)` tuple of integers. We also need to pick an orientation convention for those coordinates. I will be using:
* Up: increasing y coordinates
* Right: increasing x coordinates
* Down: decreasing y coordinates
* Left: decreasing x coordinates

```
        U
        ↑
+y  L ← . → R
 ↑      ↓
 → +x   D
```

Depending on the direction and length of the segment, we can build a list of all points in that segment. For example, let's focus on the code for going right:

```python
x0, y0 = start_position
segment_path = [
    (x0 + x, y0)
    for x in range(1, segment_length + 1)
]
``` 

Say we start at `(0, 0)` and we are going right 4 times. Then `x` will be iterating over `range(1, 5)` which are the numbers from 1 to 4 included. The points in the segment will be: `(1, 0)`, `(2, 0)`, `(3, 0)`, and `(4, 0)`.

You may wonder why we aren't starting from 0. This has a double benifit:
1. If the starting point is the last point of the previous segment, then it has already been covered and we don't output it twice.
2. It conveniently excludes `(0, 0)` from the first segment, which is always an intersection that we need to ignore.

All that's left is to wire up that logic for all four directions:

```python
def segment_path(start, direction, moves):
    x0, y0 = start
    if direction == "U":  # Increase Y
        return [(x0, y0 + y) for y in range(1, moves + 1)]
    elif direction == "D":  # Decrease Y
        return [(x0, y0 - y) for y in range(1, moves + 1)]
    elif direction == "R":  # Increase X
        return [(x0 + x, y0) for x in range(1, moves + 1)]
    else:  # Going left, decrease X
        return [(x0 - x, y0) for x in range(1, moves + 1)]  
```

Now we need to run that process for all segments, starting at `(0, 0)`. Along the way, each point needs to be stored. And the last point of every segment has to be used as a start for the next. Here is a possible implementation:

```python
def compute_path(wire):
    path = set()
    start = (0, 0)

    for direction, moves in wire:
        for point in segment_path(start, direction, moves):
            path.add(point)
            start = point

    return path
```

This works by assigning each `point` to `start` after every step, so that `start` is assigned to the last point of the segment when the inner loop ends. That way, the next call of `segment_path` starts at the correct position.

We're also storing the positions in a set. Sets are different from lists in that they are unordered, do not allow duplicates, and can only store hashable objects. The upside is that membership testing (`a in b`) is extremely fast! Unlike lists where testing if one contains an element grows linearly in time with the list's size.

Because we are using sets, finding the intersections between the two paths is now a piece of cake:

```python
intersections = path_1 & path_2
```

The `&` operator stands for "binary and", but applied to sets it computes the intersection of two sets. In other words, it returns a new set with only the elements that are present in both input sets.

Finally, we need to isolate the closest point. We only need to know its distance, so we can compute all distances first and get the smallest value from there.

```python
answer = min(abs(x) + abs(y) for x, y in intersections)
```

We need to use `abs` here because points can have negative coordinates. Had we used `x + y`, a point like `(1, -1)` would have a computed distance of 0 when the correct value is 2.

Let's assemble all the code together to solve part 1:

```python
def main(data):
    # Input data has one wire per line
    raw_1, raw_2 = data.splitlines()
    path_1 = compute_path(parse_wire(raw_1))
    path_2 = compute_path(parse_wire(raw_2))
    intersections = path_1 & path_2
    return min(abs(x) + abs(y) for x, y in intersections)
```

## Part 2

Change of plans; the closest point is no good and we are to find the intersection reached in the fewest steps. Thankfully, we can add this functionality with very few changes.

Let's first think about our data structure. Using a set of points is no longer enough, we also need to store how many (fewest) steps it takes to reach each point. The best data structure for this is a dictionary with points as keys and steps as values. Points will still stored as a set (a set is more or less a dict without values and only keys) and we can store an unique value for each.

Here is the modified path computing:

```python
def compute_path(wire):
    path = {}
    steps = 1
    start = (0, 0)

    for direction, moves in wire:
        for point in segment_path(start, direction, moves):
            if point not is path:
                path[point] = steps
            steps += 1
            start = point

    return path
```

The `if point not in path` conditional is there so that points visited more than once still use the _fewest_ steps as a value.

_Note_: This operation can be shortened further by using a lesser-known dictionary method. `dict.setdefault` will only store a value if the given key does not exist:

```python
path.setdefault(point, steps)
```

The main also needs to be modified a little. Out path objects are now dictionaries so the intersections need to be computed using each path's keys. Part 1 is unchanged, and part 2 only needs to look up the steps in the paths:

```python
def main(data):
    # Input data has one wire per line
    raw_1, raw_2 = data.strip().splitlines()
    path_1 = compute_path(parse_wire(raw_1))
    path_2 = compute_path(parse_wire(raw_2))
    intersections = path_1.keys() & path_2.keys()

    yield min(abs(x) + abs(y) for x, y in intersections)  # Part 1
    yield min(path_1[pt] + path_2[pt] for pt in intersections)  # Part 2
```

[Here is the full code for day 3](../src/aoc_2019_standalone/day_03.py). You can run it with:

    ./run_aoc.py 2019 3 standalone
