
# Dice Roller

## Tutorial

### Basics

Let's jump in:

```python
from dice_roller import Dice

d20 = Dice(20)
print(f"Rolling {d20} ...")
roll = d20.roll()

print(f"Rolled {roll}")
```

And now we have shiny new rolled dice.

```
rolling d20 ...
Rolled 6
```

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

But for now let's keep things simple and focus on the features. One important thing you need to remember now - almost all things from `dice_roller` supports batch generation with `generate(total)` method.

For future understanding, lets also use some important `dice_roller` apis. Here we can check possible extremes of the dice roll outcome:


```python
from dice_roller import Dice

d20 = Dice(20)
print(f"For dice '{d20}' min is {d20.min()} and max is {d20.max()}")
# For dice 'd20' min is 1 and max is 
```

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

As you can see in last example, possible minimal and maximal values are not changed. Let's find other differences:

```python
from dice_roller import Dice, BaseDice

def statistical_report(dice: BaseDice):
    print(f"Statistics for '{dice}'")
    print(f"Std. Dev is {dice.std():.3f}")
    print(f"Median is {dice.median():.3f}")
    print(f"Avg is {dice.average():.3f}")
    print(f"Mean is {dice.mean():.3f}")
    print("-"*40)


statistical_report(Dice(20) + 4)
statistical_report(Dice(20) + Dice(4))
```

```
Statistics for '(d20 + 4)'
Std. Dev is 5.769
Median is 15.000
Avg is 14.498
Mean is 14.505
----------------------------------------
Statistics for '(d20 + d4)'
Std. Dev is 5.866
Median is 13.000
Avg is 13.004
Mean is 13.002
----------------------------------------
```

And let's ask ChatGPT to explain this difference:

- **Standard Deviation**: Slightly higher in the d20 + d4 roll (5.866) than the d20 + 4 (5.769), indicating more variability when adding a dice roll versus a constant.

- **Median**: The median is higher for d20 + 4 (15.000) compared to d20 + d4 (13.000), reflecting the shift in the distribution's center due to the constant addition.

- **Average (Avg)** and **Mean**: Both are higher for d20 + 4 (14.498 and 14.505, respectively) than for d20 + d4 (13.004 and 13.002), showing that adding a constant value results in a higher overall result than the variable addition of another dice roll.

**Overall Explanation**: Adding a constant value (4) to a d20 roll results in uniformly higher outcomes and slightly less variability than adding the roll of a d4, due to the fixed increase versus the variable increase provided by another dice roll.

If you interested, how `dice_roller` calculates this statistical data - answer is simple. `dice_roller` just generates large amount of the rolls (*one million by default*) and then calculates required metric.

Sorry, I'm just an average engineer, not a mathematician. If someone is capable to calculate those values without simulations - please contribute.

Also, if you need to alter amount of simulations, you can do it in 2 ways:

```python
from dice_roller import Dice
dice = Dice(20)

dice.STATISTIC_SIMULATION_SAMPLES = 10_000_000  # changes samples count for all statistic methods

avg = dice.average(samples=100_000_000)  # alters only this calculation
```

### Dice Types

#### Scalar

