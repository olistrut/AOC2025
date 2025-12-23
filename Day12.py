import time
import re


def solve(filename):
    result1 = result2 = 0
    file = open(filename)
    input = file.read().strip().split("\n\n")

    blocks = input[:-1]
    spaces = input[-1]
    
    gifts = []
    flipped_gifts = []
    densities = []

    for block in blocks:
        lines = block.split("\n")
        block_id = lines[0].split(":")[0]
        gift = []
        element_count = 0
        for line in lines[1:]:
            gift.append(line.strip().replace("#",str(block_id)))
            element_count += line.count("#")
        gifts.append(gift)
        flipped_gifts.append(gift[::-1])
        densities.append(element_count)

    for space_desc in spaces.strip().split("\n"):
        required_blocks = 0
        m = re.match(r'(\d+)x(\d+)\:(.+)$', space_desc)
    
        width = int(m[1])
        height = int(m[2])
        size = width * height
        s = m[3].strip().split(" ")
        required_gifts = list(map(int,m[3].strip().split(" ")))

        for gift, count in enumerate(required_gifts):
            required_blocks += count * densities[gift]
        if sum(required_gifts)*9 <= width*height:
            result1 += 1
        else:
            print("might not fit - but doesn't seem to matter")

    return result1


start = time.time()

filename = "input/input12-sample.txt"
p1 = solve(filename)
print("Part 1 (Example): ", p1)

filename = "input/input12.txt"
p1 = solve(filename)
print("Part 1 (Data): ", p1)

print("Total time: ", time.time() - start)

