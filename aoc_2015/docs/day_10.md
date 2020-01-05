# Advent of Code 2015, day 10

https://adventofcode.com/2015/day/10

- [The normal solution](#the-normal-solution)
- [The fancy solution](#the-fancy-solution)

Today's puzzle is a classic: The _Look and Say Sequence_ (or _Conway's Sequence_). It's also one of my favorite puzzles because of rich and deep it is, despite its deceptively simple formulation.

## The "normal" solution

Look and Say is a relatively common interview question. Consequently, you will find [many implementations documented online](https://www.rosettacode.org/wiki/Look-and-say_sequence).

In general, the approach works using a loop over all characters of the string, keeping track of the previous character and how many times in a row it has appeared. Every time the current character is different from the previous one, it means that we are on a boundary between two groups, and we can store the group's length and character inside our result.

```python
def look_and_say(string):
    result = ""

    previous, count = string[0], 1
    for char in string[1:]:
        if char != previous:
            result += str(count) + previous
            previous, count = char, 1
        else:
            count += 1
    result += str(count) + previous

    return result
```

There are other ways to implement this in Python, for example using [`itertools.groupby`](https://docs.python.org/3/library/itertools.html#itertools.groupby):

```python
from itertools import groupby

def look_and_say(string: str):
    result = ""
    for char, grouper in groupby(string):
        result += str(sum(1 for _ in grouper)) + char
    return result
```

You can then apply this calculation on top of itself many times to solve the puzzle. [Here is the full implementation of this approach](../src/aoc_2015_simple/day_10.py). You can run it with:

    ./run_aoc.py 2015 10 simple

This works… "fine". Computing the result for part 2 takes several seconds to run on my machine. Pretty bad, but good enough if all you want is to solve the Advent of Code problem.
 
There is MUCH more to that puzzle however, so buckle up.

## The fancy solution

This problem was studied in detail by [John H. Conway](https://en.wikipedia.org/wiki/John_Horton_Conway) in _The Weird and Wonderful Chemistry of Audioactive Decay_ (1986). If that name sounds familiar, that is because Conway also famously worked on the [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) that bears his name.

Using his findings, we can _massively_ improve our solution, to the point where calculating the length of the string after 50 steps will look trivial.

### Splitting the string

The first and most fundamental result from this paper is one that allows us to _divide_ the problem. It reads as follows:

> _The Splitting Theorem_:
>
> A 2-day-old string `LR` splits as `L.R` just if one of `L` and `R` is empty or `L` and `R` are of the types shown in one of:
> 
> | L   | R
> |-----|---------------
> | n]  | [m (n ≥ 4, m ≤ 3)
> | 2]  | [1<sup>1</sup>X<sup>1</sup> or [1<sup>3</sup> or [3<sup>1</sup>X<sup>≠1</sup> or [n<sup>1</sup> (n ≥ 4)
> | ≠2] | [2<sup>2</sup>1<sup>1</sup>X<sup>1</sup> or [2<sup>2</sup>1<sup>3</sup> or [2<sup>2</sup>3<sup>1</sup>X<sup>≠1</sup> or [2<sup>2</sup>n<sup>(0 or 1)</sup> (n ≥ 4)

This intimidating table will be the most complicated part of the implementation, I promise. But it is the most important.
 
What "splitting" means here is that a string can be divided into substrings. And those will _never_ interfere with each other again no matter how many times look-and-say is applied. For example, here are the possible splits at each level starting with 31133:
 
    31133
    132.12.3
    111312.1112.13
    31131112.3112.1113
    1321133112.132112.3113
    11131.22.12.32112.1113122112.132113

My splitting implementation relies mostly on regular expressions. A first step detects if a string ends with `[^2]22` (in which case the `22` can be isolated). Then the string is checked against 5 different patterns. If it matches, then the string can be split after the first character of that match.  

```regexp
21([^1])(?!\1)
2111[^1]
23(?:$|([^3]){1,2}(?!\1))
2([^123])(?!\1)
[^123][123]
```

That logic is then applied recursively on each side of the split string. It is not the prettiest approach, but it works.

One important detail for later is that this logic MUST NOT be applied on strings that have not been at least through **two** iterations of the look-and-say transformation (a.k.a. two-day strings). The initial string can be any string and the mathematical properties of the transformation only appear after applying it a couple of times.

For example, the successors of `41111` are `1441` then `112411`. If we apply the split on the initial string then transform each half, we'll get `4.1111` then `14.41` and `1114.1411`. This shows that splitting too early does not guarantee that the substrings are independent. In this case, the split can be applied safely on day 2 as `112.4.11`.

### The chemistry of look-and-say

This is where it gets crazy. Conway observed that the result of transforming and splitting a string many times follows a pattern. The resulting substrings are finite in number, 92 to be precise. Conway calls those _the common elements_. Amusingly, he gave them names from the periodic table, from Hydrogen to Uranium.

This is one of the major results of his research, and reads as follows:

> _The Chemical Theorem_:
>
> 1. The descendents of any of the 92 elements in our Periodic Table are compounds of those elements.
> 2. All sufficiently late descendents of any of these elements other than Hydrogen (`22`) involve **all** of the 92 elements simultaneously.
> 3. The descendents of **any** string other than `""` (empty string) or `"22"` also ultimately involve all of those 92 elements simultaneously.
> 4. These 92 elements are precisely the common elements as defined in [a table in the paper].

On top of the 92 common elements (which only contain the digits 1, 2, and 3) there are two special elements for the higher digits:

> _The Transuranic Elements_:
>
> For each number n ≥ 4, we define two particular atoms:
>
> * an isotope of **Plutonium** (Pu): `31221132221222112112322211n`
> * an isotope of **Neptunium** (Np): `1311222113321132211221121332211n`

The common elements plus all transuranic elements build the full _Cosmolgy_ of elements, which has a remarkable property:

> _The Cosmological Theorem_:
>
> **Any** string decays into a compound of common and transuranic elements after a bounded number of derivation steps. […]

This is a _very_ important result. It means that _every_ starting string will eventually be composed of sub-strings from a **finite** set of elements (even if the length of said string grows exponentially). Since we are only interested in the length of the string, this has massive consequences.

Say we start with `12322211331222113112211` (which is element 40, Zirconium). Its descendents are:

    12322211331222113112211 (Zr)
    1112133.22.12.311322113212221 (Y.H.Ca.Tc)
    3112112.3.22.1112.13211322211312113211 (Sr.U.H.K.Mo)
    1321122112.13.22.3112.1113122113322113111221131221 (Rb.Pa.H.Ar.Nb)
    11131221222112.1113.22.132112.311311222.12322211331222113112211 (Kr.Th.H.Cl.Er.Zr)

After 4 steps, our starting element Zirconium appears again. Therefore, instead of re-applying the calculation to it, we can re-use the results we already have to compute the next lengths of that part of sub-string. And going that deep is not even necessary: the length of the descendent of Zr at depth `N > 0` is _always_ equal to the sum of the lengths of the descendents of Y, H, Ca, and Tc at depth `N - 1`. So we can apply the same thinking to those elements to build our results recursively.

Thanks to the theory we know this applies to **every** string, and that there is a **bounded** number of elements to track. Therefore, by storing enough results we can theoretically compute the length of the descendent of anything at any depth pretty fast.

### Building the solution

Now that we have tools, let's use them to build code that will leave our first solution in the dust.

The first step is to compute the immediate descendents of a given string.

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def memoized_look_say_split(string):
    return split(look_and_say(string))
```

This code may not look impressive, but it is essential to our solution. It takes a string as input, runs the transformation on it, then splits the result. Most importantly, it caches the result: this means we only need to run the actual look and say transformation once per element!

Now we can implement the core logic of our calculation:

```python
from itertools import count

def iter_look_and_say_lengths(string):

    @lru_cache(maxsize=4096)
    def recursive_lns_length(_string, depth):
        if depth <= 0:
            return len(_string)
        res, n_depth = 0, depth - 1
        for atom in memoized_look_say_split(_string):
            res += recursive_lns_length(atom, n_depth)
        return res

    yield len(string)
    string = look_and_say(string)
    for i in count():
        yield recursive_lns_length(string, i)
```

This is a generator that yields the length of the given string at each step of the process (starting with the unmodified input). It then computes the lengths one by one using an internal recursive function.

The inner `recursive_lns_cache` transforms then splits the string, then computes its length at depth `n` by summing the lengths at depth `n - 1` of its direct descendents, calling itself recursively to do so. To initialize (or terminate?) the recursion, it also returns its own length at depth `0`.

But surely this recursion grows uncontrollably, right? Each additional layer will require an exponential number of calls and our runtime will be poor, even if the look and say transformation is cached. And that would be correct, if it were not for one particular line of code.

That's where the `lru_cache` enters the scene. By storing our previous results, each step of the iterator only needs to compute one step for each element and the recursion ends early. In fact, the number of calculations to run at each step is _guaranteed to be constant_ after a while.

All that's left to solve the puzzle is to instantiate the iterator and take its 40th and 50th results.

```python
def main(string):
    """Yields the lengths at 40 and 50 steps"""
    iterator = iter_look_and_say_lengths(string)
    yield next(islice(iterator, 40, None))  # Part 1
    yield next(islice(iterator, 9, None))  # Part 2
```

[Here is the full code](../src/aoc_2015/day_10.py). You can run it with:

    ./run_aoc.py 2015 10 -t

The `-t` option enables timing on the runner. That should show you just how fast this solution is — 3 milliseconds to run both parts on my computer! This is around 1,000× faster than before! Even better: its run time is not exponential and we can go much, much further in the sequence. In the time it took for our first solution to compute the length of element 50 (3 seconds), I was able to compute the length of element _40,000_! Which happens to be a ridiculous number that fills up my terminal screen with digits.

### The nasty details

While you most likely get the general idea, I skipped some important details in my implementation. Here are some questions you might have:

#### "_Why have `@lru_cache(maxsize=128)` on `memoized_look_say_split`?_"

That is the cache that stores the results of the transform and split. Its size was chosen as 128 since that is the next power of 2 larger than 92, and it still gives us some extra room to play with. Arguably, this cache does not need to be LRU or have a size limit. But `lru_cache` is well optimized and it is imported anyway, so I might as well use it. I also know that 128 is the default cache size already, but explicit is better than implicit.

#### "_So what about `@lru_cache(maxsize=4096)` on `recursive_lns_length`?_"

This cache is much more critical, without it the solution would not work. It stores all the intermediate results of the length calculation. The 4,096 size value is somewhat magic though, I had to set it by trial an error. Setting it any lower causes the recursion to not hit the cache when it should, ending in (exponential) bad times. 2,048 is barely enough but not quite always. Setting that maximum size to `None` is also a bad idea; the memory usage of storing every result is _O(log(n!))_ and your operating system _might_ not be too happy about it.

#### "_Why do you run `look_and_say` once in the iterator before calling the internal function? Could you not use it directly?_"

No, because that inner function uses splitting and that is only allowed after transforming the string twice. `memoized_look_say_split` does it once, so we need to run it once initially to be safe.

#### "_Why is the cached recursive call hidden inside the iterator?_"

That is because this recursive call MUST be called for every depth incrementally. Otherwise, the cache does not build up (and roll over) to include the results we need to move on. Since not calling this function properly _will_ cause quasi-infinite run times or a recursion limit overflow, I think not exposing it is better.

#### "_Does this run in linear time?_"

Almost. While the number of calculations we need to run per step is constant, the integers we are working with are still growing exponentially at a rate of λ = 1.303577… (_Conway's Constant_, another finding of the paper). Thankfully, Python transparently handles large integers by default, but the CPU cost of processing those grows with their size. Since the numbers are growing slower than their bit size (λ < 2), I _think_ the runtime is _O(n.log(n))_. I have not been able to confirm that experimentally though.

#### "_But where are the chemical elements you talked about for so long?_"

This solution does not need them, which is why I like it so much! By transforming and splitting alone, the strings we manipulate will eventually be all those elements. The solution is built to take advantage of their existence and will find them pretty much automatically.

### Going further

This is by far the most elegant of the implementations I tried. It is a great demonstration of how powerful recursion and generators are in Python when used astuciously.

I spent some time playing around with different solutions that exploit the theory. In truth, it took me weeks of iterations before reaching the code I showed above. That journey taught a lot about generators, iterators, memory usage and optimization.

Interestingly, this cached recursive solution is not the fastest I have designed. I was able to achieve up to twice the speed (same complexity though) using an approach that is aware of the full "periodic table" of elements. It works by:

1. finding which elements the given input string eventually splits into,
2. building a web of self-referencing iterators, with one master iterator per element that sums the values yielded by the other elements' iterators,
3. create a length iterator that sums references those iterators in a complicated way to achieve the same result.

I nicknamed this solution "_How to abuse `itertools.tee`_". It's obsenely complicated and it would take me half an hour to explain it orally. I won't show it here for the sake of everyone's sanity.
