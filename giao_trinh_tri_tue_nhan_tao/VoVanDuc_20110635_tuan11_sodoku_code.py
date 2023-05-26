# Solve Sudoku puzzles using AC-3 and Backtracking algorithms
'''
YOUR TASKS:
1. Read to understand the following code 
2. Implement the AC3() function
3. (Optional) Add GUI, animation...
4. Input a Sudoku to try your code
'''
#%%
import itertools
from operator import truediv      
import re
import random
from functools import reduce
from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE_HASH_VALUE
from statistics import variance
 

#%% Utilities
def first(iterable, default=None):
    """Return the first element of an iterable; or default."""
    return next(iter(iterable), default)

def count(seq):
    """Count the number of items in sequence that are interpreted as true."""
    return sum(map(bool, seq))

def argmin_random_tie(seq, key=lambda x: x):
    """Return a minimum element of seq; break ties at random."""
    items = list(seq)
    random.shuffle(items) #Randomly shuffle a copy of seq.
    return min(items, key=key)

def flatten(seqs):
    return sum(seqs, [])

def different_values_constraint(A, a, B, b):
    """A constraint saying two neighboring variables must differ in value."""
    return a != b


#%% CSP
class CSP():
    """This class describes finite-domain Constraint Satisfaction Problems.
    A CSP is specified by the following inputs:
        variables   A list of variables; each is atomic (e.g. int or string).
        domains     A dict of {var:[possible_value, ...]} entries.
        neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b
    """
    def __init__(self, variables, domains, neighbors, constraints):
        """Construct a CSP problem. If variables is empty, it becomes domains.keys()."""
        variables = variables or list(domains.keys())
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.curr_domains = None
        self.nassigns = 0

    def assign(self, var, val, assignment):
        """Add {var: val} to assignment; Discard the old value if any."""
        assignment[var] = val
        self.nassigns += 1
        return assignment

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]

    def nconflicts(self, var, val, assignment):
        """Return the number of conflicts var=val has with other variables."""  
        # Subclasses may implement this more efficiently
        def conflict(var2):
            return var2 in assignment and not self.constraints(var, val, var2, assignment[var2])

        return count(conflict(v) for v in self.neighbors[var])



#%% Sudoku problem
# Constants and delarations to display and work with Sudoku grid
_R3 = list(range(3))
_CELL = itertools.count().__next__
_BGRID = [[[[_CELL() for x in _R3] for y in _R3] for bx in _R3] for by in _R3]
_BOXES = flatten([list(map(flatten, brow)) for brow in _BGRID])
_ROWS = flatten([list(map(flatten, zip(*brow))) for brow in _BGRID])
_COLS = list(zip(*_ROWS))
_NEIGHBORS = {v: set() for v in flatten(_ROWS)}
for unit in map(set, _BOXES + _ROWS + _COLS):
    for v in unit:
        _NEIGHBORS[v].update(unit - {v})


