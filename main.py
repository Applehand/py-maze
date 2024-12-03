import pygame

WINDOW_HEIGHT = 255
WINDOW_WIDTH = 255

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)


class Cell:
    """Represents a single cell in the grid."""

    def __init__(self, pos_x, pos_y, width, height, color=WHITE):
        self.x = pos_x  # Pixel x-coordinate
        self.y = pos_y  # Pixel y-coordinate
        self.width = width
        self.height = height
        self.color = color
        self.selected = False
        self.visited = False

    def draw(self, screen):
        """Draw the cell on the screen."""
        if self.selected:
            self.color = GREEN
        elif self.visited:
            self.color = GREY
        else:
            self.color = WHITE

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


class Grid:
    """Manages a grid of cells."""

    def __init__(self, grid_width, grid_height, cell_width, cell_height, cell_margin):
        self.width = grid_width  # Number of cells horizontally
        self.height = grid_height  # Number of cells vertically
        self.cell_width = cell_width  # Width of each cell in pixels
        self.cell_height = cell_height  # Height of each cell in pixels
        self.cell_margin = cell_margin  # Margin between cells
        self.cells = self._initialize_grid()

    def _initialize_grid(self):
        """Initialize the grid by creating and positioning cells."""
        grid = []
        for row in range(self.height):
            grid.append([])
            for col in range(self.width):
                # Calculate position of each cell
                pos_x = (self.cell_margin + self.cell_width) * col + self.cell_margin
                pos_y = (self.cell_margin + self.cell_height) * row + self.cell_margin
                grid[row].append(Cell(pos_x, pos_y, self.cell_width, self.cell_height))
        return grid

    def is_within_grid(self, row, col):
        """Check if the given row and column are within the grid bounds."""
        return 0 <= row < self.height and 0 <= col < self.width

    def get_neighbors(self, row, col):
        """Retrieve the neighboring cells of the given cell."""
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
        """Calculate grid row and column from pixel coordinates (x, y)."""
        col = x // (self.cell_width + self.cell_margin)
        row = y // (self.cell_height + self.cell_margin)

        if self.is_within_grid(row, col):
            return row, col
        else:
            return None, None

    def draw(self, screen):
        """Draw all cells in the grid."""
        for row in self.cells:
            for cell in row:
                cell.draw(screen)


grid = Grid(10, 10, 20, 20, 5)


def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    running = True
    while running:
        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the game loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                clicked_row, clicked_column = grid.get_cell_position(pos[0], pos[1])

                if clicked_row is not None and clicked_column is not None:
                    cell = grid.cells[clicked_row][clicked_column]
                    cell.selected = not cell.selected
                    cell.visited = True

                    print(f"Clicked cell: ({clicked_row}, {clicked_column})")
                    print("Neighbors:")
                    neighbors = grid.get_neighbors(clicked_row, clicked_column)
                    for direction, neighbor in neighbors.items():
                        neighbor_row, neighbor_col = grid.get_cell_position(neighbor.x, neighbor.y)
                        print(f"  {direction}: ({neighbor_row}, {neighbor_col})")

        # Render the grid
        grid.draw(screen)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate to 60 FPS
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    game_loop()
