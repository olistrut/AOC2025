import numpy as np
import time
import re
from sympy import symbols
import sympy
from sympy import Matrix, solve_linear_system
from copy import deepcopy
import numpy as np

def multi_choose(k, n):
 if k==0:
    return [[0] * n]
 elif n==0:
    return []
 elif n == 1:
   return [[k]]
 else:
    out = []
    if (k, n-1) in multi_choose_dict:
        r = multi_choose_dict[(k, n-1)]
    else:
        r = multi_choose(k, n-1)

    for res in r:
        res = [0] + res
        out.append(res)

    if (k-1, n) in multi_choose_dict:
        r = deepcopy(multi_choose_dict[(k-1, n)])
    else:
        r = multi_choose(k-1, n)
        
    for res in r:
        res[0] += 1
        out.append(res)

    if (k, n) not in multi_choose_dict:
        multi_choose_dict[(k, n)] = out
    return out


multi_choose_dict = {}
def solve(filename):
    result1 = result2 = 0
    file = open(filename)
    input = file.read().strip().split("\n")

    for line_number, line in enumerate(input):
        m = re.search("\[([\.\#]+)\]\s(\(.*\))\s\{(.*)\}", line)
        pattern = m[1]
        schematics = m[2].split(" ")
        joltage = list(map(int, m[3].split(",")))

        vectors = []
        for s in schematics:
            vectors.append([0] * len(pattern))
            s = s[1:-1]
            for button in s.split(","):
                vectors[-1][int(button)] = 1
        
        matrix_list = []
        for i in range(len(pattern)):
            matrix_row = []
            for v in vectors:
                matrix_row.append(v[i])
            matrix_row.append(joltage[i])
            matrix_list.append(matrix_row)
        matrix = Matrix(matrix_list)

        # Part 2
        s = sympy.symbols("x0:"+str(len(schematics)))
        r = sympy.solve_linear_system(matrix, *s)
        matrix = matrix.echelon_form()

        # count unsolved variables
        underdefined = set()
        constant_sum = 0
        for v in r.values():
            m = re.findall("(x[0-9]+)", str(v))
            for u in m:
                underdefined.add(u)
            if len(m) == 0:
                if type(v) == sympy.Integer or float(v).is_integer():
                    constant_sum += v

                
        if len(underdefined) == 0:
            line_solution = 0
            for var_sol in r.values():
                line_solution += var_sol

            result2 += sum(r.values())

        elif len(underdefined) in [1, 2, 3]:
            min_solution = 99999999

            underdefined_vars = []
            for v in underdefined:
                underdefined_vars.append(int(v[1:]))
            max_switched = 0
            for i in range(len(pattern)):
                for j in underdefined_vars:
                    if vectors[j][i] != 0:
                        if joltage[i] > max_switched:
                            max_switched = joltage[i]

            matrix_rows = []
            b = []
            for i in range(matrix.shape[0]):
                matrix_row = list(map(float, matrix.row(i)[0:-1]))
                if any(x != 0 for x in matrix_row):
                    matrix_rows.append(matrix_row)
                    b.append(float(matrix.row(i)[-1]))
            A = np.array(matrix_rows)
            b = np.array(b)

            for v in underdefined_vars:
                new_row = [0] * len(schematics)
                new_row[v] = 1
                A = np.vstack([A, new_row])
                b = np.append(b, 0)
                
            for i in range(max_switched):
                if i + constant_sum> min_solution:
                    break
                for j in range(min(max_switched, 1 if len(underdefined)<=1 else max_switched)):
                    if j + constant_sum> min_solution:
                        break
                    if i + j  + constant_sum>= min_solution:
                        continue
                    for k in range(min(max_switched, 1 if len(underdefined)<=2 else  max_switched)):
                        if i + j + k + constant_sum>= min_solution:
                            break

                        if len(underdefined) == 3:
                            b[-3] = k
                        if len(underdefined) >= 2:
                            b[-2] = j
                        b[-1] = i
                        result = np.linalg.solve(A, b)
                        if all (abs(x-round(x)) < 0.1 and x>=0 for x in result):
                            tmp_solution = sum(result)
                            if tmp_solution < min_solution:
                                min_solution = tmp_solution

            result2 += int(min_solution)


        else:
            print("=> ERROR - More than three underdefined variables")

        # Part 1
        found_1 = False
        n = 0
        while not (found_1):
            multipliers = multi_choose(n, len(vectors))
            light_target = [0] * len(pattern)
            for pos, c in enumerate(pattern):
               if c == "#":
                  light_target[pos] = 1

            # add the multiplication of each multiplier with each vector to lights (mod 2)      
            # then compare 

            for multiplier in multipliers:
                lights_1 = [0] * len(pattern)
                lights_2 = [0] * len(pattern)

                for i, change in enumerate(multiplier):
                    # change = multiplier[i]
                    vector = vectors[i]
                    for j in range(len(pattern)):
                        lights_1[j] += change * vector[j]
                        lights_1[j] = lights_1[j] % 2
                        lights_2[j] += change * vector[j]

                if lights_1 == light_target:
                    found_1 = True
                    result1 += n


                if found_1:
                   break

            n += 1    
    
    return result1, result2

start = time.time()

filename = "input/input10-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)

filename = "input/input10.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print("Part 2 (Data): ", p2)

print("Total time: ", time.time() - start)
