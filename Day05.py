import time

def solve(filename):
    result1 = result2 = 0
    file = open(filename)
    range_input, item_input = file.read().strip().split("\n\n")

    ranges = []

    fresh = set()

    for current_range in range_input.strip().split("\n"):
        l, r = map(int, current_range.split("-"))
        ranges.append((l, r))


    # Part 1
    for item in map(int, item_input.split("\n")):
        for current_range in ranges:
            if (item >= current_range[0] and item <= current_range[1]):
                result1 += 1
                break

    # Part 2

    # Merge overlapping ranges
    merged_ranges = []
    ranges.sort()
    merged_ranges.append(ranges.pop(0))
    last_merged = merged_ranges[0]

    for current_range in ranges:
        l = last_merged[0]
        r = last_merged[1]
        l_current = current_range[0]
        r_current = current_range[1]

        if l_current <= r:
            # overlaps with existing range - merge
            merged_ranges[-1] = (l, max(r, r_current))
            last_merged = merged_ranges[-1]
        else:
            # no overlap - add new range
            merged_ranges.append(current_range)
            last_merged = current_range

    for current_range in merged_ranges:
        result2 += (current_range[1] - current_range[0] + 1)

    return result1, result2

start = time.time()

filename = "input/input05-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)

filename = "input/input05.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print("Part 2 (Data): ", p2)

print("Total time: ", time.time() - start)
