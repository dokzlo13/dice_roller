
# Dice Roller

[![PyPI - Version](https://img.shields.io/pypi/v/pydiceroll)](https://pypi.org/project/pydiceroll/)
![GitHub License](https://img.shields.io/github/license/dokzlo13/dice_roller)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydiceroll)
[![dyce-powered](https://raw.githubusercontent.com/posita/dyce/latest/docs/dyce-powered.svg)](https://posita.github.io/dyce/)

> Welcome to `dice_roller`, a Python library for anyone keen on rolling dice and exploring the probabilities behind them. 

Built on the shoulders of numpy, this library doesn't just promise speed; it delivers it, enabling you to churn out massive numbers of dice rolls as numpy arrays without breaking a sweat.

### Why `dice_roller`?

- **Fast and Efficient**: Thanks to numpy, Dice Roller is incredibly fast **(TODO: PROOFS)**, making it possible to generate a large number of dice rolls quickly and efficiently. Perfect for when you need to simulate thousands of rolls in the blink of an eye.
- **Probability Modeling** with [dyce](https://posita.github.io/dyce/): Curious about the odds? We integrate with the dyce library for probability modeling, allowing you to dive deeper into the mathematics of dice rolling and get a clearer picture of potential outcomes.
- **Pretty API**: Forget about the complexity; our API is designed to be as pretty and simple as existing dice notations. It's intuitive, easy to understand, and makes dice rolling in Python a breeze.
- **Rich Notation Support**: From "keep highest" and "reroll on x" to "explode" – we've got you covered. Dice Roller supports an array of familiar dice notations, so you can express complex rolling strategies in a way that feels natural.

### Why NOT `dice_roller`?

While **`dice_roller`** offers a variety of features for dice rolling enthusiasts and developers, it's also important to understand its limitations. Here's why `dice_roller` might not be the right fit for everyone:

- **Early Version with Limited Test Coverage**: As a small hobby project, `dice_roller` is in its early stages. This means its test coverage is not as extensive as more mature libraries.
- **Designed for Simplicity, Not Complexity**: Our philosophy with `dice_roller` is to provide a simple, straightforward way to simulate dice rolls. Each roll is designed to have **one** outcome. If your project requires rolling pools of different dice and combining outcomes in more complex ways, `dice_roller` might not offer the flexibility you need without additional custom logic.
- **No Dice Notation Parsing**: Unlike some other libraries, `dice_roller` focuses on using Python-based primitives for defining dice rolls rather than parsing arbitrary dice notation strings. This approach makes for a clean and intuitive API but may not suit everyone's needs, especially if you're looking for direct notation string parsing capabilities.
- **Probability Modeling is Secondary**: Though `dice_roller` integrates with the `dyce` library for probability modeling, it's important to note that our main goal is to provide a pleasant API and rolling dices fast with numpy. If your primary focus is on modeling complex dice mechanics and probabilities, there are other tools specifically designed for that purpose which might better suit your needs.


## Get Rolling

Ready to give it a try? Installing `dice_roller` is as easy as pie:

```bash
pip install pydiceroll
```

> **Interesting fact**: do you know, almost every `dice roller` - like package name is already taken on pypi?

### Example Usage

Let's roll some dice:

```python
from dice_roller import Dice

d20 = Dice(20)
print(f"Rolling {d20} = {d20.roll()}")

# Adding modifiers to dice
d20_plus_4 = d20 + 4
print(f"Rolling {d20_plus_4} = {d20_plus_4.roll()}")
```

And now we have shiny new rolled dice.

```
Rolling d20 = 11
Rolling (d20 + 4) = 7
```

## Highlights

```python
from dice_roller import s, d, rng

def roll_info(roll: BaseDice):
    print(f"For dice '{roll}' min is {roll.min()} and max is {roll.max()}")

d20 = d(20)                                    # creating dice with possible outcomes 1-20
roll_info(d20)                                 # For dice 'd20' min is 1 and max is 20
d20.roll()                                     # Get one roll result
d20.generate(10)                               # Generates 10 rolls as numpy array
roll_info(d20 + 5)                             # For dice '(d20 + 5)' min is 6 and max is 25

fudge_dice = rng(-1, 2)                        # Creating custom range dice
roll_info(fudge_dice)                          # For dice 'rng(-1,2)' min is -1 and max is 1
fudge_dice.generate(5*3).reshape((5, 3))       # rolling a pool of dices and reshape outcome with numpy tools
# array([[-1, -1,  0],
#        [-1,  1, -1],
#        [-1,  1,  0],
#        [ 0,  0,  0],
#        [-1, -1,  0]])

advantage_roll = (2@d20).kh()                  # Keep Highest of 2 dices
disadvantage_roll = (2@d20).kl()               # Keep Lowest of 2 dices

attack_roll = (2@d20).kh() + d(4) + 3          # Roll to hit with advantage, use bless (+d4) and add +3 modifier
roll_info(attack_roll)                         # For dice '(2d20kh + d4 + 3)' min is 5 and max is 27
attack_results = attack_roll.generate(10_000)  # Generates 10000 rolls
hit_ac = attack_results[attack_results >= 16]  # Checking hits with numpy masks

damage_roll = (d(6).x == 6)                    # Roll d6 (explode on 6). Explode max 100 times (default)
roll_info(damage_roll)                         # For dice 'd6x6' min is 1 and max is 600

d20_luck = (d20.r == 1)                        # Roll d20 and reroll ones. Reroll once (default)
roll_info(d20_luck)                            # For dice 'd20r1' min is 1 and max is 20

debuff_roll = (d20 - 4) >= 1                   # Limiting your roll outcomes
roll_info(debuff_roll)                         # For dice '(d20 - 4)>=1' min is 1 and max is 16

# Let's use some functional api
from dice_roller import x, r, kh, kl, dl, dh, lim

kh(2@d(20))                                    # Keep Highest of 2 dices
kl(2@d(20))                                    # Keep Lowest of 2 dices
dh(10@d20, drop=5)                             # roll 10 d20, drop 5 highest and return sum of rest 
kh(5@d20, keep=d(2))                           # roll 5 d20, keep d2 (new reroll value each time) highest and return their sum 

explode_on_six = (x() == 6)                    # Explode on 6, max 100 times (default)
explode_on_six = (x(explode_depth=10) == 6)    # Explode on 6, max 10 times
roll_info(explode_on_six(d(6)))                # For dice 'd6x6' min is 1 and max is 600

reroll_ones = (r() == 1)                       # reroll ones, 1 reroll max (default)
reroll_ones = (r(reroll_limit=10) == 1)        # reroll ones, 100 reroll max
d20_luck = reroll_ones(d20)                    # roll d20 and
kl((2@d20_luck)).roll()                        # roll 2 d20 rolls, keeping one lowest

# Even more examples
(4@fudge_dice)                                 # roll 4 fudge dices, add results together
(d20 - d(4)) >= 1                              # roll d20-d4, ensure result greater or equal to 1
d20 * 2 + d(2) - 1                             # roll d20, multiply by 2, add d2, sub 1

d(6).r == d(2)                                 # roll d6, rerolls on 1 or 2 (new reroll value each time), 1 reroll max (default)
d(20).reroll(reroll_limit=10) == 1             # roll d20, rerolls on 1, max 10 rerolls
d(6).x >= rng(5, 7)                            # roll d6, explodes on 5 and 6. Maximum 100 explodes (default)
d(6).explode(explode_depth=2) > 4              # roll d6, explodes on 5 and 6. Maximum 2 explodes
(10@d(10)) * (10@d(10))                        # roll 2 sets of 10d10 and multiply results
(4@d(4)) @ d(10)                               # roll 4d4 of d10 dices

# roll d6 of (roll d4 of d20 dice, keep 1 highest) and drop d4 lowest. Ensure (d4 explodes on 4) <= result <= (d100 reroll <= 50).
(dl(d(6) @ kl(d(4) @ d(20)), drop=d(4)) >= (d(4).x == 4)) <= (d(100).r <= 50)
```

## Tutorial

### Basics

Main feature of this library - ability to roll large amount of rolls simultaneously, using magical powers of [numpy](https://numpy.org/).

```python
from dice_roller import Dice

d20 = Dice(20)
rolls = d20.generate(100)
print(rolls, type(rolls))
```

```
[ 7  1  5 10 12 11  8 20  5 16  9  6  3 12 12 11 19  2  8 20  7 13  1 20
  6  1 20 18  2 16  1  2 13  5  5  7  5 15  6 17 16  4  7 15 20  3  2 10
 19 20 11  6 13 11 15  1 19 19 10  4  3  9  7 14 16 12 12 19  5  2  6  9
 15 18 14  8  5 19 15 17  6  8 17 18 17  9  7 19  2 18  7 17  1 16 18 11
  5 12  5 12] <class 'numpy.ndarray'>
```

But for now let's keep things simple and focus on the other features. One important thing you need to remember now - almost all dice objects from `dice_roller` supports batch generation with `generate(total)` method.

For future understanding, lets also use some important `dice_roller` apis. Here we can check possible extremes of the dice roll outcome:


```python
from dice_roller import Dice

d20 = Dice(20)
print(f"For dice '{d20}' min is {d20.min()} and max is {d20.max()}")
# For dice 'd20' min is 1 and max is 20
```

`dice_roller` has some optimizations, which helps to calculate extreme values without expensive computations.

So far looks too boring, let's add some modifiers to this roll.

Most dice rolls result in a number that is the sum of any dice rolled, and simple math modifiers can be used to increase or decrease this result after rolls are made.

```python
from dice_roller import Dice

d20 = Dice(20)
modified_d20 = d20 + 5

print(f"For dice '{modified_d20}' min is {modified_d20.min()} and max is {modified_d20.max()}")
print(f"Rolled: {modified_d20.roll()}")
```

```
For dice '(d20 + 5)' min is 6 and max is 25
Rolled: 21
```

Here we adding constant modifier to our d20 dice. `dice_roller` objects support some mathematical operations overload, to provide simple dsl-like api.

Supported basic arithmetical operations: `+`, `-`, `*`, `/`.


```python
from dice_roller import Dice, BaseDice

def roll_info(roll: BaseDice):
    print(f"For dice '{roll}' min is {roll.min()} and max is {roll.max()}")

d20 = Dice(20)
roll_info(d20 + 4)
roll_info(d20 - 4)
roll_info(d20 * 4)
roll_info(d20 / 4)
```

```
For dice '(d20 + 4)' min is 5 and max is 24
For dice '(d20 - 4)' min is -3 and max is 16
For dice '(d20 * 4)' min is 4 and max is 80
For dice '(d20 / 4)' min is 0 and max is 5
```

**Important note**: in current state, all division operation is true division. Dices `d20 / 2` and `d20 // 2` will calculate result in same way, using rules of true division.

But this is not all, we can simply replace constant modifier with another dice:

```python
from dice_roller import Dice, BaseDice

def roll_info(roll: BaseDice):
    print(f"For dice '{roll}' min is {roll.min()} and max is {roll.max()}")

d20 = Dice(20)
d4 = Dice(4)
roll_info(d20 + d4)
roll_info(d20 - d4)
roll_info(d20 * d4)
roll_info(d20 / d4)
```

```
For dice '(d20 + d4)' min is 2 and max is 24
For dice '(d20 - d4)' min is -3 and max is 19
For dice '(d20 * d4)' min is 1 and max is 80
For dice '(d20 / d4)' min is 0 and max is 20
```

### Some Statistics

As you can see in last example, possible minimal and maximal values are not changed. Let's find other differences and check more features of `dice_roller`:

```python
import numpy as np
from dice_roller import Dice, BaseDice

def statistical_report(dice: BaseDice):
    rolls = dice.generate(1_000_000)
    print(f"Statistics for '{dice}'")
    print(f"Mean: {np.mean(rolls)}")
    print(f"Std : {np.std(rolls)}")
    print(f"Var : {np.var(rolls)}")

statistical_report(Dice(20) + 4)
print("-" * 40)
statistical_report(Dice(20) + Dice(4))
```

```
Statistics for '(d20 + 4)'
Mean: 14.500655
Std : 5.766562196922445
Var : 33.25323957097502
----------------------------------------
Statistics for '(d20 + d4)'
Mean: 13.006027
Std : 5.878449002523625
Var : 34.556162675271
```

And let's ask ChatGPT to explain this difference:

- **Mean**: The average roll result is higher for `(d20 + 4)` compared to `(d20 + d4)`, reflecting that adding a constant leads to a higher average outcome than adding another dice roll due to less variability.

- **Standard Deviation (Std)**: Indicates less variability in outcomes for `(d20 + 4)` than for `(d20 + d4)`. This means that adding a constant results in outcomes that are closer to the average, whereas adding another dice introduces more spread in the results.

- **Variance (Var)**: Confirms the trend seen in the standard deviation, with `(d20 + 4)` showing slightly less variance than `(d20 + d4)`, meaning the outcomes for the former are more tightly clustered around the mean.

**Overall**: Adding a constant to a d20 roll produces slightly higher and more consistent outcomes compared to adding the roll of a d4, which introduces more randomness and variability into the results.

Generating large amount of the rolls and then calculating required metric if simple approach, but it will require extra memory and cpu usage just to generate samples for statistics calculation.

`dice_roller` also suggest another way to calculate statistics.
Using [dyce](https://posita.github.io/dyce/) library for modeling arbitrarily complex dice mechanics, `dice_roller` brings to you perfectly designed API and ability to perform probability modeling in one package!

```python
from dice_roller import d

dice = d(8) + d(12)
h = dice.histogram()
print(h.format(scaled=True))
```

```
avg |   11.00
std |    4.14
var |   17.17
  2 |   1.04% |######
  3 |   2.08% |############
  4 |   3.12% |##################
  5 |   4.17% |########################
  6 |   5.21% |###############################
  7 |   6.25% |#####################################
  8 |   7.29% |###########################################
  9 |   8.33% |#################################################
 10 |   8.33% |#################################################
 11 |   8.33% |#################################################
 12 |   8.33% |#################################################
 13 |   8.33% |#################################################
 14 |   7.29% |###########################################
 15 |   6.25% |#####################################
 16 |   5.21% |###############################
 17 |   4.17% |########################
 18 |   3.12% |##################
 19 |   2.08% |############
 20 |   1.04% |######
```

`histogram()` method of the `BaseDice` returns [dyce.H](https://posita.github.io/dyce/0.6/dyce/#dyce.h.H) object. Returned histogram will contain finite discrete outcomes, with all modifiers applied to it.

Unfortunately, because `dice_roller` requires each transformation to return only one deterministic integer for each `roll()`, it not supports [dyce.P](https://posita.github.io/dyce/0.6/dyce/#dyce.p.P) (Dice pools) on cases with multiple dices rolled (like 2d6). Despite this, `dice_roller` will correctly calculate the histogram for this case.

```python
from dice_roller import d, kh

print(kh(5 @ d(6), keep=2).histogram().format(scaled=True))

```

```
avg |    9.93
std |    1.71
var |    2.91
  2 |   0.01% |
  3 |   0.06% |
  4 |   0.40% |
  5 |   1.03% |##
  6 |   2.71% |#####
  7 |   5.21% |##########
  8 |   9.98% |#####################
  9 |  15.43% |################################
 10 |  21.81% |#############################################
 11 |  23.73% |##################################################
 12 |  19.62% |#########################################
 ```

Let's compare two approaches:

```python
from dice_roller import BaseDice, d, kh

# Roll to hit with advantage, use bless (+d4) and add +5 modifier
r = kh(2 @ d(20)) + d(4) + 5

def stats_simulation(r: BaseDice):
    rolls = r.generate(1_000_000)
    print(f"Mean: {np.mean(rolls)}")
    print(f"Std : {np.std(rolls)}")
    print(f"Var : {np.var(rolls)}")


def stats_histogram(r: BaseDice):
    h = r.histogram()
    mu = h.mean()
    print(f"Mean: {mu}")
    print(f"Std : {h.stdev(mu)}")
    print(f"Var : {h.variance(mu)}")

stats_simulation(r)
print("-" * 40)
stats_histogram(r)
```

```
Mean: 21.3224029
Std : 4.841713051190826
Var : 23.44218527007158
----------------------------------------
Mean: 21.325
Std : 4.841939177643606
Var : 23.444375000000036
```

In comparing two methods of statistical analysis for those rolls, both simulation and histogram approaches yield remarkably similar results.
Let's compare execution time:

```python
r = kh(2 @ d(20)) + d(4) + 5

%timeit np.mean(r.generate(1_000_000))
%timeit r.histogram().mean()
```

```
2.27 s ± 19.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
1 ms ± 2.32 µs per loop (mean ± std. dev. of 7 runs, 1,000 loops each)
```

Running the simulation takes a good couple of seconds, while the histogram method is lightning fast. So, if you're looking for quick and reliable dice roll insights, the histogram way is a no-brainer.

### Dice Types

#### Scalar

Let's return back to dices. Second important dice type after regular `Dice` is `Scalar`. This type of dice simply returns constant value.
Many overload operations logic converts integers to the `Scalar` automatically, before applying modifications to original dice.
But if you want to manually use `dice_roller` objects, like `DiceAdd` in your code, you need to convert your constants into this type first.

`Scalar` is also `BaseDice`, so it implements all required API, it is useful in combinations with other dices, but you can always generate huge array of constant, using this dice.

```python
from dice_roller import Scalar

plus5 = Scalar(5)
print(f"For dice '{plus5}' min is {plus5.min()} and max is {plus5.max()}")  # For dice '5' min is 5 and max is 5
print(plus5.roll()) # 5
print(plus5.generate(10)) # [5 5 5 5 5 5 5 5 5 5]
```

#### RangeDice

If `Dice` supports only positive integers (in general), with `RangeDice` you can specify own ranges for the dice.
Range specified as in python [ranges](https://docs.python.org/3/library/functions.html#func-range) (e.g. `[start, ..., end)`).

Here is example of how to create [fudge](https://en.wikipedia.org/wiki/Fudge_(role-playing_game_system)#Fudge_dice) dice.

```python
from dice_roller import RangeDice

def roll_info(roll: BaseDice):
    print(f"For dice '{roll}' min is {roll.min()} and max is {roll.max()}")

fudge = RangeDice(-1, 2)
roll_info(fudge)  # For dice 'rng(-1,2)' min is -1 and max is 1

```

You can also provide step value for rng dice:

```python
even_only_dice = RangeDice(2, 11, 2)  # tuple(range(2,11,2)) == (2, 4, 6, 8, 10)
roll_info(even_only_dice)  # For dice 'rng(2,11,2)' min is 2 and max is 10
```

#### Dice Types Conclusion

Here is 3 most important dice types from `dice_roller`:

- `Dice` - default dice class. You should provide amount of sides, and it will roll values form 1 to `n_sides` (inclusive). Also available as `d` alias in `dice_roller`.
- `Scalar` - Constant dice, which will always be rolled into constant value, mainly used for `dice_roller` magic. Also available as `s` alias in `dice_roller`.
- `RangeDice` - Dice with little bit more freedom. Also available as `rng` alias in `dice_roller`.

Some examples of using aliases:

```python
from dice_roller import d, s, rng

d20 = d(20)
one = s(1)
fudge = rng(-1, 2)
```

### Dice Operations

We already slipped through some basics arithmetical operations. What else we can do with our dices?

#### Limits

As you can see in basic arithmetic examles above, dice `d20-4` may outcome negative minimal value. It's because lowest result of the d20 roll is `1`, and `1-4=-3`.

We can ensure dice outcome will be in bounds by providing limit with comparison operators overload:

```python
from dice_roller import Dice
d20 = Dice(20)

safe_roll = (d20 - 4) >= 1 # roll of the (d20 - 4) must be greater or equal to 1
roll_info(safe_roll)  # For dice '(d20 - 4)>=1' min is 1 and max is 16
```

`dice_roller` support different types of limits:

```python
from dice_roller import d
d20 = d(20)

d20 >= 19    # greater or equal to 19
d20 > 19     # greater then 19
d20 <= 2     # less or equal to 2
d20 < 2      # less then 2

# You can also use dices to construct limit, compared dice will be rolled first. New value will be rolled each time.
d20 >= d(4)  # d20 greater or equal to value of d4
d20 <= d(4)  # d20 less or equal to value of d4
```

As you see, here is no `==` operator supported. This has no sense - in case of `==`, any roll can be replaced with `Scalar`, and you should do this instead.

#### Multiple Dices

First thing we can make after rolling some dices - roll even more dices!

Python’s matrix multiplication operator (@) is used to express the number of a particular die (roughly equivalent to the "d" operator in common notations).
When you create multiple dice request, like `3d4`, result of the roll will always be sum of the all values of all requested dices rolled. One return value for roll - is the part of `dice_roller` philosophy.

So, your D&D wizard throws fireball, and you want to roll 8d6 fire damage? Easy:

```python
from dice_roller import Dice

d6 = Dice(6)
dice_8d6 = 8@d6

print(f"Fireball deals '{dice_8d6}' damage:")
print(f"At least: {dice_8d6.min()}")
print(f"At most: {dice_8d6.max()}")
print(f"Average: {dice_8d6.histogram().mean():.0f}")
print(f"Rolled {dice_8d6.roll():.0f}")
```

```
Fireball deals '8d6' damage:
At least: 8
At most: 48
Average: 28
Rolled 27
```

You can also create `<dice>` roll of `<dice>`:

```python
from dice_roller import Dice

(Dice(4)@Dice(6)).roll()  # 16
```

> **Important**: Parentheses are needed in the above example because `@` has a lower precedence than `.`

In this case, `dice_roller` will first roll `d4` for amount of `d6` dices to roll, and then roll this amount of `d6` and add them together to calculate outcome.

#### Keep Highest

This modifier causes the `dice_roller` to keep and add together a number of dice you specify, selecting the highest of the roll results available. Without a specified args it will keep the single highest roll. If the number of dice to roll (`of`) is less than the number of dice being kept (`keep`) then it will keep all the rolls made.

Let's simulate D&D 5e "Advantage"

```python
from dice_roller import Dice, KeepHighest

d20advantage = KeepHighest(2@Dice(20))  # by default, selects 1 highest dice of 2 dice rolled.
```

Using `KeepHighest` will have sense only when you use it with multiple dices, created with `@` operator. If you use it with one dice, outcome will be same as not using `KeepHighest` at all: `KeepHighest(Dice(20)) ~ Dice(20)`

You can override amount of tries and amount of rolls, which will be added in final roll:

```python
from dice_roller import Dice, kh  # kh is alias for KeepHighest

d20_keep_2_high_of_5 = kh(5@Dice(20), keep=2)  # Keeps and add together 2 highest rolls of 5 rolled
```

You can use complex dice expressions with KeepHighest, `keep` field also supports `BaseDice` object:

```python
from dice_roller import d, kh

kh(4 @ d(20), keep=d(4))  # roll 4d20, keep d4 highest
kh(d(4) @ d(20), keep=(d(4) / 2) >= 1)  # roll d4 of d20 dice, keep d4/2 (at least one) highest
kh(d(6) @ kh(d(4) @ d(20)), keep=d(4))  # roll d6 of (roll d4 of d20 dice, keep 1 highest) and keep d4 highest
```

#### Keep Lowest

This modifier causes the `dice_roller` to keep and add together a number of dice you specify, selecting the lowest of the roll results available. Without a specified args it will keep the single lowest roll. If the number of dice to roll (`of`) is less than the number of dice being kept (`keep`) then it will keep all the rolls made.

Let's simulate D&D 5e "Disadvantage"

```python
from dice_roller import Dice, KeepLowest

d20disadvantage = KeepLowest(2@Dice(20))  # by default, selects 1 lowest dice of 2 dice rolled.
```

Using `KeepLowest` will have sense only when you use it with multiple dices, created with `@` operator. If you use it with one dice, outcome will be same as not using `KeepLowest` at all: `KeepLowest(Dice(20)) ~ Dice(20)`

You can override amount of tries and amount of rolls, which will be added in final roll:

```python
from dice_roller import Dice, kl  # kl is alias for KeepLowest

d20_keep_2_low_of_5 = kl(5@Dice(20), keep=2)  # Keeps and add together 2 lowest rolls of 5 rolled
```

You can use complex dice expressions with KeepLowest, `keep` field also supports `BaseDice` object:

```python
from dice_roller import d, kl

kl(4 @ d(20), keep=d(4))  # roll 4d20, keep d4 lowest
kl(d(4) @ d(20), keep=(d(4) / 2) >= 1)  # roll d4 of d20 dice, keep d4/2 (at least one) lowest
kl(d(6) @ kl(d(4) @ d(20)), keep=d(4))  # roll d6 of (roll d4 of d20 dice, keep 1 lowest) and keep d4 lowest
```

#### Drop Highest

This modifier causes the `dice_roller` to drop a number of dice you specify, selecting the highest of the roll results available. Rest of the rolls added together. If no args specified, then it will drop the one highest number rolled. If the number of dice to roll (`of`) is less than the number of dice to drop (`drop`), then it will keep all the rolls made.

We can also simulate D&D 5e "Disadvantage" mechanic with this modifier:

```python
from dice_roller import Dice, DropHighest

d20disadvantage = DropHighest(2@Dice(20))  # by default, drops 1 highest dice of 2 dice rolled.
```

Using `DropHighest` will have sense only when you use it with multiple dices, created with `@` operator. If you use it with one dice, outcome rolls will always be 0, because modifier drops single roll from 1: `DropHighest(Dice(20)) ~ 0`

You can override amount of tries and amount of rolls, which will dropped from final roll:

```python
from dice_roller import Dice, dh  # dh is alias for DropHighest

d20_drop_high_2of5 = dh(5@Dice(20), drop=2)  # Drop 2 highest rolls and add together rest of 5 rolled
```

You can use complex dice expressions with DropHighest, `drop` field also supports `BaseDice` object:

```python
from dice_roller import d, dh

dh(4 @ d(20), drop=d(4))  # roll 4d20, drop d4 highest
dh(d(4) @ d(20), drop=(d(4) / 2) >= 1)  # roll d4 of d20 dice, drop d4/2 (at least one) highest
dh(d(6) @ dh(d(4) @ d(20)), drop=d(4))  # roll d6 of (roll d4 of d20 dice, drop 1 highest) and drop d4 highest
```

#### Drop Lowest

This modifier causes the `dice_roller` to drop a number of dice you specify, selecting the lowest of the roll results available. Rest of the rolls added together. If no args specified, then it will drop the one lowest number rolled. If the number of dice to roll (`of`) is less than the number of dice to drop (`drop`), then it will keep all the rolls made.

We can simulate D&D 5e  "Advantage" mechanic with this modifier:

```python
from dice_roller import Dice, DropLowest

d20advantage = DropLowest(2@Dice(20))  # by default, drops 1 lowest dice of 2 dice rolled.
```

Using `DropLowest` will have sense only when you use it with multiple dices, created with `@` operator. If you use it with one dice, outcome rolls will always be 0, because modifier drops single roll from 1: `DropLowest(Dice(20)) ~ 0`

You can override amount of tries and amount of rolls, which will dropped from final roll:

```python
from dice_roller import Dice, dl  # dl is alias for DropLowest

d20_drop_low_2of5 = dl(5@Dice(20), drop=2)  # Drop 2 lowest rolls and add together rest of 5 rolled
```

You can use complex dice expressions with DropLowest, `drop` field also supports `BaseDice` object:

```python
from dice_roller import d, dl

dl(4 @ d(20), drop=d(4))  # roll 4d20, drop d4 highest
dl(d(4) @ d(20), drop=(d(4) / 2) >= 1)  # roll d4 of d20 dice, drop d4/2 (at least one) lowest
dl(d(6) @ dl(d(4) @ d(20)), drop=d(4))  # roll d6 of (roll d4 of d20 dice, drop 1 lowest) and drop d4 lowest
```

#### Reroll

Rerolls the die based on the set condition, keeping the outcome regardless of whether it is better. Reroll will only reroll the die and use new result, for continual rerolling with sum see `Explode` below.

This modifier requires specifying extra condition. Here is example:

```python
from dice_roller import Dice

d20_reroll_ones = Dice(20).r == 1  # Reroll ones on d20
```

Reroll also supports functional api. You can create and store reroll modifier in following way:

```python
from dice_roller import Reroll, Dice

reroll_ones = (Reroll() == 1)
d20_reroll_ones = reroll_ones(Dice(20))
```

Also, take into account - result of `Reroll()` is not dice itself, it is modifier wrapper. You need to apply this modifier to dice to perform rolls.

```python
from dice_roller import Reroll

(Reroll() == 1).roll()  # is not okay
(Reroll() == 6)(some_dice).roll()  # is okay
```

**By default, roll can be rerolled once**, but you can override this behavior:

```python
from dice_roller import r, d  # r is alias for Reroll

# dice may be rerolled 100 times, if has sequential ones on d20 roll
d = (d(20).reroll(reroll_limit=100) == 1)

# For functional API
reroll_ones = (r(reroll_limit=100) == 1)
d20_reroll_ones_100_times_max = explode_on_6(d(6))
```

`Reroll` supports several comparison operations:

```python
from dice_roller import r, d

d20 = d(20)
d20.r == 10
d20.r > 10
d20.r >= 10
d20.r < 10
d20.r <= 10

reroll_on_6 = (r() == 6)
reroll_on_gt_5 = (r() > 5)
reroll_on_ge_5 = (r() >= 5)
reroll_on_lt_5 = (r() < 5)
reroll_on_le_5 = (r() <= 5)
```

You can also provide dices for `Reroll`, let's call it "Reroll Dice". In this case, "Reroll Dice" will be rolled first, and then, if dice outcomes into required dice, it will be rerolled. "Reroll Dice" rolled after each reroll step.

```python
from dice_roller import r, RangeDice, Dice

d3_with_magic = (Dice(3).r == RangeDice(1, 3))  # rerolls on 1 or 2

reroll_1_or_2 = (x() == RangeDice(1, 3)))  # rerolls on 1 or 2
d3_with_magic = reroll_1_or_2(Dice(3))
```

Logic example:

- Rolls "Reroll Dice" (RangeDice in this case), get 1
- Rolls dice, get 1
- Need to reroll, proceed to next loop
- Rolls "Reroll Dice", get 2
- ReRolls dice, get 2
- Need to reroll, proceed to next loop
- Rolls "Reroll Dice", get 1
- ReRolls dice, get 3 - no need to reroll, return

#### Explode

Explode rerolls a die continually based on the set condition, so that each occurrence of the number rolls again, continually adding to the total result.

This modifier requires specifying extra condition. Here is example:

```python
from dice_roller import Dice

d6_explode_on_6 = Dice(6).x == 6  # Explode on 6 on d6 dice
```

Reroll also supports functional api. You can create and store reroll modifier in following way:

```python
from dice_roller import Explode, Dice

explode_on_6 = (Explode() == 6)
d6_explode_on_6 = explode_on_6(Dice(6))
```

Also, take into account - result of `Explode()` is not dice itself, it is modifier wrapper. You need to apply this modifier to dice to perform rolls.

```python
from dice_roller import Explode

(Explode() == 6).roll()  # is not okay
(Explode() == 6)(some_dice).roll()  # is okay
```

**By default, roll can be exploded 100 times**, but you can override this behavior during constructing `Explode` instance:

```python
from dice_roller import x, d  # x is alias for Explode

# dice may be exploded only 5 times sequentially on d6 roll
# If you lucky enough, you will obtain result of `np.sum([6,6,6,6,6])`
d = (d(20).explode(explode_depth=5) == 1)

# For functional API
explode_on_6 = (x(explode_depth=5) == 6)
d6_explode_on_6_5_times = explode_on_6(d(6))
```

`Explode` supports several comparison operations:

```python
from dice_roller import d, x

d6 = d(6)
d6.x == 6
d6.x > 5
d6.x >= 5
d6.x < 2
d6.x <= 2

explode_on_6 = (x() == 6)
explode_on_gt_5 = (x() > 5)
explode_on_ge_5 = (x() >= 5)
explode_on_lt_5 = (x() < 2)
explode_on_le_5 = (x() <= 2)
```

You can also provide dices for `Reroll`, let's call it "Explode Dice". In this case, "Explode Dice" will be rolled first, and then, if dice outcomes into required dice, it will be exploded. "Explode Dice" rolled after each exploding step.

```python
from dice_roller import x, RangeDice, Dice

d6_explode_on_5_or_6 = (Dice(3).x == RangeDice(5, 7))  # explodes on 5 or 6

explode_on_5_or_6 = (x() == RangeDice(5, 7)))  # explodes on 5 or 6
d6_explode_on_5_or_6 = explode_on_5_or_6(Dice(6))
```

Logic example:

- Rolls "Explode Dice" (RangeDice in this case), get 6
- Rolls dice, get 6
- Need to explode, adding roll to overall result and proceed to next loop
- Rolls "Explode Dice", get 5
- Rolls new dice, get 5
- Need to explode, adding roll to overall result and proceed to next loop
- Rolls "Explode Dice", get 6
- Rolls dice, get 3 - adding to overall result, but here is no need to explode further, return