class Sudoku(CSP):
    """
    A Sudoku problem.
    init_assignment is a string of 81 digits for 81 cells, row by row.  
    Each filled cell holds a digit in 1..9. Each empty cell holds 0 or '.' 
    
    For example, for the below Sodoku
    init_assignment = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..' 
    
    >>> sodoku1 = Sudoku(init_state)
    >>> sodoku1.display()
    . . 3 | . 2 . | 6 . .
    9 . . | 3 . 5 | . . 1
    . . 1 | 8 . 6 | 4 . .
    ------+-------+------
    . . 8 | 1 . 2 | 9 . .
    7 . . | . . . | . . 8
    . . 6 | 7 . 8 | 2 . .
    ------+-------+------
    . . 2 | 6 . 9 | 5 . .
    8 . . | 2 . 3 | . . 9
    . . 5 | . 1 . | 3 . .

    >>> sodoku1.display_variables()
      0  1  2  |  9 10 11  | 18 19 20
      3  4  5  | 12 13 14  | 21 22 23
      6  7  8  | 15 16 17  | 24 25 26
     --------------------------------
     27 28 29  | 36 37 38  | 45 46 47
     30 31 32  | 39 40 41  | 48 49 50
     33 34 35  | 42 43 44  | 51 52 53
     --------------------------------
     54 55 56  | 63 64 65  | 72 73 74
     57 58 59  | 66 67 68  | 75 76 77
     60 61 62  | 69 70 71  | 78 79 80

    >>> AC3(sodoku1); sodoku1.display()
    4 8 3 | 9 2 1 | 6 5 7
    9 6 7 | 3 4 5 | 8 2 1
    2 5 1 | 8 7 6 | 4 9 3
    ------+-------+------
    5 4 8 | 1 3 2 | 9 7 6
    7 2 9 | 5 6 4 | 1 3 8
    1 3 6 | 7 9 8 | 2 4 5
    ------+-------+------
    3 7 2 | 6 8 9 | 5 1 4
    8 1 4 | 2 5 3 | 7 6 9
    6 9 5 | 4 1 7 | 3 8 2
    """

    R3 = _R3
    Cell = _CELL
    bgrid = _BGRID
    boxes = _BOXES
    rows = _ROWS
    cols = _COLS
    neighbors = _NEIGHBORS    
   
    def __init__(self, grid):  #voi grid la init_assign_easy

        """Build a Sudoku problem from a string representing the grid:
        the digits 1-9 denote a filled cell, '.' or '0' an empty one;
        other characters are ignored."""
        
        squares = re.findall(r'\d|\.', grid)            

        # NOTE: For variables in order of in order of 3x3 BOXES:
        domains = {var: list(ch) if ch in '123456789' else list('123456789')
                   for var, ch in zip(flatten(self.rows), squares)} #tien hanh thiet lap mien gia tri cho moi o trong sodoku
        
        if len(squares) > 81:
            raise ValueError("Not a Sudoku grid", grid)  # Too many squares

        # For variables in order of in order of 3x3 BOXES:
        neighbors = {0: {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 27, 30, 33, 54, 57, 60}, 1: {0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 28, 31, 34, 55, 58, 61}, 2: {0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 29, 32, 35, 56, 59, 62}, 9: {0, 1, 2, 66, 69, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 36, 39, 42, 63}, 10: {0, 1, 2, 64, 67, 70, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 37, 40, 43}, 11: {0, 1, 2, 65, 68, 71, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 38, 41, 44}, 18: {0, 1, 2, 72, 9, 10, 11, 75, 78, 19, 20, 21, 22, 23, 24, 25, 26, 45, 48, 51}, 19: {0, 1, 2, 9, 10, 11, 73, 76, 79, 18, 20, 21, 22, 23, 24, 25, 26, 46, 49, 52}, 20: {0, 1, 2, 9, 10, 11, 74, 77, 80, 18, 19, 21, 22, 23, 24, 25, 26, 47, 50, 53}, 3: {0, 1, 2, 4, 5, 6, 7, 8, 12, 13, 14, 21, 22, 23, 27, 30, 33, 54, 57, 60}, 4: {0, 1, 2, 3, 5, 6, 7, 8, 12, 13, 14, 21, 22, 23, 28, 31, 34, 55, 58, 61}, 5: {0, 1, 2, 3, 4, 6, 7, 8, 12, 13, 14, 21, 22, 23, 29, 32, 35, 56, 59, 62}, 12: {66, 3, 4, 5, 69, 9, 10, 11, 13, 14, 15, 16, 17, 21, 22, 23, 36, 39, 42, 63}, 13: {64, 3, 4, 5, 67, 70, 9, 10, 11, 12, 14, 15, 16, 17, 21, 22, 23, 37, 40, 43}, 14: {65, 3, 4, 5, 68, 71, 9, 10, 11, 12, 13, 15, 16, 17, 21, 22, 23, 38, 41, 44}, 21: {3, 4, 5, 72, 75, 12, 13, 14, 78, 18, 19, 20, 22, 23, 24, 25, 26, 45, 48, 51}, 22: {3, 4, 5, 73, 12, 13, 14, 76, 79, 18, 19, 20, 21, 23, 24, 25, 26, 46, 49, 52}, 23: {3, 4, 5, 74, 12, 13, 14, 77, 80, 18, 19, 20, 21, 22, 24, 25, 26, 47, 50, 53}, 6: {0, 1, 2, 3, 4, 5, 7, 8, 15, 16, 17, 24, 25, 26, 27, 30, 33, 54, 57, 60}, 7: {0, 1, 2, 3, 4, 5, 6, 8, 15, 16, 17, 24, 25, 26, 28, 31, 34, 55, 58, 61}, 8: {0, 1, 2, 3, 4, 5, 6, 7, 15, 16, 17, 24, 25, 26, 29, 32, 35, 56, 59, 62}, 15: {66, 69, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 24, 25, 26, 36, 39, 42, 63}, 16: {64, 67, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 24, 25, 26, 70, 37, 40, 43}, 17: {65, 68, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 24, 25, 26, 38, 71, 41, 44}, 24: {6, 7, 8, 72, 75, 78, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 26, 45, 48, 51}, 25: {6, 7, 8, 73, 76, 79, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 46, 49, 52}, 26: {6, 7, 8, 74, 77, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 80, 47, 50, 53}, 27: {0, 3, 6, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 54, 57, 60}, 28: {1, 4, 7, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 55, 58, 61}, 29: {2, 5, 8, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 56, 59, 62}, 36: {66, 69, 9, 12, 15, 27, 28, 29, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 63}, 37: {64, 67, 70, 10, 13, 16, 27, 28, 29, 36, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47}, 38: {65, 68, 71, 11, 14, 17, 27, 28, 29, 36, 37, 39, 40, 41, 42, 43, 44, 45, 46, 47}, 45: {72, 75, 78, 18, 21, 24, 27, 28, 29, 36, 37, 38, 46, 47, 48, 49, 50, 51, 52, 53}, 46: {73, 76, 79, 19, 22, 25, 27, 28, 29, 36, 37, 38, 45, 47, 48, 49, 50, 51, 52, 53}, 47: {74, 77, 80, 20, 23, 26, 27, 28, 29, 36, 37, 38, 45, 46, 48, 49, 50, 51, 52, 53}, 30: {0, 3, 6, 27, 28, 29, 31, 32, 33, 34, 35, 39, 40, 41, 48, 49, 50, 54, 57, 60}, 31: {1, 4, 7, 27, 28, 29, 30, 32, 33, 34, 35, 39, 40, 41, 48, 49, 50, 55, 58, 61}, 32: {2, 5, 8, 27, 28, 29, 30, 31, 33, 34, 35, 39, 40, 41, 48, 49, 50, 56, 59, 62}, 39: {66, 69, 9, 12, 15, 30, 31, 32, 36, 37, 38, 40, 41, 42, 43, 44, 48, 49, 50, 63}, 40: {64, 67, 70, 10, 13, 16, 30, 31, 32, 36, 37, 38, 39, 41, 42, 43, 44, 48, 49, 50}, 41: {65, 68, 71, 11, 14, 17, 30, 31, 32, 36, 37, 38, 39, 40, 42, 43, 44, 48, 49, 50}, 48: {72, 75, 78, 18, 21, 24, 30, 31, 32, 39, 40, 41, 45, 46, 47, 49, 50, 51, 52, 53}, 49: {73, 76, 79, 19, 22, 25, 30, 31, 32, 39, 40, 41, 45, 46, 47, 48, 50, 51, 52, 53}, 50: {74, 77, 80, 20, 23, 26, 30, 31, 32, 39, 40, 41, 45, 46, 47, 48, 49, 51, 52, 53}, 33: {0, 3, 6, 27, 28, 29, 30, 31, 32, 34, 35, 42, 43, 44, 51, 52, 53, 54, 57, 60}, 34: {1, 4, 7, 27, 28, 29, 30, 31, 32, 33, 35, 42, 43, 44, 51, 52, 53, 55, 58, 61}, 35: {2, 5, 8, 27, 28, 29, 30, 31, 32, 33, 34, 42, 43, 44, 51, 52, 53, 56, 59, 62}, 42: {66, 69, 9, 12, 15, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 44, 51, 52, 53, 63}, 43: {64, 67, 70, 10, 13, 16, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 51, 52, 53}, 44: {65, 68, 71, 11, 14, 17, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 51, 52, 53}, 51: {72, 75, 78, 18, 21, 24, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 52, 53}, 52: {73, 76, 79, 19, 22, 25, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 53}, 53: {74, 77, 80, 20, 23, 26, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52}, 54: {64, 65, 0, 3, 6, 72, 73, 74, 27, 30, 33, 55, 56, 57, 58, 59, 60, 61, 62, 63}, 55: {64, 65, 1, 4, 7, 72, 73, 74, 28, 31, 34, 54, 56, 57, 58, 59, 60, 61, 62, 63}, 56: {64, 65, 2, 5, 72, 73, 74, 8, 29, 32, 35, 54, 55, 57, 58, 59, 60, 61, 62, 63}, 63: {64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 9, 12, 15, 36, 39, 42, 54, 55, 56}, 64: {65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 10, 13, 16, 37, 40, 43, 54, 55, 56, 63}, 65: {64, 66, 67, 68, 69, 70, 71, 72, 73, 74, 11, 14, 17, 38, 41, 44, 54, 55, 56, 63}, 72: {64, 65, 73, 74, 75, 76, 77, 78, 79, 80, 18, 21, 24, 45, 48, 51, 54, 55, 56, 63}, 73: {64, 65, 72, 74, 75, 76, 77, 78, 79, 80, 19, 22, 25, 46, 49, 52, 54, 55, 56, 63}, 74: {64, 65, 72, 73, 75, 76, 77, 78, 79, 80, 20, 23, 26, 47, 50, 53, 54, 55, 56, 63}, 57: {0, 66, 67, 68, 3, 6, 75, 76, 77, 27, 30, 33, 54, 55, 56, 58, 59, 60, 61, 62}, 58: {1, 66, 67, 68, 4, 7, 75, 76, 77, 28, 31, 34, 54, 55, 56, 57, 59, 60, 61, 62}, 59: {66, 67, 68, 2, 5, 8, 75, 76, 77, 29, 32, 35, 54, 55, 56, 57, 58, 60, 61, 62}, 66: {64, 65, 67, 68, 69, 70, 71, 9, 75, 76, 77, 12, 15, 36, 39, 42, 57, 58, 59, 63}, 67: {64, 65, 66, 68, 69, 70, 71, 10, 75, 76, 77, 13, 16, 37, 40, 43, 57, 58, 59, 63}, 68: {64, 65, 66, 67, 69, 70, 71, 75, 76, 77, 11, 14, 17, 38, 41, 44, 57, 58, 59, 63}, 75: {66, 67, 68, 72, 73, 74, 76, 77, 78, 79, 80, 18, 21, 24, 45, 48, 51, 57, 58, 59}, 76: {66, 67, 68, 72, 73, 74, 75, 77, 78, 79, 80, 19, 22, 25, 46, 49, 52, 57, 58, 59}, 77: {66, 67, 68, 72, 73, 74, 75, 76, 78, 79, 80, 20, 23, 26, 47, 50, 53, 57, 58, 59}, 60: {0, 3, 69, 70, 71, 6, 78, 79, 80, 27, 30, 33, 54, 55, 56, 57, 58, 59, 61, 62}, 61: {1, 4, 69, 70, 71, 7, 78, 79, 80, 28, 31, 34, 54, 55, 56, 57, 58, 59, 60, 62}, 62: {2, 69, 70, 71, 5, 8, 78, 79, 80, 29, 32, 35, 54, 55, 56, 57, 58, 59, 60, 61}, 69: {64, 65, 66, 67, 68, 70, 71, 9, 12, 78, 79, 80, 15, 36, 39, 42, 60, 61, 62, 63}, 70: {64, 65, 66, 67, 68, 69, 71, 10, 13, 78, 79, 80, 16, 37, 40, 43, 60, 61, 62, 63}, 71: {64, 65, 66, 67, 68, 69, 70, 11, 78, 79, 80, 14, 17, 38, 41, 44, 60, 61, 62, 63}, 78: {69, 70, 71, 72, 73, 74, 75, 76, 77, 79, 80, 18, 21, 24, 45, 48, 51, 60, 61, 62}, 79: {69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 80, 19, 22, 25, 46, 49, 52, 60, 61, 62}, 80: {69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 20, 23, 26, 47, 50, 53, 60, 61, 62}}
        #voi moi o trong sodocu, neighbors la nhung o cung hang hoac cung cot hoac nam trong tap 9 o
        CSP.__init__(self, list(domains.keys()), domains, neighbors, different_values_constraint)

    def display(self): # For variables in order of in order of 3x3 BOXES
        """Show a human-readable representation of the Sudoku."""
        place = 0
        if self.curr_domains is not None:
            self.domains = self.curr_domains.copy() 
        for var in self.domains.keys():
            if place%3 == 0 and place%9 != 0 :
                print('  |', end = '')
            if place%9 == 0 and place!=0:
                print('')
            if place%27 == 0 and place!=0:
                print(' --------------------------------')

            if len(self.domains[var])==1:
                print('%3s' % self.domains[var][0], end = '')
            else:
                print('  .', end = '')  
            place += 1
        print('\n')    
         
    def display_variables(self): # For variables in order of in order of 3x3 BOXES
        place = 0
        for var in self.domains.keys():
            if place%3 == 0 and place%9 != 0 :
                print('  |', end = '')
            if place%9 == 0 and place!=0:
                print('')
            if place%27 == 0 and place!=0:
                print(' --------------------------------')

            print('%3s' % var, end = '')
            
            place += 1
        print('\n')     
    

