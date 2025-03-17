import matplotlib.pyplot as plt
import numpy as np
from collections import deque

def is_valid_move(x, y, maze):
    return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] == 0

def bfs(queue, visited, parent):
    (x, y) = queue.popleft()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right moves
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_valid_move(nx, ny, maze) and (nx, ny) not in visited:
            queue.append((nx, ny))
            visited.add((nx, ny))
            parent[(nx, ny)] = (x, y)

def bidirectional_search(maze, start, goal):
    if maze[start[0]][start[1]] == 1 or maze[goal[0]][goal[1]] == 1:
        return None, None, None
    
    queue_start = deque([start])
    queue_goal = deque([goal])
    visited_start = set([start])
    visited_goal = set([goal])
    parent_start = {start: None}
    parent_goal = {goal: None}
    
    while queue_start and queue_goal:
        bfs(queue_start, visited_start, parent_start)
        bfs(queue_goal, visited_goal, parent_goal)
        
        # Check for intersection
        intersect_node = None
        for node in visited_start:
            if node in visited_goal:
                intersect_node = node
                break
        
        if intersect_node is not None:
            return (intersect_node, parent_start, parent_goal)
    
    return (None, None, None)

def reconstruct_path(intersect_node, parent_start, parent_goal):
    if intersect_node is None:
        return []
    
    path = []
    # from start to intersection
    step = intersect_node
    while step is not None:
        path.append(step)
        step = parent_start[step]
    path.reverse()
    
    # from intersection to goal
    step = parent_goal[intersect_node]
    while step is not None:
        path.append(step)
        step = parent_goal[step]
    
    return path

def visualize(maze, path, start, goal):
    maze_copy = np.array(maze)
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Coloring the maze
    cmap = plt.cm.Dark2
    colors = {'empty': 0, 'wall': 1, 'path': 2}
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            color = 'white' if maze[y][x] == 0 else 'black'
            ax.fill_between([x, x+1], y, y+1, color=color)

    # Drawing the path
    if path:
        for (y, x) in path:
            ax.fill_between([x, x+1], y, y+1, color='yellow', alpha=0.5)
    
    # Mark start and goal
    sy, sx = start
    gy, gx = goal
    ax.plot(sx+0.5, sy+0.5, 'go')  # green dot at start
    ax.plot(gx+0.5, gy+0.5, 'ro')  # red dot at goal

    # Set limits and grid
    ax.set_xlim(0, len(maze[0]))
    ax.set_ylim(0, len(maze))
    ax.set_xticks(range(len(maze[0])))
    ax.set_yticks(range(len(maze)))
    ax.grid(which='both')
    ax.invert_yaxis()  # Invert the y-axis so the first row is at the top
    ax.xaxis.tick_top()  # and the x-axis is on the top

    plt.show()

# Define the maze
maze = [
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    [1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0]
]

start = (0, 0)
goal = (9, 9)

intersect_node, parent_start, parent_goal = bidirectional_search(maze, start, goal)
path = reconstruct_path(intersect_node, parent_start, parent_goal)
visualize(maze, path, start, goal)
