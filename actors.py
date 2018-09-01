import random
class Pellet:
    def __init__(self, size, start_loc):
        self.x = start_loc[0]
        self.y = start_loc[1]
        self.size = size

    def get_location(self):
        return (self.x, self.y)

    def get_rect(self):
        return (self.x, self.y, self.size, self.size)

class Bot:
    def __init__(self, size, start_loc):
        self.x = start_loc[0]
        self.y = start_loc[1]
        self.size = size

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

    def get_rect(self):
        return (self.x, self.y, self.size, self.size)


class Player:
    def __init__(self, size, start_loc):
        self.x = start_loc[0]
        self.y = start_loc[1]
        self.size = size


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

    def get_rect(self):
        return (self.x, self.y, self.size, self.size)

class Finish:
    def __init__(self, size, start_loc):
        self.x = start_loc[0]
        self.y = start_loc[1]
        self.size = size

    def get_location(self):
        return (self.x, self.y)

    def get_rect(self):
        return (self.x, self.y, self.size, self.size)

class Randos:
    def __init__(self, size, start_loc):
        self.x = start_loc[0]
        self.y = start_loc[1]
        self.size = size

    def get_location(self):
        return (self.x, self.y)

    def get_rect(self):
        return (self.x, self.y, self.size, self.size)

    def move(self, dir):
        if dir == "up":
            self.y -= self.size
        elif dir == "down":
            self.y += self.size
        elif dir == "right":
            self.x += self.size
        elif dir == "left":
            self.x -= self.size
