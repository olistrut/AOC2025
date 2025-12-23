import time

cache = {}
visited_splitters = set()


def dfs(input, depth, start_pos):

    if depth == len(input)-1:
        return 0, 1

    total_paths = 0
    row = input[depth + 1]

    if row[start_pos] == ".":
        _, increment = dfs(input, depth + 1, start_pos)
        cache[(depth + 1, start_pos)] = increment
        total_paths += increment
    elif row[start_pos] == "^":
        if (depth + 1, start_pos) not in visited_splitters:
            visited_splitters.add((depth + 1, start_pos))
        if (depth+1, start_pos-1) not in cache:
            _, increment1 = dfs(input, depth + 1, start_pos - 1)
            cache[(depth + 1, start_pos - 1)] = increment1
        total_paths += cache[(depth + 1, start_pos - 1)]

        if (depth+1, start_pos + 1) not in cache:
            _, increment2 = dfs(input, depth + 1, start_pos + 1)
            cache[(depth + 1, start_pos + 1)] = increment2
        total_paths += cache[(depth + 1, start_pos + 1)]

    return len(visited_splitters), total_paths


def solve(filename):
    global cache
    cache = {}
    global visited_splitters
    visited_splitters = set()

    file = open(filename)
    input = file.read().strip().split("\n")

    return dfs(input, 0, input[0].index("S"))


start = time.time()

filename = "input/input07-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)

filename = "input/input07.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print("Part 2 (Data): ", p2)

print("Total time: ", time.time() - start)
