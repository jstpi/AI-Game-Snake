# https://pypi.org/project/pyqlearning/
import threading
from pyqlearning.deepqlearning.deep_q_network import DeepQNetwork
import numpy as np

class SnakeMultiAgentDeepQNetwork(DeepQNetwork):
    '''
    Multi-Agent Deep Q-Network to solive Snake problem.
    '''

    SPACE = 0
    SNAKE = 1
    HEAD = 2
    FOOD = 3

    def __init__(self, function_approximator, batch_size, game, max_score):
        '''
        Init.

        Args:
            function_approximator:  is-a `FunctionApproximator`.
            game:                   Snake game with all the info.
            max_score:              maximum score for the training.
        '''
        self.batch_size = batch_size
        self.game = game
        self.game_map = self.build_map()
        self.max_score = max_score

        super().__init__(function_approximator)

    def build_map(self):
        '''return updated game map'''
        rows = self.game.get_game_map_rows()
        snake_body_pos = self.game.get_snake_full_pos()
        snake_head_pos = self.game.get_snake_head_pos()
        food_pos = self.game.get_food_pos()

        game_map = np.full((rows, rows), self.SPACE)
        for body_pos in snake_body_pos:
            game_map[body_pos[0], body_pos[1]] = self.SNAKE
        game_map[snake_head_pos[0], snake_head_pos[1]] = self.HEAD
        game_map[food_pos[0], food_pos[1]] = self.FOOD

        return game_map

    def inference(self, state_arr, limit=1000):
        '''
        Infernce.

        Args:
            state_arr:    `np.ndarray` of state.
            limit:        The number of inferencing.

        Returns:
            `list of `np.ndarray` of an optimal route.
        '''
        # game_thread = threading.Thread(target=self.game.start)
        # print("START")
        # game_thread.start()

        snake_head_x, snake_head_y = np.where(state_arr[-1] == 1)
        snake_head_x, snake_head_y = snake_head_x[0], snake_head_y[0]

        result_list = [(snake_head_x, snake_head_y, 0.0)]

        self.t = 0
        while self.t < limit:
            next_action_arr = self.extract_possible_actions(state_arr)
            next_q_arr = self.function_approximator.inference_q(next_action_arr)
            action_arr, q = self.select_action(next_action_arr, next_q_arr)

            snake_head_x, snake_head_y = np.where(state_arr[-1] == 1)
            snake_head_x, snake_head_y = snake_head_x[0], snake_head_y[0]

            result_val_list = [snake_head_x, snake_head_y]
            try:
                result_val_list.append(q[0])
            except IndexError:
                result_val_list.append(q)

            result_list.append(tuple(result_val_list))

            # Update State.
            state_arr = self.update_state(state_arr, action_arr)

            # Epsode.
            self.t += 1
            # Check.
            end_flag = self.check_the_end_flag(state_arr)
            if end_flag is True:
                self.game.kill_snake()
                break

        return result_list

    def extract_possible_actions(self, state_arr):
        '''
        Extract possible actions.
        This method is overrided.
        Args:
            state_arr:  `np.ndarray` of state.

        Returns:
            `np.ndarray` of actions.
        '''

        snake_head_x, snake_head_y = np.where(state_arr[-1] == 1)
        snake_head_x, snake_head_y = snake_head_x[0], snake_head_y[0]

        possible_action_arr = None
        for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_snake_head_x = snake_head_x + x
            next_snake_head_y = snake_head_y + y

            if next_snake_head_x < 0 or next_snake_head_x >= state_arr[-1].shape[1]:
                continue
            if next_snake_head_y < 0 or next_snake_head_y >= state_arr[0].shape[0]:
                continue

            if self.game_map[next_snake_head_x, next_snake_head_y] == self.SNAKE:
                continue

            next_action_arr = np.zeros((
                3,
                state_arr[-1].shape[0],
                state_arr[-1].shape[1]
            ))
            next_action_arr[0][snake_head_x, snake_head_y] = 1
            next_action_arr[1] = self.game_map
            next_action_arr[-1][next_snake_head_x, next_snake_head_y] = 1

            next_action_arr = np.expand_dims(next_action_arr, axis=0)

            if possible_action_arr is None:
                possible_action_arr = next_action_arr
            else:
                possible_action_arr = np.r_[possible_action_arr, next_action_arr]

        if possible_action_arr is not None:
            while possible_action_arr.shape[0] < self.batch_size:
                key = np.random.randint(low=0, high=possible_action_arr.shape[0])
                possible_action_arr = np.r_[
                    possible_action_arr,
                    np.expand_dims(possible_action_arr[key], axis=0)
                ]

        return possible_action_arr

    def observe_reward_value(self, state_arr, action_arr):
        '''
        Compute the reward value.
        This method is overrided.
        Args:
            state_arr:              `np.ndarray` of state.
            action_arr:             `np.ndarray` of action.

        Returns:
            Reward value.
        '''

        next_snake_head_x, next_snake_head_y = np.where(state_arr[-1] == 1)
        next_snake_head_x, next_snake_head_y = next_snake_head_x[0], next_snake_head_y[0]

        food_pos = self.game.get_food_pos()

        food_dist = np.sqrt(
            ((next_snake_head_x - food_pos[0]) ** 2) + ((next_snake_head_y - food_pos[1]) ** 2)
            )

        rows = self.game.get_game_map_rows()

        rel_dist = np.sqrt(
            ((rows) ** 2) + ((rows) ** 2)
        )

        close_to_food_score = 1 - (food_dist / rel_dist)

        score = self.game.get_score()

        return score + close_to_food_score

    def extract_now_state(self):
        '''
        Extract now map state.

        Returns:
            `np.ndarray` of state.
        '''
        rows = self.game.get_game_map_rows()
        snake_head_pos = self.game.get_snake_head_pos()
        state_arr = np.zeros((rows, rows))
        state_arr[snake_head_pos[0], snake_head_pos[1]] = 1
        return np.expand_dims(state_arr, axis=0)

    def update_state(self, state_arr, action_arr):
        '''
        Update state.

        Override.
        Args:
            state_arr:    `np.ndarray` of state in `self.t`.
            action_arr:   `np.ndarray` of action in `self.t`.

        Returns:
            `np.ndarray` of state in `self.t+1`.
        '''

        snake_head_x, snake_head_y = np.where(state_arr[-1] == 1)
        snake_head_x, snake_head_y = snake_head_x[0], snake_head_y[0]

        next_snake_head_x, next_snake_head_y = np.where(action_arr[-1] == 1)
        next_snake_head_x, next_snake_head_y = next_snake_head_x[0], next_snake_head_y[0]

        diff_x = next_snake_head_x - snake_head_x
        diff_y = next_snake_head_y - snake_head_y

        if diff_x > 0:
            self.game.move_snake_right()
            #print("right")
        if diff_x < 0:
            self.game.move_snake_left()
            #print("left")
        if diff_y > 0:
            self.game.move_snake_down()
            #print("down")
        if diff_y < 0:
            self.game.move_snake_up()
            #print("up")

        self.game_map = self.build_map()

        return self.extract_now_state()

    def check_the_end_flag(self, state_arr):
        '''
        Check the end flag.

        If this return value is `True`, the learning is end.
        This method is overrided.
        As a rule, the learning can not be stopped.
        This method should be overrided for concreate usecases.
        Args:
            state_arr:    `np.ndarray` of state in `self.t`.
        Returns:
            bool
        '''

        dead = not self.game.is_snake_alive()
        max_score = self.game.get_score() >= self.max_score

        return dead or max_score
