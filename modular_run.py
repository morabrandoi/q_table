import pygame
import random
from Classes import Board, Pellet, Bot, Finish



show_board = False
FPS = 10
total_iterations = 300
initial_randomness = 1.0
randomness_decay = initial_randomness / (total_iterations - 2)
gamma = .999999
how_many_pellets = 20




bot = Bot(start_loc=(0,0))

finish = Finish()

actors = [bot, finish]
for _ in range(how_many_pellets):
    actors.append(Pellet())

dimension = 20
display_size = 600


board = Board(dimension, display_size, initial_randomness, randomness_decay, gamma=gamma, FPS=FPS)
board.set_actors(actors)

pygame.init()
pygame.display.set_caption("TIMBERLEE'S Journey")

for i in range(total_iterations):
    print(i)
    print(board.randomness)
    if i >= total_iterations - 2:
        show_board = True
    board.run_episode(show=show_board)
    board.reset_board()