Second important dice type after regular `Dice` is `Scalar`. This type of dice simply returns constant value.
Many overload operations logic converts integers to the `Scalar` automatically, before applying modifications to original dice.
But if you use objects, like `Max` from `dice_roller` in your code, prefer to convert your constants into this type.

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
Range specified as in python [ranges](https://docs.python.org/3/library/functions.html#func-range) (e.g. `[start, ..., end)`), but step is not available (yet)

Here is example of how to create [fudge](https://en.wikipedia.org/wiki/Fudge_(role-playing_game_system)#Fudge_dice) dice.

```python
from dice_roller import RangeDice

fudge = RangeDice(-1, 2)
print(f"For dice '{fudge}' min is {fudge.min()} and max is {fudge.max()}")
# For dice 'd[-1 to 2]' min is -1 and max is 1
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

As you can see in basic arithmetic exables below, dice `d20-4` may outcome negative minimal value. It's because lowest result of the d20 roll is `1`, and `1-4=-3`.

We can ensure dice outcome will be in bounds by providing limit, both with comparison operators overload or with `Min` and `Max` wrapper:

```python
from dice_roller import Dice
d20 = Dice(20)

safe_roll = (d20 - 4) > 1 # roll of the (d20 - 4) must be greater then 1
roll_info(safe_roll)

from dice_roller import Min, Scalar
safe_roll = Min(d20 - 4, Scalar(1))
roll_info(safe_roll)
```

```
For dice '(d20 - 4)min1' min is 1 and max is 16
For dice '(d20 - 4)min1' min is 1 and max is 16
```


#### Multiple Dices

First thing we can make after rolling dice - roll more dices!

Your D&D wizard throws fireball, and you want to roll 8d6 fire damage? Easy:

```python
from dice_roller import Dice

d6 = Dice(6)
dice_8d6 = 8 ** d6

print(f"Fireball deals '{dice_8d6}' damage:")
print(f"At least: {dice_8d6.min()}")
print(f"At most: {dice_8d6.max()}")
print(f"Average: {dice_8d6.average():.0f}")
print(f"Rolled {dice_8d6.roll():.0f}")
```

```
Fireball deals '8d6' damage:
At least: 8
At most: 48
Average: 28
Rolled 27
```

Equivalent to create same dice with objects is:

```python
from dice_roller import Dice, DiceMany, Scalar
dice_8d6 = DiceMany(total=Scalar(8), dice=Dice(6))
```

You can also create `dice` roll of `dice`:

```python
from dice_roller import Dice

dice_d4d6 = Dice(4) ** Dice(6)
```

In this case, `dice_roller` will first roll `d4` for amount of `d6` dices to roll, and then roll this amount of `d6` and add them together to calculate outcome.

#### Keep Highest

This modifier causes the `dice_roller` to keep and add together a number of dice you specify, selecting the highest of the roll results available. Without a specified args it will keep the single highest number of two. If the number of dice to roll (`of`) is less than the number of dice being kept (`keep`), an exception will be raised on construction.

Let's simulate D&D 5e "Advantage"

```python
from dice_roller import Dice, KeepHighest

d20advantage = KeepHighest(Dice(20))  # by default, selects 1 highest dice of 2 rolled.
```

You can override amount of tries and amount of rolls, which will be added in final roll:

```python
from dice_roller import Dice, kh  # kh is alias for KeepHighest

d20_high_2of5 = kh(Dice(20), keep=2, of=5)  # Keeps and add together 2 highest rolls of 5 rolled
```

#### Keep Lowest

This modifier causes the `dice_roller` to keep and add together a number of dice you specify, selecting the lowest of the roll results available. Without a specified args it will keep the single lowest number of two. If the number of dice to roll (`of`) is less than the number of dice being kept (`keep`), an exception will be raised on construction.

Let's simulate D&D 5e "Disadvantage"

```python
from dice_roller import Dice, KeepLowest

d20disadvantage = KeepLowest(Dice(20))  # by default, selects 1 lowest dice of 2 rolled.
```

You can override amount of tries and amount of rolls, which will be added in final roll:

```python
from dice_roller import Dice, kl  # kl is alias for KeepLowest

d20_low_2of5 = kl(Dice(20), keep=2, of=5)  # Keeps and add together 2 lowest rolls of 5 rolled
```

#### Drop Highest

This modifier causes the `dice_roller` to drop a number of dice you specify, selecting the highest of the roll results available. Rest of the rolls added together. If no args specified, then it will drop the one highest number rolled of two. If the number of dice to roll (`of`) is less than the number of dice to drop (`drop`), an exception will be raised on construction.

We can simulate D&D 5e  "Disadvantage" mechanic with this modifier:

```python
from dice_roller import Dice, DropHighest

d20disadvantage = DropHighest(Dice(20))  # by default, drops 1 highest dice of 2 rolled.
```

```python
from dice_roller import Dice, dh  # dh is alias for DropHighest

d20_drop_high_2of5 = dh(Dice(20), drop=2, of=5)  # Drop 2 highest rolls and add together rest of 5 rolled
```

#### Drop Lowest

This modifier causes the `dice_roller` to drop a number of dice you specify, selecting the lowest of the roll results available. Rest of the rolls added together. If no args specified, then it will drop the one lowest number rolled of two. If the number of dice to roll (`of`) is less than the number of dice to drop (`drop`), an exception will be raised on construction.

We can simulate D&D 5e  "Advantage" mechanic with this modifier:

```python
from dice_roller import Dice, DropLowest

d20advantage = DropLowest(Dice(20))  # by default, drops 1 lowest dice of 2 rolled.
```

```python
from dice_roller import Dice, dl  # dl is alias for DropLowest

d20_drop_low_2of5 = dl(Dice(20), drop=2, of=5)  # Drop 2 lowest rolls and add together rest of 5 rolled
```

#### Reroll

Rerolls the die based on the set condition, keeping the outcome regardless of whether it is better. Reroll will only reroll the die once, for continual rerolling see `Explode` below.

This modifier requires specifying extra condition. Here is example:

```python
from dice_roller import Reroll, Dice

reroll_ones = (Reroll() == 1)
d20_reroll_ones = reroll_ones(Dice(20))
```

By default, roll can be rerolled once, but you can override this behavior during constructing `Reroll` instance:

```python
from dice_roller import r  # r is alias for Reroll

# dice may be rerolled 100 times, if has sequential ones on d20 roll
reroll_ones = (r(reroll_limit=100) == 1)
d20_reroll_ones_100_times_max = explode_on_6(Dice(6))
```

`Reroll` supports several comparison operations:

```python
from dice_roller import r

reroll_on_6 = (r() == 6)
reroll_on_gt_5 = (r() > 5)
reroll_on_ge_5 = (r() >= 5)
reroll_on_lt_5 = (r() < 5)
reroll_on_le_5 = (r() <= 5)
```

You can also provide dices for `Reroll`, let's call it "Reroll Dice". In this case, "Reroll Dice" will be rolled first, and then, if dice outcomes into required dice, it will be rerolled. "Reroll Dice" rolled after each reroll step.

```python
from dice_roller import r, RangeDice, Dice

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

Also, take into account - result of `Reroll` call is not dice itself, it is modifier wrapper. You need to apply this modifier to dice to perform rolls.

```python

from dice_roller import r, d

(r() == 1).roll()  # is not okay
(r() == 6)(d(6)).roll()  # is okay
```

#### Explode

Rerolls a die continually based on the set condition, so that each occurrence of the number rolls again, continually adding to the total result.

This modifier requires specifying extra condition. Here is example:

```python
from dice_roller import Explode, Dice

explode_on_6 = (Explode() == 6)
d6_explode_on_6 = explode_on_6(Dice(6))
```

By default, roll can be exploded 100 times, but you can override this behavior during constructing `Explode` instance:

```python
from dice_roller import x, Dice  # x is alias for Explode

# dice may be exploded only 5 times sequentially on d6 roll
# If you lucky enough, you will obtain result of `np.sum([6,6,6,6,6])`
explode_on_6 = (x(explode_depth=5) == 6)
d6_explode_on_6_5_times = explode_on_6(Dice(6))
```

`Explode` supports several comparison operations:

```python
from dice_roller import x  # x is alias for Explode

explode_on_6 = (x() == 6)
explode_on_gt_5 = (x() > 5)
explode_on_ge_5 = (x() >= 5)
explode_on_lt_5 = (x() < 5)
explode_on_le_5 = (x() <= 5)
```

You can also provide dices for `Reroll`, let's call it "Explode Dice". In this case, "Explode Dice" will be rolled first, and then, if dice outcomes into required dice, it will be exploded. "Explode Dice" rolled after each exploding step.

```python
from dice_roller import x, RangeDice, Dice

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

Also, take into account - result of `Explode` call is not dice itself, it is modifier wrapper. You need to apply this modifier to dice to perform rolls.

```python

from dice_roller import x, d

(x() == 6).roll()  # is not okay
(x() == 6)(d(6)).roll()  # is okay
```

---

Let's create simple drawing function

```python
def roll_historgam(roll, simulations: int = 1_000_000):
    sns.histplot(roll.generate(simulations), bins=roll.max(), discrete=True, stat="count")
    plt.xticks(np.arange(roll.min(), roll.max() + 1))
    plt.show()
```
