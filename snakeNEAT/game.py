import random
import pygame
import numpy as np
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
        self.size = 0

    def get_inputs(self):
        return[self.get_snake_head_pos(), self.get_snake_dir(), self.get_food_pos()]
        #return[self.get_snake_head_pos(), self.get_snake_full_pos(), self.get_snake_dir()]

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

    def send_inputs(self,net):
        '''Envoie 200 input à notre reseau de neuronne
        On commence par faire une matrice de taille 10x10 remplies de 0
        On insère la position courante de la tête du snake
        On refais la meme chose pour la position de la nourriture
        On transforme les deux matrices en liste unidimensionnels et on les appends ensemble
        On envoie nos 200 inputs à notre réseaux, on recois 4 ouput entre -1 et 1
        Dépendemment des outputs, on donne un certains mouvement
        La partie commenté au millieu est une méthode vorace qui avais beaucoup plus de succès
        '''
        matrixS = np.zeros((10, 10))
        snakePos = self.get_snake_head_pos()
        print(snakePos)
        matrixS[snakePos[0],snakePos[1]]=1
        inputS = np.squeeze(np.asarray(matrixS))

        matrixF = np.zeros((10, 10))
        foodPos = self.get_food_pos()
        matrixF[foodPos[0],foodPos[1]]=1
        inputF = np.squeeze(np.asarray(matrixF))

        input = np.append(inputS,inputF)

        output = net.activate(input)
        print(output)

        #méthode vorace
        # x = input[0]-input[4]
        # y = input[1]-input[5]
        #
        # if (x<0 and y<=0):
        #     if (x<y):
        #         self.move_snake_right()
        #     else:
        #         self.move_snake_down()
        # elif(x>=0 and y>=0):
        #     if (x>y):
        #         self.move_snake_left()
        #     else:
        #         self.move_snake_up()
        #
        # elif (x>=0 and y<=0):
        #     if (x>abs(y)):
        #         self.move_snake_left()
        #     else:
        #         self.move_snake_down()
        # elif (x<0 and y>0):
        #     if (abs(x)>y):
        #         self.move_snake_right()
        #
        #     else:
        #         self.move_snake_up()

        if (output[0]>=output[1] and output[0]>=output[2] and output[0]>=output[3]):
            self.move_snake_right()
        elif (output[1]>=output[0] and output[1]>=output[2] and output[1]>=output[3]):
            self.move_snake_left()
        elif (output[2]>=output[1] and output[2]>=output[0] and output[2]>=output[3]):
            self.move_snake_up()
        else:
            self.move_snake_down()

    def isCloser(self, snakeBefore, foodBefore):
        '''Regarde la position avant et après et retourne l'augmentation du fitness
        Retourne 10 si le snake a trouvé le food
        Retourne 1 si le snake a fait un mouvement vers le food
        Retourne -2 si le snake fait un mouvement plus loins du food'''
        snakeNow = self.get_snake_head_pos()
        foodNow = self.get_food_pos()
        distanceToFoodBefore = abs(snakeBefore[0]-foodBefore[0])+ abs(snakeBefore[1]-foodBefore[1])
        distanceToFoodNow = abs(snakeNow[0]-foodNow[0])+ abs(snakeNow[1]-foodNow[1])

        if (foodBefore[0]!=foodNow[0] or foodBefore[1]!=foodNow[1]):
            return 10
        elif(distanceToFoodNow < distanceToFoodBefore ):
            return 1
        else:
            return -2


    def start(self, net, genome):
        '''Main loop of the game'''
        self.size=0
        win = pygame.display.set_mode((self.width, self.width))
        clock = pygame.time.Clock()
        flag=True
        counter = 0
        while flag:
            counter+=1
            #if statement pour limité le nombre de mouvement à 50
            if counter>50:
                self.snake.alive=False
            # pygame.time.delay(50)
            # clock.tick(10)

            #les données avant un mouvement
            snakeBefore = self.get_snake_head_pos()[:]
            food = self.get_food_pos()
            #appel send inputs qui va envoyer envoyer des inputs dans noter RN et ensuite faire un mouvement
            self.send_inputs(net)
            #fonction qui prend les events de deplacement et l'applique
            self.snake.move()
            #augmentation du fitness
            genome.fitness += self.isCloser(snakeBefore,food)

            #si le serpent a mangé une nourriture
            if self.snake.body[0].pos == self.food.pos:
                self.snake.add_cube()
                self.food = Square(self.random_food_pos(), self.food_color)

            #si le serpent meurt
            if self.snake.alive == False:
                genome.fitness -= 10
                self.size = len(self.snake.body)
                print('Score:', self.size)
                self.snake.reset(data.getConfig("initialSnakePos"))
                self.snake.alive = True
                flag=False
            self.redraw_window(win)
