import time
from collections import defaultdict

def remove_rolls(map, width, height):
    neighbours = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]

    del_count = 0
    new_map = defaultdict(lambda: defaultdict(lambda: 0))

    for y in range(height):
        for x in range(width):
            count = 0
            if map[x][y] == 1:
                for dx, dy in neighbours:
                    count += map[x + dx][y + dy]
                if count < 4:
                    del_count += 1
                else:
                    new_map[x][y] = 1
    
    if del_count == 0:
        return 0, 0
    else:
        return del_count, del_count + remove_rolls(new_map, width, height)[1]


def solve(filename):
    result1 = result2 = 0
    file = open(filename)
    rows = file.read().strip().split()
    map = defaultdict(lambda: defaultdict(lambda: 0))

    y = 0
    for row in rows:
        x = 0
        for c in row:
            if c == "@":
                map[x][y] = 1
            else:
                map[x][y] = 0
            x += 1
        y += 1

    return remove_rolls(map, x, y) 


start = time.time()

filename = "input/input04-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)

filename = "input/input04.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print("Part 2 (Data): ", p2)

print("Total time: ", time.time() - start)
