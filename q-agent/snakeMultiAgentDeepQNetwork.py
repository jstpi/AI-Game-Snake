# https://pypi.org/project/pyqlearning/
from pyqlearning.functionapproximator.cnn_fa import CNNFA
from pyqlearning.deepqlearning.deep_q_network import DeepQNetwork
import numpy as np
import random


class SnakeMultiAgentDeepQNetwork(DeepQNetwork):
    '''
    Multi-Agent Deep Q-Network to solive Snake problem.
    '''
    
    FOOD = 3
    HEAD = 2
    SNAKE = 1
    SPACE = 0
    
    END_STATE = "running"

    def __init__(
        self,
        function_approximator,
        game
    ):
        '''
        Init.
        
        Args:
            function_approximator:  is-a `FunctionApproximator`.
            game:                   Snake game with all the info.
        '''
        self.game = game
        self.gameMap = self.updateMap()
        self.snakePos = self.updateSnakePos()
        self.reward_list = []

        super().__init__(function_approximator)

    ## !!! IMPORTANT !!
    def extract_possible_actions(self, state_arr):
        '''
        Extract possible actions.
        Args:
            state_arr:  `np.ndarray` of state.
        
        Returns:
            `np.ndarray` of actions.
            The shape is:(
                `batch size corresponded to each action key`, 
                `channel that is 1`, 
                `feature points1`, 
                `feature points2`
            )
        '''
        agent_x, agent_y = np.where(state_arr[-1] == 1)
        agent_x, agent_y = agent_x[0], agent_y[0]

        possible_action_arr = None
        for x, y in [
            (-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)
        ]:
            next_x = agent_x + x
            if next_x < 0 or next_x >= state_arr[-1].shape[1]:
                continue
            next_y = agent_y + y
            if next_y < 0 or next_y >= state_arr[-1].shape[0]:
                continue

            wall_flag = False
            if x > 0:
                for add_x in range(1, x):
                    if self.__map_arr[agent_x + add_x, next_y] == self.WALL:
                        wall_flag = True
            elif x < 0:
                for add_x in range(x, 0):
                    if self.__map_arr[agent_x + add_x, next_y] == self.WALL:
                        wall_flag = True
                    
            if wall_flag is True:
                continue

            if y > 0:
                for add_y in range(1, y):
                    if self.__map_arr[next_x, agent_y + add_y] == self.WALL:
                        wall_flag = True
            elif y < 0:
                for add_y in range(y, 0):
                    if self.__map_arr[next_x, agent_y + add_y] == self.WALL:
                        wall_flag = True

            if wall_flag is True:
                continue

            if self.__map_arr[next_x, next_y] == self.WALL:
                continue

            if (next_x, next_y) in self.__route_memory_list:
                continue

            next_action_arr = np.zeros((
                 3 + self.__enemy_num,
                 state_arr[-1].shape[0],
                 state_arr[-1].shape[1]
            ))
            next_action_arr[0][agent_x, agent_y] = 1
            next_action_arr[1] = self.__map_arr
            next_action_arr[-1][next_x, next_y] = 1

            for e in range(self.__enemy_num):
                enemy_state_arr = np.zeros(state_arr[0].shape)
                enemy_state_arr[self.__enemy_pos_list[e][0], self.__enemy_pos_list[e][1]] = 1
                next_action_arr[2 + e] = enemy_state_arr

            next_action_arr = np.expand_dims(next_action_arr, axis=0)
            if possible_action_arr is None:
                possible_action_arr = next_action_arr
            else:
                possible_action_arr = np.r_[possible_action_arr, next_action_arr]

        if possible_action_arr is not None:
            while possible_action_arr.shape[0] < self.__batch_size:
                key = np.random.randint(low=0, high=possible_action_arr.shape[0])
                possible_action_arr = np.r_[
                    possible_action_arr,
                    np.expand_dims(possible_action_arr[key], axis=0)
                ]
        else:
            # Forget oldest memory and do recuresive executing.
            self.__route_memory_list = self.__route_memory_list[1:]
            possible_action_arr = self.extract_possible_actions(state_arr)

        return possible_action_arr

    ## !! IMPORTANT !!
    def observe_reward_value(self, state_arr, action_arr):
        '''
        Compute the reward value.
        
        Args:
            state_arr:              `np.ndarray` of state.
            action_arr:             `np.ndarray` of action.
        
        Returns:
            Reward value.
        '''
        if self.__check_goal_flag(action_arr) is True:
            return 1.0
        else:
            self.__move_enemy(action_arr)

            x, y = np.where(action_arr[-1] == 1)
            x, y = x[0], y[0]

            e_dist_sum = 0.0
            for e in range(self.__enemy_num):
                e_dist = np.sqrt(
                    ((x - self.__enemy_pos_list[e][0]) ** 2) + ((y - self.__enemy_pos_list[e][1]) ** 2)
                )
                e_dist_sum += e_dist

            e_dist_penalty = e_dist_sum / self.__enemy_num
            goal_x, goal_y = self.__goal_pos
            
            if x == goal_x and y == goal_y:
                distance = 0.0
            else:
                distance = np.sqrt(((x - goal_x) ** 2) + (y - goal_y) ** 2)

            if (x, y) in self.__route_long_memory_list:
                repeating_penalty = self.__repeating_penalty
            else:
                repeating_penalty = 0.0

            return 1.0 - distance - repeating_penalty + e_dist_penalty

    # !! IMPORTANT !!
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
        x, y = np.where(action_arr[-1] == 1)
        self.__agent_pos = (x[0], y[0])
        self.__route_memory_list.append((x[0], y[0]))
        self.__route_long_memory_list.append((x[0], y[0]))
        self.__route_long_memory_list = list(set(self.__route_long_memory_list))
        while len(self.__route_memory_list) > self.__memory_num:
            self.__route_memory_list = self.__route_memory_list[1:]

        return self.extract_now_state()

    def __check_goal_flag(self, state_arr):
        x, y = np.where(state_arr[0] == 1)
        goal_x, goal_y = self.__goal_pos
        if x[0] == goal_x and y[0] == goal_y:
            self.END_STATE = "Goal"
            return True
        else:
            return False
    
    def __check_crash_flag(self, state_arr):
        x, y = np.where(state_arr[-1] == 1)
        x, y = x[0], y[0]

        flag = False
        for e in range(self.__enemy_num):
            if x == self.__enemy_pos_list[e][0] and y == self.__enemy_pos_list[e][1]:
                flag = True
                break

        if flag is True:
            self.END_STATE = "Crash"
        return flag
    
    # !! IMPORTANT !!
    def check_the_end_flag(self, state_arr):
        '''
        Check the end flag.
        
        If this return value is `True`, the learning is end.
        As a rule, the learning can not be stopped.
        This method should be overrided for concreate usecases.
        Args:
            state_arr:    `np.ndarray` of state in `self.t`.
        Returns:
            bool
        '''
        if self.__check_goal_flag(state_arr) is True or self.__check_crash_flag(state_arr):
            return True
        else:
            return False

    def updateMap(self):
        return np.array(self.game.gameMap)

    def updateSnakePos(self):
        return self.game.getSnakePos()