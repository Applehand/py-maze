from models import Grid, Maze, GameSession
from utils import WHITE

def loop(pygame, window_width, window_height, grid_width, grid_height, cell_margin):
    """Main game loop to handle events and rendering."""
    screen = pygame.display.set_mode((window_width, window_height))
    clock = pygame.time.Clock()

    grid = Grid(grid_width, grid_height, window_width, window_height, cell_margin)
    maze = Maze(grid)
    game_session = GameSession(maze, "default")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                direction_map = {
                    pygame.K_UP: "N",
                    pygame.K_DOWN: "S",
                    pygame.K_LEFT: "W",
                    pygame.K_RIGHT: "E",
                }
                if event.key in direction_map:
                    direction = direction_map[event.key]
                    cur_row, cur_col = grid.get_cell_position(
                        game_session.current_cell.x, game_session.current_cell.y
                    )
                    neighbors = grid.get_neighbors(cur_row, cur_col)
                    if direction in neighbors:
                        target_cell = neighbors[direction]
                        if not grid.has_wall_between(game_session.current_cell, target_cell):
                            game_session.move_player_to_cell(game_session.current_cell, target_cell)

        screen.fill(WHITE)
        grid.draw(screen, pygame.draw)
        pygame.display.flip()
        clock.tick(60)
