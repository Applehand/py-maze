import pygame
import random

WINDOW_WIDTH = 550
WINDOW_HEIGHT = 550
GRID_WIDTH = 5
GRID_HEIGHT = 5
CELL_MARGIN = 0

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
DARK_GREY = (50, 50, 50)
LIGHT_GREY = (228, 228, 228)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BEIGE = (245, 245, 220)
BROWN = (139, 69, 19)
NEON_GREEN = (57, 255, 20)
ELECTRIC_BLUE = (44, 117, 255)
HOT_PINK = (255, 105, 180)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
MIDNIGHT_BLUE = (25, 25, 112)
CHARCOAL = (54, 69, 79)
OLIVE = (128, 128, 0)
TEAL = (0, 128, 128)
LIME = (50, 205, 50)
CRIMSON = (220, 20, 60)
INDIGO = (75, 0, 130)
AMBER = (255, 191, 0)


class Cell:
    """Represents a single cell in the grid."""

    def __init__(self, pos_x, pos_y, width, height, color=WHITE):
        """
        Initialize a cell with its position, dimensions, and default color.

        :param pos_x: X-coordinate of the top-left corner.
        :param pos_y: Y-coordinate of the top-left corner.
        :param width: Width of the cell in pixels.
        :param height: Height of the cell in pixels.
        :param color: Initial color of the cell.
        """
        self.x = pos_x  # Top-left corner X position
        self.y = pos_y  # Top-left corner Y position
        self.width = width
        self.height = height
        self.color = color
        self.current = False
        self.chosen = False
        self.visited = False
        self.start = False
        self.goal = False
        self.walls = [True, True, True, True] # Left[0], Top[1], Right[2], Bottom[3]

    def draw(self, screen):
        """
        Draw the cell on the given screen surface.

        :param screen: Pygame surface to draw on.
        """
        draw_color = self.color
        if self.start:
            draw_color = NEON_GREEN
        elif self.goal:
            draw_color = GOLD
        if self.current:
            draw_color = BLUE
        elif self.chosen:
            draw_color = YELLOW
        elif self.visited:
            draw_color = LIGHT_GREY

        # Draw walls
        wall_color = BLACK
        wall_thickness = 6
        wall_coords = [
            ((self.x, self.y), (self.x, self.y + self.height)),  # Left wall
            ((self.x, self.y), (self.x + self.width, self.y)),  # Top wall
            ((self.x + self.width, self.y), (self.x + self.width, self.y + self.height)),  # Right wall
            ((self.x, self.y + self.height), (self.x + self.width, self.y + self.height))  # Bottom wall
        ]

        for i, wall in enumerate(self.walls):
            if wall:  # Check if the wall exists
                start, end = wall_coords[i]
                pygame.draw.line(screen, wall_color, start, end, wall_thickness)

        # Draw the cell background
        pygame.draw.rect(screen, draw_color, (self.x, self.y, self.width, self.height))


