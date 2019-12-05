from game import Game
import threading

def main():
    game = Game()
    x = threading.Thread(target=game.start)
    x.start()
    x.join()
    x = threading.Thread(target=game.start)
    x.start()
    x.join()
    x = threading.Thread(target=game.start)
    x.start()

main()
