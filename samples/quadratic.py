"""O(n^2): nested loops. Use smaller sizes, e.g. -s 100 300 1000."""

import sys

n = int(sys.argv[1])
total = 0
for i in range(n):
    for j in range(n):
        total += 1
print(total)
