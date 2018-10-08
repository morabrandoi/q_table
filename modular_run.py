import pygame
import random
from Classes import Board, Pellet, Bot, Finish



show_board = False
FPS = 5
total_iterations = 100
initial_randomness = 1.0
randomness_decay = initial_randomness / (total_iterations - 2)
gamma = .9


bot = Bot(start_loc=(0,0))

finish = Finish()

nugget = Pellet()
actors = [bot, finish, nugget]

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
