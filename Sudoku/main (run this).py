from itertools import chain, product
from grid import grid
from get_things import *


class Solver:
    def __init__(s):
        s.update()
        
    def update(s, need_to_unlistify = True):
        if need_to_unlistify:
            
            # turns all the single item lists into ints
            for i, spot in enumerate(get_spots()): # gets_spots() bc s.spots isn't updated yet
                if type(spot) == list and len(spot) == 1:
                    grid[to_row(i)][to_column(i)] = spot[0]

            s.spots = get_spots()

    def strategy_1(s):
        # removes spot options that directly conflict with already solved spots, ex if there is already a 6 in that column remove it from the possibilities

        for i, spot in enumerate(s.spots):
            if type(spot) == list:
                
                # nos is numbers that can't be in that spot
                NOs = list(chain(get_row(i), get_column(i),get_box(i)))
                NOs = set([spot for spot in NOs if type(spot) == int])
                to_remove = NOs & set(spot)

                if to_remove:
                    spots = [option for option in spot if not option in to_remove]
                    grid[to_row(i)][to_column(i)] = spots

                    s.update()
                    return True # progress was made even if a square wasn't decided

    def strategy_2(s):
        # if a spot is the only spot where a certain number fits within its section, then solve that spot with that number
        for i, spot in enumerate(s.spots):
            if not type(spot) == list:
                continue
            
            # all the numbers that are left to solve within each section, including duplicates
            row_candidates = list(chain(*[spot2 for spot2 in get_row(i) if type(spot2) == list]))
            column_candidates = list(chain(*[spot2 for spot2 in get_column(i) if type(spot2) == list]))
            box_candidates = list(chain(*[spot2 for spot2 in get_box(i) if type(spot2) == list]))

            for candidates in [row_candidates,column_candidates,box_candidates]:
                # the values within the current section that also can be in the current spot
                intersection = set(spot) & set(candidates)
                # if a value from intersection only occurs once in the section, then it is the only place where that number could occur within the section, so solve it
                unique = [value for value in intersection if candidates.count(value)==1]
                if unique:
                    grid[to_row(i)][to_column(i)] = unique[0]
                    s.update(False)
                    return True


solver = Solver()
while list in [type(spot) for spot in solver.spots]:
    # don't mess with this running system
    if solver.strategy_1():
        continue
    elif solver.strategy_2():
        continue
    else:
        break # giving up


print('End')  # not guarenteed that it is solved
for row in get_rows():
    to_print = []
    for spot in row:
        if type(spot) == list:
            to_print.append('.')
        else:
            to_print.append(spot)
    print(*to_print)