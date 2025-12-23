import time
import math
import itertools
from collections import deque

def solve(filename):
    result1 = result2 = 0
    file = open(filename)
    input = file.read().strip().split("\n")

    red_coordinates = []
    field = {}
    rects = []
    min_x, min_y = 0, 0

    width = height = 0

    last_corner = None
    edges = []

    for line in input:
        x, y = map(int, line.strip().split(","))
        red_coordinates.append((x, y))
        if x < min_x or min_x == 0:
            min_x = x
        if y < min_y or min_y == 0:
            min_y = y

        if x > width:
            width = x
        if y > height:
            height = y
        field[(x, y)] = "r"

        # Construct edges (only used temporarily)
        if last_corner != None:
            edges.append((last_corner, (x,y)))
        last_corner = (x, y)

    # As we build the field, we trace both  an inner and outer border - we don't know yet which one will 
    # be inner and which one will be outer
    borders_1 = []
    borders_2 = []
    last_direction = None
    edges.append((edges[-1][1],edges[0][0]))
    edges.append(edges[0])

    # print("Edges:", edges)
    for last_edge, cur_edge in itertools.pairwise(edges):
        if last_edge[0][0] > last_edge[1][0]:
            last_direction = "left"
        elif last_edge[0][0] < last_edge[1][0]:
            last_direction = "right"
        elif last_edge[0][1] > last_edge[1][1]:
            last_direction = "up"
        else:
            last_direction = "down"

        x1 = cur_edge[0][0]
        y1 = cur_edge[0][1]
        x = cur_edge[1][0]
        y = cur_edge[1][1]
        # Construct inner and outer border
        
        if cur_edge[1][0] > cur_edge[0][0]:
            direction = "right"
            if last_direction == "up":
                borders_1.append(((x1-1, y1), (x1-1, y1)))
                borders_1.append(((x1, y1-1), (x-1, y-1)))
                borders_2.append(((x1+1, y1+1), (x-1, y1+1)))
            elif last_direction == "down":
                borders_1.append(((x1+1, y1-1), (x-1, y-1)))
                borders_2.append(((x1-1, y1), (x1-1, y1)))
                borders_2.append(((x1, y1+1), (x, y+11)))
            
        elif cur_edge[1][0] < cur_edge[0][0]:
            direction = "left"
            if last_direction == "up":
                borders_1.append(((x1-1, y1+1), (x+1, y+1)))
                borders_2.append(((x1+1, y1), (x1+1, y)))
                borders_2.append(((x1, y1-1), (x, y-1)))

            elif last_direction == "down":
                borders_1.append(((x1, y1+1), (x+1, y+1)))
                borders_2.append(((x1-1, y1-1), (x, y-1)))

        elif cur_edge[1][1] > cur_edge[0][1]:
            direction = "down"
            if last_direction == "right":
                borders_1.append(((x1, y1-1), (x1, y1-1)))
                borders_1.append(((x1+1, y1), (x+1, y)))
                borders_2.append(((x1-1, y1+1), (x-1, y-1)))

            else:
                borders_1.append(((x1+1, y1+1), (x+1, y-1)))
                borders_2.append(((x1, y1-1), (x, y1-1)))
                borders_2.append(((x1-1, y1), (x-1, y-1)))

        elif cur_edge[1][1] < cur_edge[0][1]:
            direction = "up"
            if last_direction == "right":
                borders_1.append(((x1-1, y1-1), (x-1, y+1)))
                borders_2.append(((x1+1, y1), (x+1, y)))
                borders_2.append(((x1, y1+1), (x1, y1+1)))

            else:
                borders_1.append(((x1, y1+1), (x1, y1+1)))
                borders_1.append(((x1-1, y1), (x-1, y+1)))
                borders_2.append(((x1+1, y1-1), (x+1, y+1)))
                # missing b2

    for r1, r2 in itertools.combinations(red_coordinates, 2):
        area = abs(r1[0] - r2[0] + 1) * abs(r1[1] - r2[1] + 1)
        rects.append((r1, r2))
        if area > result1:
            result1 = area


    red_coordinates.append(red_coordinates[0])
    for r1, r2 in itertools.pairwise(red_coordinates):
        if r1[0] == r2[0] or r1[1] == r2[1]:
            for x in range(min(r1[0], r2[0] + 1), max(r1[0], r2[0]) + 1):   
                for y in range(min(r1[1], r2[1] + 1), max(r1[1], r2[1]) + 1):
                    if (x, y) not in field:
                        field[(x, y)] = "g"

    print("Border done")

    for i, border in enumerate(borders_1):
        for x in range(min(border[0][0], border[1][0] ), max(border[0][0], border[1][0]) + 1):   
            for y in range(min(border[0][1], border[1][1] ), max(border[0][1], border[1][1]) + 1):
                field[(x, y)] = 1

    for border in borders_2:
        for x in range(min(border[0][0], border[1][0] + 1), max(border[0][0], border[1][0]) + 1):   
            for y in range(min(border[0][1], border[1][1] + 1), max(border[0][1], border[1][1]) + 1):
                field[(x, y)] = 2

    # Determine which one of our borders is the relevant outer border
    border_found = False
    borders = None
    for y in range(min_y-1, height+1):
        for x in range(min_x-1, width+1):
            if (x, y) in field:
                if field[(x, y)] == 1:
                    borders = borders_1
                    print("1 is outer border")
                elif field[(x, y)] == 2:
                    borders = borders_2
                    print("2 is outer border")
                else:
                    print("Found inside before border 1")
                border_found = True
                break
        if border_found:
            break
    
    # for y in range(height + 2):
    #     print(str(y).rjust(2, '0') , end = "")
    #     for x in range(width + 2):
    #         if (x,y) in field:
    #             print(field[(x, y)], end="")
    #         else:
    #             print(".", end="")
    #     print("")

    print("Testing rectangles against borders for ", len(rects), "rectangles and", len(borders), "borders")
    for r1, r2 in rects:
        if (abs(r1[0] - r2[0]) + 1) * (abs(r1[1] - r2[1]) + 1) <= result2:
            continue
        
        rect_borders = [ ((r1[0], r1[1]), (r1[0], r2[1])),
                         ((r1[0], r2[1]), (r2[0], r2[1])),
                         ((r2[0], r2[1]), (r2[0], r1[1])),
                         ((r2[0], r1[1]), (r1[0], r1[1])) ]
        
        # Check if any of lines specified by the points in rect_borders intersects with a border
        intersection = False
        for rect_edge in rect_borders:
            for border in borders:
                # print("Border: ",b, " - ",border)
                border_start = border[0]
                border_end = border[1]
                edge_start = rect_edge[0]
                edge_end = rect_edge[1]
                # check if the lines specified by the points start_1 and end_1 and start_2 and end_2 intersect
                dir_1 = "vertical" if border_start[0] == border_end[0] else "horizontal"
                dir_2 = "vertical" if edge_start[0] == edge_end[0] else "horizontal"

                if dir_1 != dir_2:
                    # No intersection possible if edges are parallel
                    if dir_1 == "vertical":
                        if (max(edge_start[1], edge_end[1]) >= min(border_start[1], border_end[1])) and (min(edge_start[1], edge_end[1]) <= max(border_start[1], border_end[1])) and (max(edge_start[0], edge_end[0]) > min(border_start[0], border_end[0])) and (min(edge_start[0], edge_end[0]) < max(border_start[0], border_end[0])):
                            intersection = True
                            break
                    elif dir_1 == "horizontal":
                        if (max(edge_start[1], edge_end[1]) > min(border_start[1], border_end[1])) and (min(edge_start[1], edge_end[1]) < max(border_start[1], border_end[1])) and (max(edge_start[0], edge_end[0]) >= min(border_start[0], border_end[0])) and (min(edge_start[0], edge_end[0]) <= max(border_start[0], border_end[0])):
                            intersection = True
                            break

            if intersection:
                break

        if not intersection:
            area = (abs(r1[0] - r2[0]) + 1) * (abs(r1[1] - r2[1]) + 1)
            if area > result2:
                result2 = area

    return result1, result2


start = time.time()

filename = "input/input09-sample.txt"
# filename = "input/input09-sample-extra.txt"

p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)



filename = "input/input09.txt"
p1, p2 = solve(filename)
# 1396463530 is too low
# 2567906509 is too high
# 2031536924 is too high
print("Part 1 (Data): ", p1)
print("Part 2 (Data): ", p2)

print("Total time: ", time.time() - start)


