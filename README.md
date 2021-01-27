# Snake Game AI
Project for the course CSI4506 of the University of Ottawa. Experimentation on the efficiency of the Q Learning, NEAT learning and gready approach to teach an AI to play the snake game.

## Contributors
* Jérémie St-Pierre (8628942)
* Frédérik Laflèche (8616081)

## Dependencies
* pip3 install pygame
* (Ubuntu): sudo apt-get install python3-dev

## Q-Learning

### Path
* SnakeQ
  * gym-foo/
    * setup.py
    * gym_foo/
      * __init__.py
      * envs/
        * __init__.py
        * foo_env.py
        * game.py
        * main.py
        * q_agent.py
        * snake.py
        * square.py
        * data/
          * config.json
          * dataUtils.py

### Dependencies
* pip3 install gym
* pip3 install numpy
* cd snakeQ/gym_foo pip3 install -e .

### Run
* python3 main.py (To test manually the snake game)
* python3 q_agent.py (To test the q agent)

## NEAT

### Path
* SnakeNEAT
  * game.py
  * neat_config.txt
  * neatAgent.py
  * snake.py
  * square.py
  * data/
    * config.json
    * dataUtils.py

### Dependencies
* pip3 install neat-python

### Run
* python3 neatAgent.py (To test the NEAT agent)

## Greedy

### Path
* SnakeG
  * game.py
  * main.py
  * snake.py
  * square.py
  * data/
    * config.json
    * dataUtils.py

### Dependencies
* no additional dependencies

### Run
* python3 main.py (To test the Gready agent)

