"""O(n): one pass over the input size."""

import sys

n = int(sys.argv[1])
total = 0
for i in range(n):
    total += i
print(total)
