import time
import math

def solve(filename):
    result1 = result2 = 0
    file = open(filename)
    lines = file.read().strip().split("\n")
    
    columns = None

    for line in lines:
        elements = line.strip().split()

        if columns is None:
            col_count = len(elements)
            columns = [[] for _ in range(col_count)]
            operators = ["" for _ in range(col_count)]
        for i, element in enumerate(elements):
            if element not in ["+", "*"]:
                columns[i].append(int(element))

    operators = lines[-1].strip().split()        
    del(lines[-1])
    for i, c in enumerate(columns):
        if operators[i] == "+":
            result1 += sum(c)
        elif operators[i] == "*":
            result1 += math.prod(c) 

    width = len(lines[0])
    op_index = len(operators) -1
    numbers = []
    for i in range(width - 1, -1, -1):
        cur_number_str = ""
        for line in lines:
            if line[i].isdigit():
                cur_number_str += line[i]
        if cur_number_str != "":
            numbers.append(int(cur_number_str))

        if cur_number_str == "" or i == 0:
 
            if op_index >= 0:
                op = operators[op_index]
                # print("Operation:", op, " on", numbers, end=" => ")
                if op == "+":
                    result2 += sum(numbers)
                    # print(sum(numbers))
                elif op == "*":
                    result2 += math.prod(numbers)
                    # print(math.prod(numbers))
                numbers = []
                op_index -= 1
            else:
                print("Error: more numbers than operators")

    
    return result1, result2

start = time.time()

filename = "input/input06-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)

filename = "input/input06.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print("Part 2 (Data): ", p2)

print("Total time: ", time.time() - start)