class Grid:
    """Manages a grid of cells, including their interactions and dynamic scaling."""

    def __init__(self, grid_width, grid_height, screen_width, screen_height, cell_margin):
        """
        Initialize the grid with given dimensions and cell spacing.

        :param grid_width: Number of cells horizontally.
        :param grid_height: Number of cells vertically.
        :param screen_width: Width of the entire screen in pixels.
        :param screen_height: Height of the entire screen in pixels.
        :param cell_margin: Space between cells in pixels.
        """
        self.width = grid_width
        self.height = grid_height
        self.cell_margin = cell_margin
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Dynamically calculate cell dimensions, grid margins, and offset
        self.cell_width, self.cell_height = self._evaluate_dimensions()
        self.cells = self._initialize_grid()

    def _evaluate_dimensions(self):
        """
        Calculate the width, height, and margin for cells to fit the screen.

        :return: (cell_width, cell_height) as integers.
        """
        # Total space occupied by margins
        total_margin_width_x = self.cell_margin * (self.width + 1)
        total_margin_width_y = self.cell_margin * (self.height + 1)

        # Calculate cell dimensions
        square_width = int((self.screen_width - total_margin_width_x) / self.width)
        square_height = int((self.screen_height - total_margin_width_y) / self.height)

        # Calculate grid size in pixels
        self.grid_width_px = square_width * self.width + self.cell_margin * (self.width + 1)
        self.grid_height_px = square_height * self.height + self.cell_margin * (self.height + 1)

        # Center the grid on the screen
        self.offset_x = (self.screen_width - self.grid_width_px) // 2
        self.offset_y = (self.screen_height - self.grid_height_px) // 2

        return square_width, square_height

    def _initialize_grid(self):
        """
        Create and position all cells in the grid.

        :return: A 2D list of Cell objects.
        """
        grid = []
        for row in range(self.height):
            grid.append([])
            for col in range(self.width):
                # Calculate position of each cell with margin and offset
                pos_x = self.offset_x + self.cell_margin * (col + 1) + self.cell_width * col
                pos_y = self.offset_y + self.cell_margin * (row + 1) + self.cell_height * row
                grid[row].append(Cell(int(pos_x), int(pos_y), self.cell_width, self.cell_height))
        return grid

    def is_within_grid(self, row, col):
        """
        Check if the given row and column are within the grid bounds.

        :return: True if within bounds, False otherwise.
        """
        return 0 <= row < self.height and 0 <= col < self.width

    def get_neighbors(self, row, col):
        """
        Retrieve neighboring cells for the given cell.

        :param row: Row index of the cell.
        :param col: Column index of the cell.
        :return: A dictionary of neighboring cells with direction keys (N, S, E, W).
        """
        directions = {
            "N": (row - 1, col),  # North
            "S": (row + 1, col),  # South
            "W": (row, col - 1),  # West
            "E": (row, col + 1),  # East
        }
        neighbors = {}
        for direction, (neighbor_row, neighbor_col) in directions.items():
            if self.is_within_grid(neighbor_row, neighbor_col):
                neighbors[direction] = self.cells[neighbor_row][neighbor_col]
        return neighbors

    def get_cell_position(self, x, y):
        """
        Calculate the row and column of the cell at a given screen position.

        :param x: X-coordinate of the mouse click.
        :param y: Y-coordinate of the mouse click.
        :return: (row, col) indices of the cell, or (None, None) if out of bounds.
        """
        # Adjust for grid offset
        adjusted_x = x - self.offset_x
        adjusted_y = y - self.offset_y

        # Ensure click is within grid bounds
        if adjusted_x < 0 or adjusted_y < 0:
            return None, None

        # Calculate row and column
        col = int(adjusted_x // (self.cell_width + self.cell_margin))
        row = int(adjusted_y // (self.cell_height + self.cell_margin))

        if self.is_within_grid(row, col):
            # Determine the cell's actual rectangle
            cell_x = self.offset_x + self.cell_margin * (col + 1) + self.cell_width * col
            cell_y = self.offset_y + self.cell_margin * (row + 1) + self.cell_height * row

            # Verify within the actual cell
            if cell_x <= x < cell_x + self.cell_width and cell_y <= y < cell_y + self.cell_height:
                return row, col

        return None, None

    def remove_wall_between(self, cell_a, cell_b):
        """
        Remove the wall between two adjacent cells.

        :param cell_a: The first cell.
        :param cell_b: The second cell (must be adjacent to cell_a).
        """
        # Determine the relationship between the cells
        row_a, col_a = self.get_cell_position(cell_a.x, cell_a.y)
        row_b, col_b = self.get_cell_position(cell_b.x, cell_b.y)

        if row_a == row_b:  # Same row
            if col_a < col_b:  # cell_b is to the east
                cell_a.walls[2] = False  # Remove right wall of cell_a
                cell_b.walls[0] = False  # Remove left wall of cell_b
            elif col_a > col_b:  # cell_b is to the west
                cell_a.walls[0] = False  # Remove left wall of cell_a
                cell_b.walls[2] = False  # Remove right wall of cell_b
        elif col_a == col_b:  # Same column
            if row_a < row_b:  # cell_b is to the south
                cell_a.walls[3] = False  # Remove bottom wall of cell_a
                cell_b.walls[1] = False  # Remove top wall of cell_b
            elif row_a > row_b:  # cell_b is to the north
                cell_a.walls[1] = False  # Remove top wall of cell_a
                cell_b.walls[3] = False  # Remove bottom wall of cell_b

    def has_wall_between(self, cell_a, cell_b):
        """
        Check if there is a wall between two adjacent cells.

        :param cell_a: The first cell.
        :param cell_b: The second cell.
        :return: True if there is a wall between the cells, False otherwise.
        """
        # Calculate grid coordinates of the cells
        row_a, col_a = self.get_cell_position(cell_a.x, cell_a.y)
        row_b, col_b = self.get_cell_position(cell_b.x, cell_b.y)

        # Determine the relative position of cell_b to cell_a
        if row_a == row_b:  # Same row
            if col_a < col_b:  # cell_b is to the east
                return cell_a.walls[2] or cell_b.walls[0]
            elif col_a > col_b:  # cell_b is to the west
                return cell_a.walls[0] or cell_b.walls[2]
        elif col_a == col_b:  # Same column
            if row_a < row_b:  # cell_b is to the south
                return cell_a.walls[3] or cell_b.walls[1]
            elif row_a > row_b:  # cell_b is to the north
                return cell_a.walls[1] or cell_b.walls[3]

        return True  # Default to True if cells are not adjacent



    def draw(self, screen):
        """
        Draw all cells in the grid on the given screen surface.

        :param screen: Pygame surface to draw on.
        """
        for row in self.cells:
            for cell in row:
                cell.draw(screen)


class Maze:
    """
    Manages maze generation and solving.
    """

    def __init__(self, grid):
        self.grid = grid
        self.origin_cell = random.choice([cell for row in self.grid.cells for cell in row])
        self.distances = {}
        self.stack = []
        self._generate_maze()

    def _generate_maze(self):  # depth first search algorithm for generating maze
        self.origin_cell.visited = True
        self.distances[self.origin_cell] = 0
        self.stack.append(self.origin_cell)
        while self.stack:
            current_cell = self.stack.pop()
            current_cell_row, current_cell_col = self.grid.get_cell_position(current_cell.x, current_cell.y)
            neighbors = self.grid.get_neighbors(current_cell_row, current_cell_col)
            unvisited_neighbors = [n for n in neighbors.values() if not n.visited]
            if unvisited_neighbors:
                self.stack.append(current_cell)
                chosen_cell = random.choice(unvisited_neighbors)
                self.grid.remove_wall_between(current_cell, chosen_cell)
                self.distances[chosen_cell] = self.distances[current_cell] + 1
                chosen_cell.visited = True
                self.stack.append(chosen_cell)

        for row in self.grid.cells:  # reset cells to be unvisited
            for cell in row:
                cell.visited = False

class GameSession:
    """
    Manages game sessions, including maze interactions, gameplay rules, and scores.
    """

    def __init__(self, maze, game_mode):
        self.maze = maze
        self.start_cell = self.maze.origin_cell
        self.goal_cell = max(self.maze.distances, key=self.maze.distances.get)
        self.start_cell.start, self.goal_cell.goal = True, True
        self.current_cell = self.start_cell
        self.game_mode = game_mode

    def target_neighboring_cell(self, target_direction):  # "N", "S", "W", "E"
        cur_row, cur_col = self.maze.grid.get_cell_position(self.current_cell.x, self.current_cell.y)
        current_neighbors = self.maze.grid.get_neighbors(cur_row, cur_col)
        target_cell = current_neighbors[target_direction]
        target_cell.chosen = True

    def move_player_to_cell(self, cell, target_cell):
        if not self.maze.grid.has_wall_between(cell, target_cell):
            self.current_cell.current = False
            target_cell.current = True
            self.current_cell = target_cell


grid = Grid(GRID_WIDTH, GRID_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, CELL_MARGIN)
maze = Maze(grid)
game = GameSession(maze, "default")


def game_loop():
    """Main game loop to handle events and rendering."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Handle arrow keys for movement
                direction_map = {
                    pygame.K_UP: "N",
                    pygame.K_DOWN: "S",
                    pygame.K_LEFT: "W",
                    pygame.K_RIGHT: "E"
                }
                if event.key in direction_map:
                    direction = direction_map[event.key]

                    cur_row, cur_col = grid.get_cell_position(game.current_cell.x, game.current_cell.y)
                    neighbors = grid.get_neighbors(cur_row, cur_col)

                    if direction in neighbors:
                        target_cell = neighbors[direction]

                        if not grid.has_wall_between(game.current_cell, target_cell):
                            game.move_player_to_cell(game.current_cell, target_cell)

        # Draw the grid and update the display
        screen.fill(WHITE)  # Clear screen
        grid.draw(screen)
        pygame.display.flip()
        clock.tick(60)  # Cap the frame rate at 60 FPS

    pygame.quit()




if __name__ == "__main__":
    game_loop()
