import pygame
import random
from Classes import Board, Pellet, Bot, Finish



show_board = False

bot = Bot(start_loc=(0,0))

finish = Finish()

actors = [bot, finish]

dimension = 20
display_size = 600

board = Board(dimension, display_size)
board.set_actors(actors)

pygame.init()

for i in range(45):
    print(i)
    print(board.randomness)
    if i >= 43:
        show_board = True
    board.run_episode(show=show_board)
    board.reset_board()
