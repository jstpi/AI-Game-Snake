from game import Game
import threading
import os
import neat



def eval_genomes(genomes, config):


    for genome_id, genome in genomes:
        winnerSize = 0
        genome.fitness = 0
        #instantiation of the neat neural network
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        #thread creation for the play of the game
        x = threading.Thread(target=game.start(net, genome))
        x.start()
        #if statment to keep track of biggest snake through iterations
        if(game.size>winnerSize):
            winnerSize = game.size
        print("Fitness: ", genome.fitness)
        x.join()
    print("Longest snake length: ", winnerSize)

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet, neat.DefaultStagnation,config_file)
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)


    # Run for up to 40 generations.
    winner = p.run(eval_genomes, 40)

if __name__ == '__main__':
    #main()
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat_config.txt')
    #new game
    game = Game()
    run(config_path)
