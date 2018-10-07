import random
import pygame

# fix q-table structure so direction correspondss to an index of the list as the value
# fix decesion process
# create update q_table method

class Board:
    def __init__(self, dimension, display_size):
        self.dimension = dimension
        self.display_size = display_size
        self.tile_size = self.display_size // self.dimension
        self.tile_location_coord = range(0, self.display_size, self.tile_size)
        self.game_display = pygame.display.set_mode((self.display_size, self.display_size))
        self.clock = pygame.time.Clock()
        self.actors = None
        self.bot = None
        self.randomness = 90
        self.delta_random = 0.9
        self.finish = None
        self.pellets = None
        self.pair_history = []
        self.q_table = {}


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

        dir = actor.decide_move(self, q_table=self.q_table, state=self.get_state())



        if random.random() < self.randomness:
            dir = random.choice(["left", "right", "stay", "up", "down"])
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
        else:
            return "stay"


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


    def add_history(self, action):
        state = self.get_state()
        self.pair_history.append((state, action))


    def display_board(self, actors):
        self.game_display.fill((255,255,255))
        for actor in self.actors:
            pygame.draw.rect(self.game_display, actor.get_color(), actor.get_rect())
        pygame.display.update()
        self.clock.tick(60)


    def update_table(self, reward):
        local_reward = reward
        self.pair_history.reverse()
        for pair in self.pair_history:

            state = pair[0]
            action = pair[1]
            reward *= 0.9
            self.q_table[state][action] += reward


    def reset_board(self):
        for actor in self.actors:
            actor.x = actor.start_x
            actor.y = actor.start_y
        self.pair_history = []
        self.randomness *= self.delta_random



    def run_episode(self):
        game_exit = False
        total_reward = 0
        print(self.randomness)
        
        while not game_exit:
            total_reward -= 1

                # confirm move
            dir = self.confirm_move(self.bot)

            if self.is_collided(self.bot, self.finish):
                game_exit = True
                total_reward += 10000
            else:
                self.add_history(dir)

            self.display_board(self.actors)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
        self.update_table(total_reward)


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

    def decide_move(self, board, q_table=None, state=None):
        state = tuple(state)
        if state not in q_table:
            q_table[state] = {"left": 0,
                              "right": 0,
                              "down": 0,
                              "up": 0,
                              "stay": 0}
            board.q_table = q_table
            return random.choice(["left", "right", "up", "down", "stay"])
        else:
            largestVal = max(list(q_table[state].values()))
            highest_directions = []
            for key in list(q_table[state].keys()):
                if q_table[state][key] == largestVal:
                    highest_directions.append(key)

            if len(highest_directions) == 1:
                return highest_directions[0]
            else:

                return random.choice(highest_directions)


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
