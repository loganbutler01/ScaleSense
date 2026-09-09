"""Run a Python program at different input sizes and see how fast the runtime grows."""

import math
import subprocess
import sys
import time

DEFAULT_SIZES = [1000000, 3000000, 10000000]
RUNS_PER_SIZE = 3
STARTUP_RUNS = 15  # startup is cheap to measure, and every size depends on it
TIME_LIMIT = 60  # seconds allowed for a single run


def run_and_time(command, runs=RUNS_PER_SIZE):
    """Run a command a few times and return the fastest time, in seconds.

    Other programs on the computer steal time from ours at random, so a single
    measurement can come out much too slow. The fastest one is the cleanest.
    """
    seconds = []
    for _ in range(runs):
        start = time.perf_counter()
        result = subprocess.run(command, capture_output=True, text=True, timeout=TIME_LIMIT)
        seconds.append(time.perf_counter() - start)
        if result.returncode != 0:
            print(result.stderr)
            sys.exit("That program crashed, so there is nothing to measure.")
    return min(seconds)


def growth_exponent(sizes, times):
    """Find the k in  time = size ** k, comparing the first run to the last.

    k = 1 means 10x the input gives 10x the time.
    k = 2 means 10x the input gives 100x the time.

    Dividing by the log of the size span is why sizes that are close together
    give jumpy answers: the same timing wobble is divided by a smaller number.
    """
    return math.log(times[-1] / times[0]) / math.log(sizes[-1] / sizes[0])


def main():
    arguments = sys.argv[1:]
    if len(arguments) == 0:
        sys.exit("usage: scalecheck PROGRAM.py [SIZE SIZE SIZE ...]")

    program = arguments[0]
    if len(arguments) > 1:
        sizes = [int(argument) for argument in arguments[1:]]
    else:
        sizes = DEFAULT_SIZES

    if len(sizes) < 2:
        sys.exit("Give at least two sizes, so there is something to compare.")

    # Starting Python costs about 10-30 ms, which is more than a small run of
    # the program itself. Measure it once and subtract it from every run.
    startup = run_and_time([sys.executable, "-c", ""], runs=STARTUP_RUNS)

    times = []
    for size in sizes:
        try:
            seconds = run_and_time([sys.executable, program, str(size)]) - startup
        except subprocess.TimeoutExpired:
            sys.exit(
                f"\nSize {size} took longer than {TIME_LIMIT} seconds.\n"
            )
        seconds = max(seconds, 0.000001)  # stay above zero for the math
        times.append(seconds)
        print(f"Input {size:>9} -> {seconds:.4f} sec")

    growth = growth_exponent(sizes, times)
    print(f"\nGrowth: time = size ** {growth:.2f}")

    if growth <= 1.2:
        print("Result: GOOD - the runtime grows about as fast as the input")
    elif growth <= 1.6:
        print("Result: WARNING - the runtime grows noticeably faster than the input")
    else:
        print("Result: POOR - the runtime grows much faster than the input")

    # Every time above is a measured run minus startup. When the leftover is
    # smaller than startup itself, it is a small difference between two big
    # numbers, and small errors in either one get magnified.
    if min(times) < startup:
        print(
            f"\nNote: the shortest run ({min(times):.4f} sec) was faster than Python's"
            f" own\nstartup ({startup:.4f} sec), so these numbers are rough."
        )



if __name__ == "__main__":
    main()