#%%  Constraint Propagation with AC3
''' IMPLEMENT THE FOLLOWING FUNCTION '''
def AC3(csp):
    """See [Figure 6.3] for the algorithm"""
    queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]} #voi moi phan tu Xi trong danh sach cac variables se co mot tap neighbors Xk
                                                                            #tien hanh lay cap giua (Xi, Xk), nghia la voi mot gia tri Xi se co Xk cap tuong ung
    csp.curr_domains = csp.domains.copy() # curr_domains: a copy of domains. We will do inference on curr_domains
    
    ''' ADD YOUR CODE HERE '''
    # print(queue)
    while len(queue) > 0: #tien hanh kiem tra xem queue co rong khong, neu rong thi tien hanh ket thuc thuat toan, con neu khong rong thi tien hanh cac buoc tiep theo
        (Xi, Xj) = queue.pop()   #tien hanh lay ra phan tu tren dau cua queue-> gan gia tri cap vua lay cho cap bien (Xi, Xj)
        if revise(csp, Xi, Xj):   #tien hanh kiem tra revise (csp, Xi, Xj) dung thi 
            if csp.domains[Xi] == 0:  #kiem tra domain cua Xi da rong chua, neu rong thi AC3 tra ve false
                return False            #neu domain cua Xi van con ton tai thi 
            for Xk in csp.neighbors[Xi] - {Xj}: #tien hanh xet tat ca neighbor cua Xi ngoai tru Xj vi Xj da duoc xet truoc do
                queue.add((Xk, Xi)) #them cap gia tri (Xk, Xi) vao queue va cho cho vong lap tiep theo

    return True  # CSP is satisfiable


