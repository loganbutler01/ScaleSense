# ScaleSense

Runs a Python program at increasing input sizes, times each run, and reports how
fast the runtime grows compared to the input.

From *Software Engineering at Google*, "Scale and Efficiency": if costs grow
superlinearly as a system grows, the operation is not scalable. This measures one
narrow version of that idea, wall-clock runtime against input size.

## Setup

```
uv sync --dev
```

## Usage

You can run the program in one of these 3 ways.

This program is mainly supposed to be used for simple python programs.

```
uv run scalesense samples/linear.py
uv run scalesense samples/quadratic.py 300 1000 3000
uv run scalesense myprogram.py 1000000 3000000 10000000 
```

The first argument is the program. Any arguments after it are the input sizes to
try. With no sizes given it uses 1,000,000 , 3,000,000 , 10,000,000 

## Output

```
Input   1000000 -> 0.0953 sec
Input   3000000 -> 0.2975 sec
Input  10000000 -> 0.9354 sec

Growth: time = size ** 1.00
Result: GOOD - the runtime grows about as fast as the input
```

The exponent is the number being judged. `1.00` means 10x the input gives 10x the
runtime. `2.00` means 10x the input gives 100x the runtime.

| Exponent | Result |
| --- | --- |
| 1.2 or less | GOOD |
| 1.2 to 1.6 | WARNING |
| above 1.6 | POOR |

