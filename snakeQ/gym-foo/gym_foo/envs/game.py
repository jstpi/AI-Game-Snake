import random
import pygame
from pygame.locals import QUIT, K_LEFT, K_RIGHT, K_UP, K_DOWN
import data.dataUtils as data
from square import Square
from snake import Snake

class Game:
    width = data.getConfig("width")
    rows = data.getConfig("rows")
    square_color = data.getConfig("squareColor")
    initial_snake_pos = data.getConfig("initialSnakePos")
    food_color = data.getConfig("foodColor")
    line_color = data.getConfig("lineColor")
    board_color = data.getConfig("boardColor")

    def __init__(self, ai_mode=False):
        '''snake game'''
        self.snake = Snake(self.initial_snake_pos, self.square_color)
        self.food = Square(self.random_food_pos(), self.food_color)
        self.ai_mode = ai_mode
        self.surface = pygame.display.set_mode((self.width, self.width))
        self.clock = pygame.time.Clock()

    def get_game_map_rows(self):
        '''return rows config'''
        return self.rows

    def get_game_map_size(self):
        return (self.rows, self.rows)

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

    def is_snake_alive(self):
        '''return True if the snake is alive'''
        return self.snake.alive

    def kill_snake(self):
        '''set snake.alive to False'''
        self.snake.alive = False

    def move_snake_up(self):
        '''Move the snake up'''
        self.snake.move_snake_up()

    def move_snake_down(self):
        '''Move the snake down'''
        self.snake.move_snake_down()

    def move_snake_left(self):
        '''Move the snake left'''
        self.snake.move_snake_left()

    def move_snake_right(self):
        '''Move the snake right'''
        self.snake.move_snake_right()

    def draw_grid(self):
        '''draw visual of the game grid'''
        size_between = self.width // self.rows
        grid_x = 0
        grid_y = 0
        for l in range(self.rows):
            grid_x = grid_x + size_between
            grid_y = grid_y + size_between
            pygame.draw.line(self.surface, self.line_color, (grid_x, 0), (grid_x, self.width))
            pygame.draw.line(self.surface, self.line_color, (0, grid_y), (self.width, grid_y))

    def redraw_window(self):
        '''draw visual of the full game board'''
        self.surface.fill(self.board_color)
        self.snake.draw(self.surface)
        self.food.draw(self.surface)
        self.draw_grid()
        pygame.display.update()
        return pygame.surfarray.array3d(pygame.display.get_surface())

    def random_food_pos(self):
        '''return a valid random food position'''
        positions = self.snake.body
        while True:
            pos = [random.randrange(self.rows), random.randrange(self.rows)]
            if len(list(filter(lambda z: z.pos == pos, positions))) > 0:
                continue
            break
        return pos

    def update(self):
        '''update the game state'''
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
                pygame.quit()
        if self.snake.body[0].pos == self.food.pos:
            self.snake.add_cube()
            self.food = Square(self.random_food_pos(), self.food_color)
        if not self.is_snake_alive():
            print('Score:', len(self.snake.body))
        return self.redraw_window()

    def reset(self):
        '''reset the game'''
        self.snake.reset(data.getConfig("initialSnakePos"))
        self.food = Square(self.random_food_pos(), self.food_color)
        self.snake.alive = True

    def quit_game(self):
        pygame.display.quit()
        pygame.quit()

    def start(self):
        '''Main loop of the game'''
        while True:

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    break

            if not self.ai_mode:
                pygame.time.delay(100)
                self.clock.tick(10)
                self.snake.move()
                
            if self.snake.body[0].pos == self.food.pos:
                self.snake.add_cube()
                self.food = Square(self.random_food_pos(), self.food_color)

            if not self.is_snake_alive():
                print('Score:', len(self.snake.body))
                self.snake.reset(data.getConfig("initialSnakePos"))
                self.snake.alive = True
                break
            self.redraw_window()
