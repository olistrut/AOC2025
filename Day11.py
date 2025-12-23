import time
import re

path_cache = {}

def dfs(nodes, start, end, forbidden, path):
    result = 0
    if (start, end, forbidden) in path_cache:
        return path_cache[(start, end, forbidden)]

    for n in nodes[start]:
        if n == end:
            return 1
        elif n not in path and n not in forbidden:
            path[n] = True
            r = dfs(nodes, n, end, forbidden, path)
            result += r
            del path[n]

    path_cache[(start, end, forbidden)] = result
    return result



def solve(filename):
    result1 = result2 = 0
    file = open(filename)
    input = file.read().strip().split("\n")

    nodes = {}
    for line in input:
        m = re.match("(\w\w\w)\:(\s.+)", line)
        source = m[1]
        nodes[source] = set(m[2].strip().split(" "))
    nodes["out"] = []

    result1 = dfs(nodes, "you", "out", (), {'you': True})

    a = dfs(nodes, "svr", "fft", ("dac"), {'svr': True})
    b = dfs(nodes, "fft", "dac", ("svr", "out"), {'fft': True})
    c = dfs(nodes, "dac", "out", ("svr", "fft"), {'dac': True})

    d = dfs(nodes, "svr", "dac", ("fft"), {'svr': True})
    e = dfs(nodes, "fft", "out", ("svr", "dac"), {'fft': True})
    f = dfs(nodes, "dac", "fft", ("svr", "out"), {'dac': True})

    result2 = a*b*c + d*e*f

    return result1, result2


start = time.time()

# filename = "input/input11-sample-part2.txt"
# p1, p2 = solve(filename)
# print("Part 1 (Example): ", p1)
# print("Part 2 (Example): ", p2)

filename = "input/input11.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print("Part 2 (Data): ", p2)

print("Total time: ", time.time() - start)

