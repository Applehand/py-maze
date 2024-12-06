from models import Grid, Maze, GameSession
from utils import WHITE
from render import PygameRenderer

GRID_WIDTH = 10
GRID_HEIGHT = 10
CELL_MARGIN = 0

def loop(pygame, window_width, window_height):
    """Main game loop to handle events and rendering."""
    screen = pygame.display.set_mode((window_width, window_height))
    clock = pygame.time.Clock()
    renderer = PygameRenderer(pygame, screen)

    grid = Grid(GRID_WIDTH, GRID_HEIGHT, window_width, window_height, CELL_MARGIN)
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

        renderer.clear_screen(WHITE)
        grid.draw(renderer)
        renderer.update_screen()

        clock.tick(60)
