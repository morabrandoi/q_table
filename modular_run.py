import pygame
import random
from Classes import Board, Pellet, Bot, Finish


bot = Bot(start_loc=(0,0))

finish = Finish()

actors = [bot, finish]

dimension = 12
display_size = 600

board = Board(dimension, display_size)
board.set_actors(actors)

pygame.init()

for i in range(5):
    print(i)
    board.run_episode()
    board.reset_board()
