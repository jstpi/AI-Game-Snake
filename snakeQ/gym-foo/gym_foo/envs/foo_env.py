import gym
from gym import error, spaces, utils
from gym.utils import seeding
from game import Game
import numpy as np

class FooEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.game = Game(ai_mode=True)

        self.maze_size = self.game.get_game_map_size()

        self.action_space = spaces.Discrete(4)

        # observation is the x, y coordinate of the grid
        low = np.zeros(len(self.maze_size), dtype=int)
        high = np.array(self.maze_size, dtype=int) - np.ones(len(self.maze_size), dtype=int)
        self.observation_space = spaces.Box(low, high, dtype=np.int64)

        self.game.reset()

    def step(self, action):
        if action == 0:
            # print("right")
            self.game.move_snake_right()
        if action == 1:
            # print("left")
            self.game.move_snake_left()
        if action == 2:
            # print("up")
            self.game.move_snake_up()
        if action == 3:
            # print("down")
            self.game.move_snake_down()

        score = self.game.get_score()
        food_pos = self.game.get_food_pos()
        snake_pos = self.game.get_snake_head_pos()
        done = False
        reward = 0

        if score == 8:
            reward = 1000
            done = True
        elif not self.game.is_snake_alive():
            reward = -1000
            done = True
        else:
            food_dist = np.sqrt(
                ((snake_pos[0] - food_pos[0]) ** 2) + ((snake_pos[1] - food_pos[1]) ** 2)
                )

            rows = self.game.get_game_map_rows()

            rel_dist = np.sqrt(
                ((rows) ** 2) + ((rows) ** 2)
            )

            reward = score - (food_dist / rel_dist)

        info = {}

        return np.array(snake_pos), reward, done, info

    def reset(self):
        self.game.reset()
        snake_pos = self.game.get_snake_head_pos()
        return np.array(snake_pos)

    def render(self, mode="human", close=False):
        if close:
            self.game.quit_game()

        return np.array(self.game.update())