def revise(csp, Xi, Xj):
    """Return true if we remove a value."""
    revised = False
    for x in csp.domains[Xi]: 
        conflict = True #voi moi gia tri trong domais Xi thi gan gia tri True cho bien conflict
        
        for y in csp.curr_domains[Xj]: #voi moi gia tri trong domains cua Xj
            if csp.constraints(Xi, x, Xj, y): #kiem tra xem neu (x,y) tuong ung voi (1 gia tri trong domain Xi, 1 gia tri trong domain Xi ) thoa constraint
                conflict = False #neu dieu kien trne thoa constraint thi gan gia tri false cho bien conflict va tien hanh thoat khoi vong lap
                break
        if conflict:  #neu bien conflict co gia true thi tien hanh loai bo gia tri x ra khoi domain cua Xi
            csp.domains[Xi].remove(x)  #neu xuat hien su loai bo gia tri, tien hanh return True cho ham
            revised = True
                
    return revised


#%%  CSP Backtracking Search  
# Variable ordering
def first_unassigned_variable(assignment, csp): #random selection
    """The default variable order."""
    return first([var for var in csp.variables if var not in assignment])

def num_legal_values(csp, var, assignment):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        return count(csp.nconflicts(var, val, assignment) == 0 for val in csp.domains[var])

