import numpy as np
import random
import math

class Node:
    def __init__(self, state, parent=None, action = None, path_cost=0):
        self.state=state
        self.parent=parent
        self.action=action
        self.path_cost=path_cost
        self.depth=0
        if parent:
            self.depth=parent.depth+1


    def expand(self, problem):
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next_state=problem.result(self.state, action)
        next_node=Node(next_state, self, action)
        return next_node
class n_Queens_Problem:
    def __init__(self, n):
        self.initial=tuple([-1]*number_of_queens)  
        self.n=n

    def Goal_check(self, node):
        return (self.value(node)==0 and node.state.count(-1)==0)

    def DeadEnd_check(self, node, possibleNodes):
        return (len(possibleNodes) ==0 and node.state.count(-1)>0)

    def actions(self, state):
        if state[-1] != -1:
            return []
        else:
            column=state.index(-1)
            return [row for row in range(self.n)
                if not self.conflicted(state, row, column)]

    def result(self, state, row):
        column=state.index(-1)
        new=list(state[:])
        new[column]=row
        return tuple(new)

    def conflicted(self, state, row, column):
        return any(self. conflict(row, column, state[c],c) for c in range(column))

    def conflict(self, row1, column1, row2, column2):
        return (row1==row2 or
                column1==column2 or
                row1-column1==row2-column2 or
                row1+column1==row2+column2)

    def value(self, node):
        number_conflicted=0
        for(row1, column1) in enumerate(node.state):
            for (row2, column2) in enumerate(node.state):
                if (row1,column1) != (row2, column2):
                    number_conflicted+=self.conflict(row1, column1, row2, column2)
        return -number_conflicted

def schedule(a, b=20, c=0.005, l=1000):
    return (b* np.exp(-c*a) if a< l else 0)

def simulated_annealing(problem):
    current=Node(problem.initial)  #tao ra problem co vi tri cac con hau la -1
    print("initial state with node: ", current.state)
    t=1
    while True:
        T=schedule(t)
        print("T = ", T)
        if T==0:
            print("current state: ", current.state)
            return current.state          #state hien tai co vi tri cac con hau la -1
        success=current.expand(problem)
        print("len success = ", len(success))

        print("problem value cerrent = ", problem.value(current), " current state count = ", current.state.count(-1) )
        if problem.value(current)==0 and current.state.count(-1)==0: 
            print("current state: ", current.state)
            return current.state
        elif len(success) == 0:
            if current.state.count(-1)>0:
                print("current state count: ", current.state.count(-1))
                current=Node(problem.initial)
                print("current problem initial: ", current.state)
        else:
            next_node=random.choice(success)
            print("next_node: ", next_node.state)
            delta_e=problem.value(next_node) - problem.value(current)
            print("delta_e = ", delta_e)
            # a = random.rand()
            # b = math.exp(delta_e/T)
            if delta_e >0:
                current=next_node
                print("current node: ", current.state)
            elif random.rand() < math.exp(delta_e/T):
                print("random.rand(): ", random.rand() + " math.exp(delta_e/T): ",math.exp(delta_e/T))
                current=next_node
                print("current node: ", current.state)
            else:
                current=current
                print("current: ", current.state)
        t+=1
        print("t = ", t)
        print("\n")
        print("\n")
        # choose = int(input("Muon tiep tuc: "))
        # if choose == 1:
        #     continue
        # else:
        #     break
        

number_of_queens = 8
random.seed(1)
Problem_ = n_Queens_Problem(number_of_queens)
Result_= simulated_annealing(Problem_)
print(Result_)
