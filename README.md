# AlphaZero Variant - A Self-Learning Computer on a Game of Chance

## Programming Assignment 3

This is a program that learns to play a simple game of chance in somewhat the same way that the AlphaZero program learned to play chess, Go, and other games. The game is a variant of the card game “Blackjack”. Two players alternately roll dice, and keep track of their total across turns. They are each trying to reach a sum that lies in a specified target, between a fixed low value and high value. If a player reaches a score in the target range, they immediately win. If they exceed the high value, they immediately lose. The players can choose the number of dice to roll on each turn, between 1 and a fixed maximum. The game thus has four parameters:

- NSides, The number of sides of the die. The die is numbered 1 to NSides and all outcomes are equally likely.
- LTarget, the lowest winning value.
- UTarget, the highest winning value.
- NDice, the maximum number of dice a player may roll.

## Running the program

### Requirements

Any version of Python 3 is required. The program was tested on Python 3.11.2.

### How to run

The program accepts the following arguments:

```
NDice = int(sys.argv[1])
NSides = int(sys.argv[2])
LTarget = int(sys.argv[3])
UTarget = int(sys.argv[4])
M = float(sys.argv[5])
NGAMES = int(sys.argv[6])
```

Therefore, run the program with the following command:

```
python3 main.py NDice NSides LTarget UTarget M NGAMES
```

For example, to run the program with 2 dice, 3 sides, a lower target of 6, an upper target of 7, a hyperparameter M of 100, and 100,000 games, run the following command:

```
python3 main.py 2 3 6 7 100 100000
```

## Output

The program output will be written to a file called `output.txt` located in the same directory as the program.
