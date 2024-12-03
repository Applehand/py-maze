import pygame

WINDOW_HEIGHT = 255
WINDOW_WIDTH = 255

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)

cell_width, cell_height, cell_margin = 20, 20, 5
grid_height, grid_width = 10, 10


def is_within_grid(row, col):
    return 0 <= row < grid_height and 0 <= col < grid_width


class Cell:
    def __init__(self, pos_x, pos_y, width, height, color=WHITE):
        self.x = pos_x # x pixel coord for pygame drawing
        self.y = pos_y # y pixel coord for pygame drawing
        self.width = width
        self.height = height
        self.color = color
        self.col = self.x // (cell_width + cell_margin) # col pos in grid
        self.row = self.y // (cell_height + cell_margin) # row pos in grid
        self.selected = False
        self.visited = False

    @property
    def neighbors(self):
        neighbors = {}

        directions = {
            "N": (self.row - 1, self.col),
            "S": (self.row + 1, self.col),
            "W": (self.row, self.col - 1),
            "E": (self.row, self.col + 1),
        }

        for direction, (neighbor_row, neighbor_col) in directions.items():
            if is_within_grid(neighbor_row, neighbor_col):
                neighbors[direction] = grid[neighbor_row][neighbor_col]

        return neighbors

    def draw(self, screen):
        if self.selected:
            self.color = GREEN
        elif self.visited:
            self.color = GREY
        else:
            self.color = WHITE
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


grid = []
for row in range(grid_height):
    grid.append([])
    for col in range(grid_width):
        pos_x = (cell_margin + cell_width) * col + cell_margin
        pos_y = (cell_margin + cell_height) * row + cell_margin
        grid[row].append(Cell(pos_x, pos_y, cell_width, cell_height))


def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    running = True
    while running:
        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                clicked_column = pos[0] // (cell_width + cell_margin)
                clicked_row = pos[1] // (cell_height + cell_margin)
                if 0 <= clicked_row < grid_height and 0 <= clicked_column < grid_width:
                    cell = grid[clicked_row][clicked_column]
                    cell.selected = not cell.selected
                    cell.visited = True

                    print(f"Clicked cell: ({clicked_row}, {clicked_column})")
                    print("Neighbors:")
                    for direction, neighbor in cell.neighbors.items():
                        print(f"  {direction}: ({neighbor.row}, {neighbor.col})")


        # Fill the screen with a color to wipe away anything from last frame
        screen.fill(BLACK)

        # Render game here
        for row in grid:
            for cell in row:
                cell.draw(screen)

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # Limits FPS to 60

    pygame.quit()


if __name__ == "__main__":
    game_loop()
