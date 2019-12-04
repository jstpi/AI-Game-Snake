import random
import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN
import data.dataUtils as data
from square import Square
from snake import Snake

class Game:

    FOOD = 3
    HEAD = 2
    SNAKE = 1
    SPACE = 0

    width = data.getConfig("width")
    rows = data.getConfig("rows")
    square_color = data.getConfig("squareColor")
    initial_snake_pos = data.getConfig("initialSnakePos")
    food_color = data.getConfig("foodColor")
    line_color = data.getConfig("lineColor")
    board_color = data.getConfig("boardColor")

    def __init__(self):
        '''snake game'''
        self.snake = Snake(self.initial_snake_pos, self.square_color)
        self.food = Square(self.random_food_pos(), self.food_color)

    def get_game_map_rows(self):
        '''return rows config'''
        return self.rows

    def get_snake_head_pos(self):
        '''return snake head pos [x, y]'''
        return self.snake.head.pos

    def get_snake_full_pos(self):
        '''return array for each of the snake body pos [x, y]'''
        return [body.pos for body in self.snake.body]

    def get_snake_dir(self):
        '''return snake dir [x, y]'''
        return self.snake.dir

    def get_food_pos(self):
        '''return food pos [x, y]'''
        return self.food.pos

    def get_score(self):
        '''return len of the snake body'''
        return len(self.snake.body)

    def draw_grid(self, surface):
        '''draw visual of the game grid'''
        size_between = self.width // self.rows
        grid_x = 0
        grid_y = 0
        for l in range(self.rows):
            grid_x = grid_x + size_between
            grid_y = grid_y + size_between
            pygame.draw.line(surface, self.line_color, (grid_x, 0), (grid_x, self.width))
            pygame.draw.line(surface, self.line_color, (0, grid_y), (self.width, grid_y))

    def redraw_window(self, surface):
        '''draw visual of the full game board'''
        surface.fill(self.board_color)
        self.snake.draw(surface)
        self.food.draw(surface)
        self.draw_grid(surface)
        pygame.display.update()

    def random_food_pos(self):
        '''return a valid random food position'''
        positions = self.snake.body
        while True:
            pos = [random.randrange(self.rows), random.randrange(self.rows)]
            if len(list(filter(lambda z: z.pos == pos, positions))) > 0:
                continue
            break
        return pos

    def move_snake_up(self):
        '''Trigger one input K_UP to the snake'''
        newevent = pygame.event.Event(pygame.KEYDOWN, unicode='', key=K_UP, mod=pygame.locals.KMOD_NONE, scancode=111, window=None)
        newevent2 = pygame.event.Event(pygame.KEYUP, key=K_UP, mod=pygame.locals.KMOD_NONE, scancode=111, window=None)
        pygame.event.post(newevent)
        pygame.event.post(newevent2)

    def move_snake_down(self):
        '''Trigger one input K_DOWN to the snake'''
        newevent = pygame.event.Event(pygame.KEYDOWN, unicode='', key=K_DOWN, mod=pygame.locals.KMOD_NONE, scancode=116, window=None)
        newevent2 = pygame.event.Event(pygame.KEYUP, key=K_DOWN, mod=pygame.locals.KMOD_NONE, scancode=116, window=None)
        pygame.event.post(newevent)
        pygame.event.post(newevent2)

    def move_snake_left(self):
        '''Trigger one input K_LEFT to the snake'''
        newevent = pygame.event.Event(pygame.KEYDOWN, unicode='', key=K_LEFT, mod=pygame.locals.KMOD_NONE, scancode=113, window=None)
        newevent2 = pygame.event.Event(pygame.KEYUP, key=K_LEFT, mod=pygame.locals.KMOD_NONE, scancode=113, window=None)
        pygame.event.post(newevent)
        pygame.event.post(newevent2)

    def move_snake_right(self):
        '''Trigger one input K_RIGHT to the snake'''
        newevent = pygame.event.Event(pygame.KEYDOWN, unicode='', key=K_RIGHT, mod=pygame.locals.KMOD_NONE, scancode=114, window=None)
        newevent2 = pygame.event.Event(pygame.KEYUP, key=K_RIGHT, mod=pygame.locals.KMOD_NONE, scancode=114, window=None)
        pygame.event.post(newevent)
        pygame.event.post(newevent2)

    def start(self):
        '''Main loop of the game'''
        win = pygame.display.set_mode((self.width, self.width))
        clock = pygame.time.Clock()

        while True:
            pygame.time.delay(50)
            clock.tick(10)
            self.snake.move()
            if self.snake.body[0].pos == self.food.pos:
                self.snake.add_cube()
                self.food = Square(self.random_food_pos(), self.food_color)

            if self.snake.alive == False:
                print('Score:', len(self.snake.body))
                self.snake.reset(self.initial_snake_pos)
                break
            self.redraw_window(win)