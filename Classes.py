import random
import pygame



class Board:
    def __init__(self, dimension, display_size, randomness=0.9, delta_random=0.45, gamma=0.9, FPS=3):
        self.dimension = dimension
        self.display_size = display_size
        self.tile_size = self.display_size // self.dimension
        self.tile_location_coord = range(0, self.display_size, self.tile_size)
        self.game_display = pygame.display.set_mode((self.display_size, self.display_size))
        self.clock = pygame.time.Clock()
        self.FPS = FPS
        self.actors = None
        self.bot = None
        self.gamma = gamma
        self.randomness = randomness
        self.delta_random = delta_random
        self.finish = None
        self.pellets = None
        self.pair_history = []
        self.value_table = {}


    def set_actors(self, actors):
        self.actors = actors
        for actor in self.actors:
            actor.set_size(self.tile_size)
            if type(actor) is Finish:
                self.finish = actor
                start_x = self.tile_location_coord[-1]
                start_y = self.tile_location_coord[-1]
                self.finish.set_location((start_x, start_y))
                self.finish.start_x = start_x
                self.finish.start_y = start_y
            if type(actor)is Bot:
                self.bot = actor
            if type(actor) is Pellet:
                self.destructables.append(actor)


    def confirm_move(self, actor):

        dir = actor.decide_move(self, value_table=self.value_table, state=self.get_state())
        if random.random() < self.randomness:
            dir = random.choice(["left", "right", "up", "down"])
        if dir == "right" and (actor.x + self.tile_size <= self.tile_location_coord[-1]):
            actor.move(dir)
            return dir
        elif dir == "down" and (actor.y + self.tile_size <= self.tile_location_coord[-1]):
            actor.move(dir)
            return dir
        elif dir == "up" and (actor.y > 0):
            actor.move(dir)
            return dir
        elif dir == "left" and (actor.x > 0):
            actor.move(dir)
            return dir



    def is_collided(self, actor1, actor2):
        if actor1.get_location() == actor2.get_location():
            return True
        else:
            return False


    def get_state(self):
        state = []
        for actor in self.actors:
            state.append(actor.get_location())
        return tuple(state)


    def add_history(self, immediate_reward):
        state = self.get_state()
        self.pair_history.append((state, immediate_reward))


    def display_board(self, actors):
        self.game_display.fill((255,255,255))
        for actor in self.actors:
            pygame.draw.rect(self.game_display, actor.get_color(), actor.get_rect())
        pygame.display.update()
        self.clock.tick(self.FPS)




    def update_value_table(self, total_reward):

        prev_value = 0
        for pair in self.pair_history:
            state = pair[0]

            immediate_reward = pair[1]
            self.value_table[state] = max(immediate_reward + (self.gamma * prev_value), self.value_table[state])
            prev_value = self.value_table[state]


    def reset_board(self):
        for actor in self.actors:
            actor.x = actor.start_x
            actor.y = actor.start_y
        self.pair_history = []
        self.randomness -= self.delta_random



    def run_episode(self, show=True):
        game_exit = False
        final_reward = 0


        while not game_exit:
            prev_reward = final_reward
            final_reward -= 1
                # confirm move
            self.confirm_move(self.bot)

            if self.is_collided(self.bot, self.finish):
                game_exit = True
                final_reward += 10000

            immediate_reward = final_reward - prev_reward

            self.add_history(immediate_reward)




            if show:
                self.display_board(self.actors)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True


        self.pair_history.reverse()
        self.update_value_table(final_reward)

class Generic_Block:
    def __init__(self, start_loc=(-1,-1), color=(255,255,255)):
        self.start_x = start_loc[0]
        self.start_y = start_loc[1]
        self.x = start_loc[0]
        self.y = start_loc[1]
        self.size = 0
        self.color = color

    def get_rect(self):
        return (self.x, self.y, self.size, self.size)


    def get_color(self):
        return self.color

    def decide_move(self):
        return random.choice(["left", "up", "right", "down"])

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

    def set_location(self, loc):
        self.x = loc[0]
        self.y = loc[1]

    def set_size(self, size):
        self.size = size


class Bot(Generic_Block):
    def __init__(self, start_loc=(-1,-1)):
        super().__init__(start_loc, (0,0,255))

    def decide_move(self, board, value_table=None, state=None):

        directional_values = {}

        if self.x + board.tile_size <= board.tile_location_coord[-1]:
            self.move("right")
            state = board.get_state()
            if state not in board.value_table.keys():
                board.value_table[state] = 0
                directional_values["right"] = 0
            else:
                directional_values["right"] = board.value_table[state]
            self.move("left")

        if self.y + board.tile_size <= board.tile_location_coord[-1]:
            self.move("down")
            state = board.get_state()
            if state not in board.value_table.keys():
                board.value_table[state] = 0
                directional_values["down"] = 0
            else:
                directional_values["down"] = board.value_table[state]
            self.move("up")

        if self.y > 0:
            self.move("up")
            state = board.get_state()
            if state not in board.value_table.keys():
                board.value_table[state] = 0
                directional_values["up"] = 0
            else:
                directional_values["up"] = board.value_table[state]
            self.move("down")

        if self.x > 0:
            self.move("left")
            state = board.get_state()
            if state not in board.value_table.keys():
                board.value_table[state] = 0
                directional_values["left"] = 0
            else:
                directional_values["left"] = board.value_table[state]
            self.move("right")

        max_directional_value = max(list(directional_values.values()))
        list_of_highest_value_dir = [x for x in list(directional_values.keys()) if directional_values[x] == max_directional_value]
        return random.choice(list_of_highest_value_dir)


class Pellet(Generic_Block):
    def __init__(self, start_loc=(-1,-1)):
        super().__init__(start_loc, (255,255,0))


class Player(Generic_Block):
    def __init__(self, start_loc=(-1,-1)):
        super().__init__(start_loc, (0,0,255))


class Finish(Generic_Block):
    def __init__(self, start_loc=(-1,-1)):
        super().__init__(start_loc, (0,255,0))


class Rando(Generic_Block):
    def __init__(self, start_loc=(-1,-1)):
        super().__init__(start_loc, (255,0,0))
