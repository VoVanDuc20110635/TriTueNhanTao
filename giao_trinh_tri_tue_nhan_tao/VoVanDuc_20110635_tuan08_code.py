# Solve N-queens problems using AND-OR search algorithm
'''
YOUR TASKS:
1. Read the given code to understand
2. Implement the and_or_graph_search() function
3. (Optinal) Add GUI, animation...
'''

from importlib.resources import path
import sys
from collections import deque
import numpy as np
import random

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        #next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        next_node = Node(next_state, self, action)
        return next_node


class NQueensProblem:
    """The problem of placing N queens on an NxN board with none attacking each other. 
    A state is represented as an N-element array, where a value of r in the c-th entry means there is a queen at column c,
    row r, and a value of -1 means that the c-th column has not been filled in yet. We fill in columns left to right.
    
    Sample code: iterative_deepening_search(NQueensProblem(8))
    Result: <Node (0, 4, 7, 5, 2, 6, 1, 3)>
    """

    def __init__(self, N):
        #self.initial = initial 
        self.initial = tuple([-1]*no_of_queens)  # -1: no queen in that column
        self.N = N

    def actions(self, state):
        """In the leftmost empty column, try all non-conflicting rows."""
        if state[-1] != -1:
            return []  # All columns filled; no successors
        else:
            col = state.index(-1)
            #return [(col, row) for row in range(self.N)
            return [row for row in range(self.N)
                    if not self.conflicted(state, row, col)]

    def goal_test(self, state):
        """Check if all columns filled, no conflicts."""
        if state[-1] == -1:
            return False
        return not any(self.conflicted(state, state[col], col)
                       for col in range(len(state)))

    def result(self, state, row):
        """Place the next queen at the given row."""
        col = state.index(-1)
        print("col: ", col)
        new = list(state[:])
        new[col] = row
        print("new[col]: ", new[col])
        print("tuple(new)[col]: ",tuple(new)[col])
        return tuple(new)

    def conflicted(self, state, row, col):
        """Would placing a queen at (row, col) conflict with anything?"""
        return any(self.conflict(row, col, state[c], c)
                   for c in range(col))

    def conflict(self, row1, col1, row2, col2):
        """Would putting two queens in (row1, col1) and (row2, col2) conflict?"""
        return (row1 == row2 or  # same row
                col1 == col2 or  # same column
                row1 - col1 == row2 - col2 or  # same \ diagonal
                row1 + col1 == row2 + col2)  # same / diagonal

    def value(self, node): 
        """Return (-) number of conflicting queens for a given node"""
        num_conflicts = 0
        for (r1, c1) in enumerate(node.state):
            for (r2, c2) in enumerate(node.state):
                if (r1, c1) != (r2, c2):
                    num_conflicts += self.conflict(r1, c1, r2, c2)

        return -num_conflicts 

def and_or_graph_search(problem):
    '''
    Thuật toán AND-OR SEARCH (AO*) dùng để tìm lời giải cho bài toán N quân hậu.
    Hàm and_or_graph_search() sử dụng đệ quy tương hỗ, dựa trên Depth-First Search để tìm goal state.
    Sử dụng 2 hàm con, gọi đệ quy lẫn nhau là or_search() và and_search().
    '''

    
    def or_search(state, problem, path):
        print("OR_SEARCH")
        print("state: ", state)
        print("path: ", path)
        print("\n")
        if problem.goal_test(state):
            print("======================Da ket thuc=======================!")
            return []

        if state in path:
            print("===============================thoat khoi ham=============")
            return None

        plans = []
        for action in problem.actions(state):
            print("action: ", action)
            print("[problem.result(state, action)]: ", [problem.result(state, action)])
            print("state: ", state)
            print("path: ", path)
            print("[state]+ path: ", [state] + path)
            print("\n")
            plan = and_search([problem.result(state, action)], problem, [state] + path)
            print("plan: ",plan)
            
            #Nếu tìm thấy goal state, mỗi action chỉ ứng với 1 goal state (NQueens) nên có thể return luôn 
            if plan is not None:
                plans.append((action, plan))
                print("plans: ", plans)

        if len(plans) > 0:
            print("==================len(plans) > 0 va thoat ham or==================")
            return plans
        print("==================len(plans) <= 0 va thoat ham or==================")
        return None


    def and_search(states, problem, path):
        # print("state: ", states)
        # print("path: ", path)
        print("AND_SEARCH")
        print("\n")
        print("states:", states)
        print("problem: ", problem.initial)
        print("path: ", path)
        print("")
        '''
        Return dictionary là plans nếu có thể tìm thấy ít nhất một goal state ứng với state s_i. Ngược lại, return None.
        states: list các states (chính là các successors của state hiện tại ở or_search()).
        problem: là thể hiện (instance) của NQUEENSPROBLEM.
        path:
        '''

        plans = {}  #plan là mọt dictionary, có key là 1 state cụ thể, mỗi key ứng với một value là kết quả trả về của hàm or_search().
        #Thêm các phần tử vào plan 
        for state in states:
            print("states:", states)
            print("problem: ", problem.initial)
            print("path: ", path)
            print("plans: ", plans)
            plan = or_search(state, problem, path)
            print("plan: ", plan)
            if plan is None:
                continue
            else:
                plans[state] = plan
                print("plans[state]: ", plans[state])
                print("plans: ", plans)
        
        '''Có thể sau khi chuẩn hóa dictionary plans thì không còn phần tử nào.
        Nghĩa là từ state ở or_search(), sinh ra các successors, không một successor nào đi đến được goal state.'''
        if len(plans) > 0:
            print("====================plans: ",plans,"====================")
            return plans
        else:
            print("============Thoat khoi and================")
            return None


    state = problem.initial
    plans = {}
    print("hihi state: ", state)
    print("hi hi plans: ", plans)
    print("\n")
    plans[state] = or_search(state, problem, [])
    
    return plans


if __name__ == '__main__':
    no_of_queens = 4;
    problem1 = NQueensProblem(no_of_queens)

    print("Problem: ",problem1.initial)

    result2 = and_or_graph_search(problem1)
    print(result2)