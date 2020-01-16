# Advent of Code "solutions" in Python

This repository holds all my current solutions to the [Advent of Code](https://adventofcode.com/) challenges from 2015 to 2019.

State of the code by year:

* **2015**: _Completed_. Done recently, so the code mostly good I think.
* **2016**: In progress (almost there), some of it doesn't run well.
* **2017**: _Completed_. Old code, lots of it definitely broken.
* **2018**: _Completed_. Code in good state and should work.
* **2019**: _Completed_ (except day 25). All the code works, currently in the process of cleaning it up.

## Acknowledgements

Huge shout-out to and infinite respect for Eric Wastl, the creator of Advent of Code and designer of all its puzzles. For having tried myself, creating good and fun programming puzzles requires _crazy_ amounts of effort. Being able to build two dozens of these every year, with randomized input data and a storyline, is nothing short of mind-blowing.

Kudos to my colleagues too, off whom I like to bounce ideas.

## Disclaimer

* _Most of this is not good code_. It is either undocumented, untested, full of assumptions, slow, or broken. Maybe all of the above.
* I have years of experience writing Python but I am by no means an expert. I try to follow best practices and point out where I explicitly do not, but don't take my word for it.
* I try to make my solutions run reasonably fast, at the very least not take more than several seconds. I have no reference for what's considered fast or slow, so any claim I make about code being optimized is potentially very very wrong.
* I don't think my solutions are particularly exotic, but that's subjective. This is mostly "normal" Python.

## The Good Stuff

What I _am_ trying to do correctly is to document and explain my solutions accessibly. I recommend heading out to the wiki for the index of documented solutions:

* [Index for 2015 solutions](aoc_2015/docs/readme.md)
* [Index for 2019 solutions](aoc_2019/docs/readme.md)

## Requirements

This code **requires Python 3.8** to run. Before you ask, yes I use the "Walrus" operator. No, I don't care if you hate it. And that's not the only 3.8 feature I use so deal with it.

Other requirements:
* [NumPy](https://numpy.org/) (known to work with 1.17)
* [Parsimonious](https://pypi.org/project/parsimonious/)
* [pytest](https://docs.pytest.org/en/latest/) to run the (few) tests
