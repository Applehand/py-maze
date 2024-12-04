import pygame

WINDOW_WIDTH = 550
WINDOW_HEIGHT = 550
GRID_WIDTH = 10
GRID_HEIGHT = 10
CELL_MARGIN = 3

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)


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
        self.selected = False
        self.visited = False

    def draw(self, screen):
        """
        Draw the cell on the given screen surface.

        :param screen: Pygame surface to draw on.
        """
        # Change color based on cell state
        if self.selected:
            self.color = GREEN
        elif self.visited:
            self.color = GREY
        else:
            self.color = WHITE

        # Draw the cell
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


class Grid:
    """Manages a grid of cells and handles interactions with them."""

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

            # Verify click is within the actual cell
            if cell_x <= x < cell_x + self.cell_width and cell_y <= y < cell_y + self.cell_height:
                return row, col

        return None, None

    def draw(self, screen):
        """
        Draw all cells in the grid on the given screen surface.

        :param screen: Pygame surface to draw on.
        """
        for row in self.cells:
            for cell in row:
                cell.draw(screen)


grid = Grid(GRID_WIDTH, GRID_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, CELL_MARGIN)


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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle mouse click to select a cell
                pos = pygame.mouse.get_pos()
                clicked_row, clicked_column = grid.get_cell_position(pos[0], pos[1])

                if clicked_row is not None and clicked_column is not None:
                    cell = grid.cells[clicked_row][clicked_column]
                    cell.selected = not cell.selected
                    cell.visited = True
                    print(f"Clicked cell: ({clicked_row}, {clicked_column})")

        grid.draw(screen)  # Draw the grid
        pygame.display.flip()  # Update the display

        clock.tick(60)  # Cap the frame rate at 60 FPS

    pygame.quit()


if __name__ == "__main__":
    game_loop()
