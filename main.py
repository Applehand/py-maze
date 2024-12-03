import pygame

WINDOW_HEIGHT = 255
WINDOW_WIDTH = 255

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

cell_width, cell_height, cell_margin = 20, 20, 5
grid_height, grid_width = 10, 10


class Cell:
    def __init__(self, pos_x, pos_y, width, height, color=WHITE):
        self.x = pos_x
        self.y = pos_y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen):
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
                print(f"Clicked at:{clicked_column, clicked_row}",)


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
