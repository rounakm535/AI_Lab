import heapq

def a_star(grid, start, goal):
    def h(cell):
        return ((cell[0] - goal[0]) ** 2 + (cell[1] - goal[1]) ** 2) ** 0.5

    def get_neighbors(cell):
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            x, y = cell[0] + dx, cell[1] + dy
            if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y]:
                yield (x, y)

    def reconstruct_path(came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]

    g_score = {start: 0}
    f_score = {start: h(start)}
    open_set = [(f_score[start], start)]
    came_from = {}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = reconstruct_path(came_from, current)
            print("The Path is")
            print(" -> ".join(str(cell) for cell in path))
            return

        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + h(neighbor)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    print("Failed to find the destination cell")

def main():
    grid = [
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
        [1, 0, 1, 1, 1, 1, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 0, 0, 1]
    ]
    start = (8, 0)
    goal = (0, 0)
    a_star(grid, start, goal)

if __name__ == "__main__":
    main()