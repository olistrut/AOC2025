import time
import math
import itertools

def solve(filename, rounds):
    result1 = result2 = 0
    file = open(filename)
    input = file.read().strip().split("\n")

    junctions = {}
    clusters = {}

    for i, line in enumerate(input):
        x, y, z = map(int, line.split(","))
        new_junction = [(x, y, z)]
        clusters[i] = {(x, y, z)}
        junctions[(x, y, z)] = i

    distances = []
    for j1, j2 in itertools.combinations(junctions.keys(), 2):
        dist = math.sqrt(pow(j1[0]-j2[0], 2) + pow(j1[1]-j2[1], 2) + pow(j1[2]-j2[2], 2))
        distances.append((dist, j1, j2))

    distances.sort()

    i = 0
    while len(clusters) > 1:
        i += 1
        dist, j1, j2 = distances[i-1]

        if (junctions[j1] != junctions[j2]):
            clusters[junctions[j1]] = clusters[junctions[j1]].union(clusters[junctions[j2]])
            del clusters[junctions[j2]]
            for j in clusters[junctions[j1]]:
                junctions[j] = junctions[j1]

        if i == rounds:
            cluster_lengths = [len(c) for c in clusters.values()]
            cluster_lengths.sort()
            result1 = cluster_lengths[-1] * cluster_lengths[-2] * cluster_lengths[-3]
    
    result2 = j1[0] * j2[0]
        
    return result1, result2


start = time.time()

filename = "input/input08-sample.txt"
p1, p2 = solve(filename, 10)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)

filename = "input/input08.txt"
p1, p2 = solve(filename, 1000)
print("Part 1 (Data): ", p1)
print("Part 2 (Data): ", p2)

print("Total time: ", time.time() - start)
