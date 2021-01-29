# Snake Game AI
Projet pour le cours CSI4506 de l'Université d'Ottawa. Ce projet est une expérimentation sur l'éfficacité du "Q Learning", "NEAT Learning" et l'approche "Greedy" pour la conception d'un IA capable de jouer le jeu: Snake de façon efficace.

* [Conception du projet](https://github.com/jstpi047/AI-Game-Snake/blob/master/doc/CSI4506-Projet-Etape2-DefinitionProjet-SnakeAI.pdf)
* [Présentation du projet](https://github.com/jstpi047/AI-Game-Snake/blob/master/doc/CSI4506-Projet-Presentation.pdf)
* [Rapport du projet](https://github.com/jstpi047/AI-Game-Snake/blob/master/doc/CSI4506-Projet-Etape3.pdf)

## Dépendance
```
> pip3 install pygame
```
(pour système Ubuntu)
```
> sudo apt-get install python3-dev
```

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

### Dépendance
```
> pip3 install gym
> pip3 install numpy
> cd snakeQ/gym_foo pip3 install -e .
```

### Execution
-> test du jeu
```
> python3 ./snakeQ/gym-foo/gym_foo/envs/main.py
```

-> test l'agent
```
> python3 ./snakeQ/gym-foo/gym_foo/envs/q_agent.py
```

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

### Dépendance
```
> pip3 install neat-python
```

### Execution
-> test l'agent
```
> python3 ./snakeNEAT/neatAgent.py
```

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

### Dépendance
* pas de dépendance additionnel

### Execution
-> test l'agent
```
> python3 ./snakeG/main.py
```

## Membre du projet
* Jérémie St-Pierre
* Frédérik Laflèche
