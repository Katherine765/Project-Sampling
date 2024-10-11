grid =   [[0,7,0,0,8,0,0,0,0],
        [0,1,0,0,0,0,0,3,0],
        [0,0,6,7,0,9,4,0,0],
        [0,0,8,0,4,0,0,0,0],
        [0,0,0,0,5,0,2,0,0],
        [0,6,0,8,9,2,0,0,1],
        [0,0,7,2,0,6,9,0,0],
        [0,0,0,0,0,5,0,0,0],
        [9,0,0,0,0,0,0,0,5]]



print('Beginning')
for row in grid:
    to_print = []
    for spot in row:
        if spot == 0:
            to_print.append('.')
        else:
            to_print.append(spot)
    print(*to_print)

# sets up grid for use in main program
for i, row in enumerate(grid):
    for j, spot in enumerate(row):
        if spot == 0:
            grid[i][j] = list(range(1,10))

