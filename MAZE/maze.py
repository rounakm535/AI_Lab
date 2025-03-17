import tkinter as tk
from enum import Enum
from random import choice


class Color(Enum):
    """Color schemes for the maze"""
    DARK = ('#1a1a1a', 'white')  # Background, Wall color
    LIGHT = ('white', 'black')
    BLUE = ('DeepSkyBlue4', 'white')
    GREEN = ('green4', 'white')


class MazeCell:
    """Represents a single cell in the maze"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.visited = False


class Player:
    """Player character in the maze"""

    def __init__(self, maze, x, y, size=20):
        self.maze = maze
        self.x = x
        self.y = y
        self.size = size
        self.create_player()

    def create_player(self):
        """Create player visual representation"""
        x, y = self.get_canvas_coords()
        self.shape = self.maze.canvas.create_oval(
            x + self.size // 4, y + self.size // 4,
            x + 3 * self.size // 4, y + 3 * self.size // 4,
            fill='red'
        )

    def get_canvas_coords(self):
        """Convert grid coordinates to canvas coordinates"""
        return (self.y * self.size, self.x * self.size)

    def move(self, dx, dy):
        """Move player if valid move"""
        new_x, new_y = self.x + dx, self.y + dy

        # Check if move is valid
        if 0 <= new_x < self.maze.rows and 0 <= new_y < self.maze.cols:
            current = self.maze.grid[self.x][self.y]

            # Check walls
            if dx == 1 and not current.walls['S']:
                self.x = new_x
            elif dx == -1 and not current.walls['N']:
                self.x = new_x
            elif dy == 1 and not current.walls['E']:
                self.y = new_y
            elif dy == -1 and not current.walls['W']:
                self.y = new_y

            # Update player position
            x, y = self.get_canvas_coords()
            self.maze.canvas.coords(
                self.shape,
                x + self.size // 4, y + self.size // 4,
                x + 3 * self.size // 4, y + 3 * self.size // 4
            )

            # Check if reached goal
            if (self.x, self.y) == (self.maze.rows - 1, self.maze.cols - 1):
                self.maze.show_win_message()


class Maze:
    """Main maze game class"""

    def __init__(self, rows=10, cols=10, cell_size=40):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.width = cols * cell_size
        self.height = rows * cell_size

        # Initialize window and canvas
        self.window = tk.Tk()
        self.window.title("Maze Game")
        self.canvas = tk.Canvas(
            self.window,
            width=self.width,
            height=self.height,
            bg=Color.DARK.value[0]
        )
        self.canvas.pack()

        # Create maze grid
        self.grid = [[MazeCell(i, j) for j in range(cols)] for i in range(rows)]

        # Generate maze
        self.generate_maze()

        # Create player
        self.player = Player(self, 0, 0, cell_size)

        # Bind keys
        self.bind_keys()

        # Draw maze
        self.draw_maze()

    def generate_maze(self):
        """Generate maze using DFS algorithm"""

        def get_neighbors(x, y):
            neighbors = []
            for dx, dy, direction in [(0, 1, 'E'), (0, -1, 'W'), (1, 0, 'S'), (-1, 0, 'N')]:
                new_x, new_y = x + dx, y + dy
                if (0 <= new_x < self.rows and
                        0 <= new_y < self.cols and
                        not self.grid[new_x][new_y].visited):
                    neighbors.append((new_x, new_y, direction))
            return neighbors

        def remove_walls(x1, y1, x2, y2, direction):
            if direction == 'E':
                self.grid[x1][y1].walls['E'] = False
                self.grid[x2][y2].walls['W'] = False
            elif direction == 'W':
                self.grid[x1][y1].walls['W'] = False
                self.grid[x2][y2].walls['E'] = False
            elif direction == 'N':
                self.grid[x1][y1].walls['N'] = False
                self.grid[x2][y2].walls['S'] = False
            elif direction == 'S':
                self.grid[x1][y1].walls['S'] = False
                self.grid[x2][y2].walls['N'] = False

        stack = [(0, 0)]
        self.grid[0][0].visited = True

        while stack:
            current = stack[-1]
            neighbors = get_neighbors(*current)

            if not neighbors:
                stack.pop()
                continue

            next_cell = choice(neighbors)
            x, y = current
            new_x, new_y = next_cell[0], next_cell[1]
            remove_walls(x, y, new_x, new_y, next_cell[2])

            self.grid[new_x][new_y].visited = True
            stack.append((new_x, new_y))

    def draw_maze(self):
        """Draw maze walls"""
        for i in range(self.rows):
            for j in range(self.cols):
                x, y = j * self.cell_size, i * self.cell_size
                cell = self.grid[i][j]

                # Draw walls
                if cell.walls['N']:
                    self.canvas.create_line(
                        x, y, x + self.cell_size, y,
                        fill=Color.DARK.value[1], width=2
                    )
                if cell.walls['S']:
                    self.canvas.create_line(
                        x, y + self.cell_size, x + self.cell_size, y + self.cell_size,
                        fill=Color.DARK.value[1], width=2
                    )
                if cell.walls['E']:
                    self.canvas.create_line(
                        x + self.cell_size, y, x + self.cell_size, y + self.cell_size,
                        fill=Color.DARK.value[1], width=2
                    )
                if cell.walls['W']:
                    self.canvas.create_line(
                        x, y, x, y + self.cell_size,
                        fill=Color.DARK.value[1], width=2
                    )

        # Draw goal
        x = (self.cols - 1) * self.cell_size
        y = (self.rows - 1) * self.cell_size
        self.canvas.create_oval(
            x + self.cell_size // 4, y + self.cell_size // 4,
            x + 3 * self.cell_size // 4, y + 3 * self.cell_size // 4,
            fill='green'
        )

    def bind_keys(self):
        """Bind keyboard controls"""
        self.window.bind('<Left>', lambda e: self.player.move(0, -1))
        self.window.bind('<Right>', lambda e: self.player.move(0, 1))
        self.window.bind('<Up>', lambda e: self.player.move(-1, 0))
        self.window.bind('<Down>', lambda e: self.player.move(1, 0))
        self.window.bind('<Escape>', lambda e: self.window.destroy())

    def show_win_message(self):
        """Display win message"""
        self.canvas.create_text(
            self.width // 2, self.height // 2,
            text="You Win!",
            fill="green",
            font=("Arial", 24, "bold")
        )

    def run(self):
        """Start the game"""
        self.window.mainloop()


if __name__ == "__main__":
    # Create and run maze game
    game = Maze(10, 10)  # Creates a 10x10 maze
    game.run()