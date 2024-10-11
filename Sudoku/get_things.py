from itertools import chain
from grid import grid


def get_spots():
    return list(chain(*grid))


# these retrun the row/column/box of grid items given a spot index (i)
def get_row(i):
    return grid[to_row(i)]
def get_column(i):
    return [row[to_column(i)] for row in grid]

def get_box(i):
    # each range from 0-2
    rowish = to_row(i) // 3 
    columnish = to_column(i) // 3 # changed this to //

    spots = []

    # ri is row index, ci is column index
    for ri, row in enumerate(get_rows()): # i had get_rows here before but it wasn't used anywhere else so...
        if ri in range(3*rowish, 3*rowish+3):
            for ci, spot in enumerate(row):
                if ci in range(3*columnish, 3*columnish+3):
                    spots.append(spot)
            
    return spots
    

    

def get_rows():
    return grid
def get_columns():
    return [get_column(n) for n in range(9)]
def get_boxes():
    return [get_box(n) for n in range(9)]
        
def to_row(i):
    return i // 9
def to_column(i):
    return i % 9

    
