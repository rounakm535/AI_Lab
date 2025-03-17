import heapq

class PuzzleState:
    def __init__(self, board, parent=None, move=0, cost=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.cost = cost
        self.zero_index = self.board.index(0)
    def __lt__(self, other):
        return self.cost < other.cost

    def generate_successors(self):
        successors = []
        x, y = divmod(self.zero_index, 3)
        moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        
        for nx, ny in moves:
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_board = self.board[:]
                new_zero_index = nx * 3 + ny
                new_board[self.zero_index], new_board[new_zero_index] = new_board[new_zero_index], new_board[self.zero_index]
                successors.append(PuzzleState(new_board, self, self.move + 1))
        
        return successors

    def manhattan_distance(self, goal):
        distance = 0
        for i in range(1, 9):  # Skip the blank tile (0)
            x1, y1 = divmod(self.board.index(i), 3)
            x2, y2 = divmod(goal.index(i), 3)
            distance += abs(x1 - x2) + abs(y1 - y2)
        return distance

def a_star(start_state, goal_state):
    open_list = []
    closed_set = set()
    
    start_state.cost = start_state.manhattan_distance(goal_state.board)
    heapq.heappush(open_list, start_state)

    while open_list:
        current_state = heapq.heappop(open_list)

        if current_state.board == goal_state.board:
            path = []
            while current_state:
                path.append(current_state.board)
                current_state = current_state.parent
            return path[::-1]

        closed_set.add(tuple(current_state.board))

        for successor in current_state.generate_successors():
            if tuple(successor.board) in closed_set:
                continue
            
            successor.cost = successor.move + successor.manhattan_distance(goal_state.board)
            heapq.heappush(open_list, successor)

    return None

# Define the initial and goal states
initial_board = [1, 2, 3,
                 4, 0, 5,
                 6, 7, 8]

goal_board = [1, 2, 3,
              4, 5, 6,
              7, 8, 0]

start_state = PuzzleState(initial_board)
goal_state = PuzzleState(goal_board)

# Solve the puzzle
solution_path = a_star(start_state, goal_state)

if solution_path:
    print("Solution found:")
    for step in solution_path:
        print(step[:3])
        print(step[3:6])
        print(step[6:])
        print()
else:
    print("No solution exists.")
