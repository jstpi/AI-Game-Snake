# https://pypi.org/project/pyqlearning/
import threading
from pyqlearning.deepqlearning.deep_q_network import DeepQNetwork
import numpy as np

class SnakeMultiAgentDeepQNetwork(DeepQNetwork):
    '''
    Multi-Agent Deep Q-Network to solive Snake problem.
    '''

    A_RIGHT = 1
    A_LEFT = 2
    A_DOWN = 3
    A_UP = 4

    def __init__(self, function_approximator, game, max_score):
        '''
        Init.

        Args:
            function_approximator:  is-a `FunctionApproximator`.
            game:                   Snake game with all the info.
            max_score:              maximum score for the training.
        '''
        self.game = game
        self.max_score = max_score

        super().__init__(function_approximator)

    def inference(self, state_arr, limit=1000):
        '''
        Infernce.

        Args:
            state_arr:    `np.ndarray` of state.
            limit:        The number of inferencing.

        Returns:
            `list of `np.ndarray` of an optimal route.
        '''
        game_thread = threading.Thread(target=self.game.start)
        game_thread.start()

        snake_head_x, snake_head_y = np.where(state_arr[2] == 1)
        snake_head_x, snake_head_y = snake_head_x[0], snake_head_y[0]

        result_list = [(snake_head_x, snake_head_y, 0.0)]

        self.t = 0
        while self.t < limit:
            next_action_arr = self.extract_possible_actions(state_arr)
            next_q_arr = self.function_approximator.inference_q(next_action_arr)
            action_arr, q = self.select_action(next_action_arr, next_q_arr)

            snake_head_x, snake_head_y = np.where(state_arr[2] == 1)
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
                game_thread.join()
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

        possible_action = np.zeros(4)
        possible_action[0] = self.A_RIGHT
        possible_action[1] = self.A_LEFT
        possible_action[2] = self.A_DOWN
        possible_action[3] = self.A_UP

        return np.expand_dims(possible_action, axis=0)

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

        snake_head_x, snake_head_y = np.where(state_arr[2] == 1)
        snake_head_x, snake_head_y = snake_head_x[0], snake_head_y[0]

        if action_arr[0] == self.A_RIGHT:
            snake_head_x += 1
        if action_arr[0] == self.A_LEFT:
            snake_head_x -= 1
        if action_arr[0] == self.A_DOWN:
            snake_head_y += 1
        if action_arr[0] == self.A_UP:
            snake_head_y -= 1

        food_x, food_y = np.where(state_arr[1] == 1)
        food_x, food_y = food_x[0], food_y[0]

        food_dist = np.sqrt(((snake_head_x - food_x) ** 2) + ((snake_head_y - food_y) ** 2))

        score = np.count_nonzero(state_arr[0] == 1)

        return score + food_dist

    def extract_now_state(self):
        '''
        Extract now map state.

        Returns:
            `np.ndarray` of state.
        '''
        rows = self.game.get_game_map_rows()
        snake_body_pos = self.game.get_snake_full_pos()
        food_pos = self.game.get_food_pos()
        snake_head_pos = self.game.get_snake_head_pos()
        snake_dir = self.game.get_snake_dir()

        snake_map = np.zeros(rows*rows)
        for body_pos in snake_body_pos:
            snake_map[body_pos[0], body_pos[1]] = 1
        np.expand_dims(snake_map, axis=0)

        food_map = np.zeros(rows*rows)
        food_map[food_pos[0], food_pos[1]] = 1
        np.expand_dims(food_map, axis=0)

        head_map = np.zeros(rows*rows)
        head_map[snake_head_pos[0], snake_head_pos[1]] = 1
        np.expand_dims(head_map, axis=0)

        dir_map = np.zeros(4)

        # Left
        if snake_dir[0] == -1:
            dir_map[0] = 1

        # Right
        if snake_dir[0] == 1:
            dir_map[1] = 1

        # UP
        if snake_dir[1] == -1:
            dir_map[2] = 1

        # Down
        if snake_dir[1] == 1:
            dir_map[3] = 1

        # [Left, Right, Up, Down]
        np.expand_dims(dir_map, axis=0)

        alive_map = np.zeros(1)
        if self.game.is_snake_alive():
            alive_map[0] = 1
        else:
            alive_map[0] = 0

        state_map = np.concatenate((snake_map, food_map, head_map, dir_map, alive_map), axis=0)
        return state_map

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

        if action_arr[0] == self.A_RIGHT:
            self.game.move_snake_right()
        if action_arr[0] == self.A_LEFT:
            self.game.move_snake_left()
        if action_arr[0] == self.A_DOWN:
            self.game.move_snake_down()
        if action_arr[0] == self.A_UP:
            self.game.move_snake_up()

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

        return state_arr[4] == 0 or np.count_nonzero(state_arr[0] == 1) == self.max_score
