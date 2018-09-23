import random
import pygame




class Board:
    def __init__(self, dimension, display_size, actors):
        self.dimension = dimension
        self.display_size = display_size
        self.tile_size = display_size // dimension
        self.tile_location_coord = range(0, display_size, tile_size)
        self.game_display = pygame.display.set_mode((display_size, display_size))
        self.clock = pygame.time.Clock()
        self.actors = actors
        self.q_dict = {}



    def display_board(self, actors):
        game_display.fill(WHITE)
        for actor in actors:
            pygame.draw.rect(game_display, actor.get_color(), actor.get_rect())
        pygame.display.update()

    def run_episode(self, actors):


        game_exit = False




class Generic_Block:
    def __init__(self, size, start_loc=(0,0), color=(255,255,255)):
        self.x = start_loc[0]
        self.y = start_loc[1]
        self.size = size
        self.color = color

    def get_rect(self):
        return (self.x, self.y, self.size, self.size)


    def get_color(self):
        return self.color


    def move(self, dir):
        if dir == "up":
            self.y -= self.size
        elif dir == "down":
            self.y += self.size
        elif dir == "right":
            self.x += self.size
        elif dir == "left":
            self.x -= self.size

    def get_location(self):
        return (self.x, self.y)



class Bot(Generic_Block):
    def __init__(self, size, start_loc):
        super().__init__(start_loc[0], start_loc[1], (0,0,255), size)


    def get_dir(self, q_dict, state):
        # state is location
        # value is reward for action in order of L, U, R, D

        state = tuple(state)
        if state not in q_dict.keys():
            q_dict[state] = [0,0,0,0]
        indices = [i for i, x in enumerate(q_dict[state]) if x == max(q_dict[state])]
        if len(indices) > 1:
            index = random.choice(indices)
        else:
            index = indices[0]

        return (["left", "up", "right", "down"][index], q_dict)


class Pellet(Generic_Block):
    def __init__(self, size, start_loc):
        super().__init__(start_loc[0], start_loc[1], (255,255,0), size)


class Player(Generic_Block):
    def __init__(self, size, start_loc):
        super().__init__(start_loc[0], start_loc[1], (0,0,255), size)


class Finish(Generic_Block):
    def __init__(self, size, start_loc):
        super().__init__(start_loc[0], start_loc[1], (0,255,0), size)


class Rando(Generic_Block):
    def __init__(self, size, start_loc):
        super().__init__(start_loc[0], start_loc[1], (255,0,0), size)
