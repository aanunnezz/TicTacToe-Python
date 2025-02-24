import pygame as pg
import sys
import time

pg.init()

WIDTH, HEIGHT = 400, 400
BACKGROUND = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)
WIN_LINE_COLOR = (250, 0, 0)

grid = [[None] * 3 for _ in range(3)]
screen = pg.display.set_mode((WIDTH, HEIGHT + 100))
pg.display.set_caption("Tic Tac Toe")
clock = pg.time.Clock()
FPS = 30
current_player = 'x'
current_winner = None
is_draw = False
game_over = False


def draw_grid():
    screen.fill(BACKGROUND)
    for i in range(1, 3):
        pg.draw.line(screen, LINE_COLOR, (WIDTH / 3 * i, 0), (WIDTH / 3 * i, HEIGHT), 7)
        pg.draw.line(screen, LINE_COLOR, (0, HEIGHT / 3 * i), (WIDTH, HEIGHT / 3 * i), 7)


def draw_status():
    status_message = f"{current_player.upper()}'s Turn"
    if current_winner:
        status_message = f"{current_winner.upper()} Won!"
    elif is_draw:
        status_message = "Game Draw!"
    
    font = pg.font.Font(None, 36)
    text = font.render(status_message, True, TEXT_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT + 50))
    
    pg.draw.rect(screen, BACKGROUND, (0, HEIGHT, WIDTH, 100))
    screen.blit(text, text_rect)
    pg.display.update()


def check_win():
    global current_winner, is_draw, game_over

    for row in range(3):
        if grid[row][0] == grid[row][1] == grid[row][2] and grid[row][0]:
            current_winner = grid[row][0]
            pg.draw.line(screen, WIN_LINE_COLOR,
                         (0, (row + 1) * HEIGHT / 3 - HEIGHT / 6),
                         (WIDTH, (row + 1) * HEIGHT / 3 - HEIGHT / 6), 4)
            game_over = True
            return

    for col in range(3):
        if grid[0][col] == grid[1][col] == grid[2][col] and grid[0][col]:
            current_winner = grid[0][col]
            pg.draw.line(screen, WIN_LINE_COLOR,
                         ((col + 1) * WIDTH / 3 - WIDTH / 6, 0),
                         ((col + 1) * WIDTH / 3 - WIDTH / 6, HEIGHT), 4)
            game_over = True
            return

    if grid[0][0] == grid[1][1] == grid[2][2] and grid[0][0]:
        current_winner = grid[0][0]
        pg.draw.line(screen, WIN_LINE_COLOR, (50, 50), (350, 350), 4)
        game_over = True
        return

    if grid[0][2] == grid[1][1] == grid[2][0] and grid[0][2]:
        current_winner = grid[0][2]
        pg.draw.line(screen, WIN_LINE_COLOR, (350, 50), (50, 350), 4)
        game_over = True
        return

    if all(all(row) for row in grid):
        is_draw = True
        game_over = True


def draw_xo(row, col):
    global current_player
    x, y = col * WIDTH // 3 + WIDTH // 6, row * HEIGHT // 3 + HEIGHT // 6
    size = 50

    if current_player == 'x':
        pg.draw.line(screen, TEXT_COLOR, (x - size, y - size), (x + size, y + size), 5)
        pg.draw.line(screen, TEXT_COLOR, (x + size, y - size), (x - size, y + size), 5)
        grid[row][col] = 'x'
        current_player = 'o'
    else:
        pg.draw.circle(screen, TEXT_COLOR, (x, y), size, 5)
        grid[row][col] = 'o'
        current_player = 'x'

    pg.display.update()


def user_click():
    if game_over:
        return

    x, y = pg.mouse.get_pos()
    col, row = x // (WIDTH // 3), y // (HEIGHT // 3)

    if grid[row][col] is None:
        draw_xo(row, col)
        check_win()
        draw_status()


def reset_game():
    global grid, current_player, current_winner, is_draw, game_over
    time.sleep(10)  # Espera 10 segundos en vez de los 3 originales
    grid = [[None] * 3 for _ in range(3)]
    current_player, current_winner, is_draw, game_over = 'x', None, False, False
    draw_grid()
    draw_status()


draw_grid()
draw_status()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN and not game_over:
            user_click()
        elif game_over and event.type == pg.MOUSEBUTTONDOWN:
            reset_game()

    pg.display.update()
    clock.tick(FPS)