def minimum_remaining_values(assignment, csp):
    """Minimum-remaining-values heuristic."""
    return argmin_random_tie([v for v in csp.variables if v not in assignment],
                             key=lambda var: num_legal_values(csp, var, assignment))

# Value ordering
def unordered_domain_values(var, assignment, csp): #random selection
    """The default value order."""
    return (csp.curr_domains or csp.domains)[var]

def least_constraining_value(var, assignment, csp):
    """Least-constraining-values heuristic."""
    return sorted((csp.curr_domains or csp.domains)[var], key=lambda val: csp.nconflicts(var, val, assignment))   

# Inference
def forward_checking(csp, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""

    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.curr_domains[B].remove(b)
                    if removals is not None:
                        removals.append((B, b)) # variable B and value b are removed from its domain
            if not csp.curr_domains[B]:
                return False
    return True
 

# Backtracking search
def backtracking_search(csp, select_unassigned_variable=minimum_remaining_values,
                        order_domain_values=least_constraining_value, 
                        inference=forward_checking):
    def backtrack(assignment):      #assignment la mot dictionary va gia tri dang rong      
    # """See [Figure 6.5] for the algorithm""" 
        # print(assignment)
        if len(assignment) == 81:
            return assignment
        variable_sodoku = select_unassigned_variable( assignment, csp) #ham select_unassigned_variable co tac dung chon 1 bien ngau nhien va chua ton tai o trong assignment
        for value in order_domain_values(variable_sodoku, assignment, csp): #moi bien se co mot domain, vong lap nay se duyet toan bo value trong domain cua bien bo
            if csp.nconflicts(variable_sodoku, value, assignment) == 0:  #kiem tra xem bien dang xet voi value co xung dot voi cac varible da co trong assignment khong, neu co thi ham se tra ve gia tri khac 0 va nguoc lai
                csp.assign(variable_sodoku, value, assignment)  #tien hanh gan value cho variable_sodoku va gan vao assignment
                removals = [(variable_sodoku, constraint) for constraint in csp.curr_domains[variable_sodoku] if constraint != value] #tao ra mot removal rong
                inferences = inference(csp, variable_sodoku, value, assignment, removals)  #voi moi bien la neighbor cua bien dang xet ma khong nam trong assigment, sau do duyet cac gia tri thuoc cac domain cua cac bien hang xom, neu value nao hop le thi loai cai value khoi domain cua bien hang xom, roi add vao removal, tuong tu cac bien hang xom khac roi add vao removal, sau do se con bien ke tiep de add vao assaignment
                # print(inferences)
                if inferences ==  True:        #neu inference bang true se tien hanh gan inference vao assigment
                    assignment[inferences] = inferences
                    print(inferences)
                    result = backtrack(assignment)  #tien hanh de quy lai backtrack voi assignment hien tai
                    if result!= None: #neu result khac failure  thi return la solution, result
                        return result
                    restore(csp, removals)
            csp.unassign( variable_sodoku, assignment)  #tien hanh loai bo variable khoi assigment
            csp.unassign( inferences, assignment)
            # assignment.remove([var] = value)
            # assignment.remove[assignment]
        return None 
    csp.curr_domains =csp.domains.copy()   #tien hanh sao chep domain cua tat ca cac bien thuoc csp cho current domain cua csp
    assignment = {} #tien hanh tao mot dictionary rong
    result = backtrack(assignment) #tham so la dictionary assignment vua tao
    return result
        
    #em chi lam duoc toi day thoi


    


def restore(csp, removals):
    """Undo a supposition and all inferences from it."""
    for B, b in removals:
        csp.curr_domains[B].append(b)


#%% main
if __name__ == '__main__':       
    # init_assign_easy = ''' ..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.. ''' #day la input cua bai toan, dua vao mot chuoi chua dau "." va cac chu so,
    #                                                                                                             #trong do dau "." tuong ung voi o trong trong sodocu, cac chu so tuong ung voi cac chu so trong tung o chu sodocu
    # sodoku = Sudoku(init_assign_easy)
    # print('VARIABLES:')
    # sodoku.display_variables()   #cac variables co gia tri bat dau tu 0 cho den (so phan tu -1). Trong vi du nay co 81 o tuong ung voi 0- 80
    # print('EASY SUDOKU:')
    # sodoku.display() #in ra bang sodoku ban dau tu du lieu dau vao la init_assign_easy
    # AC3(sodoku)  #tien hanh goi thuat toan AC3 voi argument la sodoku voi du lieu la init_aggsign_easy
    # print('SOLUTION TO THE EASY SUDOKU:')
    # sodoku.display() #hien ra state cuoi cung

    init_assign_hard = ''' ..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.. '''
    sodoku = Sudoku(init_assign_hard)
    print('\nHARD SUDOKU:')
    sodoku.display() 
    
    backtracking_search(sodoku)
    print('SOLUTION TO THE HARD SUDOKU:')
    sodoku.display()
# %%



# %%
