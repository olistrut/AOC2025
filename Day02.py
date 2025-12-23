import time

def solve(filename):
    result1 = result2 = 0
    file = open(filename)
    pairs = file.read().strip().split(",")
    for pair in pairs:
        for e1, e2 in [pair.split("-")]:
            for num in range(int(e1), int(e2) + 1):
                element = str(num)
                digits = len(element)
                # Part 1 original string solution
                # if element[0:len(element) // 2] * 2 == element: 
                #     result1 += num
                
                # Part 1 integer solution
                if num % pow(10, digits // 2) == num // pow(10, digits // 2):
                    result1 += num

                for chunk_len in range(1, digits // 2 + 1):
                    if digits % chunk_len == 0:    # slights optimization to skip chunk lengths that won't fit the full string
                        # So far fastest solution
                        head = element[0:chunk_len]
                        if head * (digits // chunk_len) == element:
                            result2 += num
                            break

                        # Math - invalid IDs (with repeated chunks) are all of the form abc x "1001001" etc
                        # Building up the multipliers and multiplying with the first n digits to check equality 
                        # This is super slow, however
                        # multiplier = int(str(pow(10, chunk_len - 1)) * (digits // chunk_len - 1)) * 10 + 1
                        # head = num // pow(10, digits - chunk_len)
                        # if head * multiplier == num:
                        #     result2 += num
                        #     break

                        # Slowest and original solution
                        # if all (element[i:i + chunk_len] == element[0:chunk_len] for i in range(chunk_len, digits, chunk_len)):
                        #     result2 += num
                        #     break # to avoid double-counting if an id fulfils criteria for different chunk lenghts

    return result1, result2


start = time.time()

filename = "input/input02-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)

filename = "input/input02.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print("Part 2 (Data): ", p2)

print("Total time: ", time.time() - start)
