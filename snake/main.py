import pygame
import random
import data.dataUtils as data
from square import Square
from snake import Snake

def draw_grid(surface):
    '''draw visual of the game grid'''
    width = data.getConfig("width")
    rows = data.getConfig("rows")
    line_color = data.getConfig("lineColor")
    size_between = width // rows
    grid_x = 0
    grid_y = 0
    for l in range(rows):
        grid_x = grid_x + size_between
        grid_y = grid_y + size_between
        pygame.draw.line(surface, line_color, (grid_x, 0), (grid_x, width))
        pygame.draw.line(surface, line_color, (0, grid_y), (width, grid_y))

def redraw_window(surface, snake, food):
    '''draw visual of the full game board'''
    board_color = data.getConfig("boardColor")
    surface.fill(board_color)
    snake.draw(surface)
    food.draw(surface)
    draw_grid(surface)
    pygame.display.update()

def random_food_pos(snake):
    '''return a valid random food position'''
    rows = data.getConfig("rows")
    positions = snake.body
    while True:
        pos = [random.randrange(rows), random.randrange(rows)]
        if len(list(filter(lambda z: z.pos == pos, positions))) > 0:
            continue
        break
    return pos

def main():
    '''snake game'''
    width = data.getConfig("width")
    square_color = data.getConfig("squareColor")
    initial_snake_pos = data.getConfig("initialSnakePos")
    food_color = data.getConfig("foodColor")
    win = pygame.display.set_mode((width, width))
    snake = Snake(initial_snake_pos, square_color)
    food = Square(random_food_pos(snake), food_color)

    clock = pygame.time.Clock()

    while True:
        pygame.time.delay(50)
        clock.tick(10)
        snake.move()
        if snake.body[0].pos == food.pos:
            snake.add_cube()
            food = Square(random_food_pos(snake), food_color)

        if snake.alive == False:
            print('Score:', len(snake.body))
            snake.reset(initial_snake_pos)
            break
        redraw_window(win, snake, food)

main()
