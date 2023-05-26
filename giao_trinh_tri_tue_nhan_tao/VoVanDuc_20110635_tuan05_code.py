# [SHARED WITH AI CLASSES] week05 exercise
'''
The code below is INCOMPLETE. You need to implement the following functions:
1. depth_limited_search()  
2. iterative_deepening_search() 

HINT: Function breadth_first_graph_search() is for your reference (Its usage is demonstrated in the __main__ part (line 154)). Read it to understand the given code.
'''


from ast import NodeTransformer
import sys
from collections import deque


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

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
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))


def breadth_first_graph_search(problem):
    """Bread first search (GRAPH SEARCH version)
    See [Figure 3.11] for the algorithm"""

    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier = deque([node])
    explored = set()
    while frontier:
        node = frontier.popleft()
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                if problem.goal_test(child.state):
                    return child
                frontier.append(child)
    return None
      

''' IMPLEMENT THE FOLLOWING FUNCTION '''
def depth_limited_search(problem, limit=50):
    """See [Figure 3.17] for the algorithm"""
    node = Node(problem.initial)  # tạo ra node có state ban đầu là [3,1,2,6,0,8,7,5,4]
    if problem.goal_test(node.state):  #kiểm tra xem state của biến node có bằng với node đích hay không [0, 1, 2, 3, 4, 5, 6, 7, 8]
        return node                      #nếu bằng thì trả về node có state đích
    frontier = []                        #nếu node hiện tại có state không bằng với goal_state thì tiến hành tạo một frontier rỗng
    frontier.append(node)        # thêm node ban đầu vào frontier
    explored = []        # tạo một mảng explored để lưu những node có trạng thái đã đi qua

    #loop do
    while frontier:          #sử dụng while vì không rõ có bao nhiêu vòng lặp để tìm được state goal
        node = frontier.pop(0)            # lấy ra và xoá đi node đầu tiên trong frontier
        if problem.goal_test(node.state):   #kiểm tra nếu node hiện tại bằng node_goal thì trả về node đó 
            return node                         #nếu không bằng node_goal thì tiến hành so sánh độ sâu của node với limit, mếu bằng thì thoát
        elif node.depth == limit:
            break
        explored.append(node.state)          #nếu node hiện tại không bằng node goal thì tiến hành thêm trạng thái của node hiện tại vào explored
        for action in problem.actions(node.state):     #sử dụng vòng lặp for để duyệt tất cả các action có thể thực hiện bởi 1 node có state
            nodeChild = node.child_node(problem, action)   #tạo node con từ node hiện tại
            if nodeChild.state not in frontier or explored:  # nếu node con chứa state không tồn tại trong frontier hoặc explored thì tiếp tục tiến hành 
                if problem.goal_test(nodeChild.state):  #so sáng node con và node đích, nếu 2 node bằng nhau thì trả về node con có state đích,
                    return nodeChild
                else:                     #nếu không thì tiến hành thêm node con vào frontier
                    frontier.append(nodeChild)




''' IMPLEMENT THE FOLLOWING FUNCTION '''
def iterative_deepening_search(problem):
    """See [Figure 3.18] for the algorithm""" 
    maxIndex = sys.maxsize       #sử dụng thư viện sys để gọi hàm maxsize tạo ra giá trị nguyên cực lớn
    for depth in range(0, maxIndex, 1):  # sử dụng vòng lặp for với biến index chạy từ 0 tới giá trị gần vô cùng
        result = depth_limited_search(problem, depth) #gán node có state đích cho result
        if result != None:  #nếu result không chạm cutoff (đáy của problem) thì trả về result
            return result
  

class EightPuzzleProblem:
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=(0, 1, 2, 3, 4, 5, 6, 7, 8)):
        """ Define goal state and initialize a problem """
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square % 3 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < 3:
            possible_actions.remove('UP')
        if index_blank_square % 3 == 2:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1     

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""    
        return state.index(0)


if __name__ == '__main__':
    import time

    problem = EightPuzzleProblem(initial=(3, 1, 2, 6, 0, 8, 7, 5, 4), goal=(0, 1, 2, 3, 4, 5, 6, 7, 8))

    result1 = iterative_deepening_search(problem)
    print(result1.solution())
    
    
    # USE BELOW CODE TO TEST YOUR IMPLEMENTED FUNCTIONS
    #result2 = iterative_deepening_search(problem)
    #print(result2.solution())