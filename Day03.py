import time

def highest_n(bank, n):
    bank = list(map(int, bank))
    result = ""
    pos = 0
    for i in range(n, 0, -1):
        digit = max(bank[pos:len(bank) - i + 1])
        pos = pos + bank[pos:].index(digit) + 1
        result += str(digit)      
    return int(result)

def solve(filename):
    result1 = result2 = 0
    file = open(filename)
    banks = file.read().strip().split()
    for bank in banks:
        result1 += highest_n(bank, 2)
        result2 += highest_n(bank, 12)

    return result1, result2


start = time.time()

filename = "input/input03-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)

filename = "input/input03.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print("Part 2 (Data): ", p2)

print("Total time: ", time.time() - start)
