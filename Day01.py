import time

def solve(filename):
    file = open(filename)
    lines = file.read().split("\n")
    pos = 50
    result1 = result2 = 0
    for line in lines:
        dir = line[0]
        length = int((line[1:]).strip())
        if dir == "L":
            leftZ = 0

            if length >= pos and pos > 0:
                leftZ += 1
                length = length - pos
                pos = 0
                
            leftZ += length // 100
            pos = (pos - length) % 100
            result2 += leftZ
            # print("The dial is rotated ", dir, int((line[1:]).strip()), "to point at ",pos, "passing zero ", abs(leftZ), "times")
        else:
            result2 += (pos + length) // 100
            pos = (pos + length) % 100
            # print("The dial is rotated ", dir, length, "to point at ",pos, "passing zero ", (pos + length) // 100, "times")

        if pos == 0:
            result1 += 1

    return result1, result2


start = time.time()

filename = "input/input01-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)


filename = "input/input01.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print("Part 2 (Data): ", p2)

print("Total time: ", time.time() - start)
