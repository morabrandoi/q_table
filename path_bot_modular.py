import pygame
import random
import simpleaudio as sa
from actors import Player, Finish, Bot, Pellet


def move_block(actor, dir=None, dict=None, iter=0):
    if dir == "right" and (actor.x + tile_size <= tile_location_coord[-1]):
        actor.move(dir)
    elif dir == "down" and (actor.y + tile_size <= tile_location_coord[-1]):
        actor.move(dir)
    elif dir == "up" and (actor.y > 0):
        actor.move(dir)
    elif dir == "left" and (actor.x > 0):
        actor.move(dir)
    elif dir == None and type(actor) == Randos:
        dir = random.choice(["left", "right", "up", "down", "stay"])
        move_block(actor, dir)
    elif dir == None and type(actor) == Bot:
        state = get_state()


        new_dir, new_dict = actor.get_dir(dict, state[0])
        # randomness
        if random.random() <= initial_randomness * (1 - (iter / total_iterations)):
            new_dir = random.choice(["left", "right", "up", "down"])

        state_dir_pair = get_state()
        dir_index = ["left", "up", "right", "down"].index(new_dir)
        state_dir_pair.append(dir_index)
        state_dir_pair.append(dir_index)
        state_dir_pair = tuple(state_dir_pair)
        pair_history.append(state_dir_pair)

        move_block(actor, new_dir)

        return new_dict

def is_collision(actor1, actor2):
    if type(actor2) == type([]):
        for act in actor2:
            if actor1.get_location() == act.get_location():
                return True
        return False
    else:
        if actor1.get_location() == actor2.get_location():
            return True
        else:
            return False

def get_state():
    return [user.get_location()]



def update_dict(q_dict, pair_history, total_reward):
    # pair_history.reverse()
    for pair in pair_history:
        state = pair[0]
        dir = pair[1]
        reward = pair[2]
        (q_dict[state])[dir] = (q_dict[state])[dir] + (LR * total_reward)




iteration = 0
total_iterations = 20
q_dict = {}
FPS = 120
initial_randomness = 0.8
#learning rate
LR = 0.5
# Discount rate
DR = 0.9


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)

# display parameters
display_size = 600
grid_tile_length = 12 # random.randint(10, 14)

# defining stage variables
tile_size = display_size // grid_tile_length
tile_location_coord = [iter * tile_size for iter in range(grid_tile_length)]

pellet_loc = (random.choice(tile_location_coord[-2:-1]), random.choice(tile_location_coord[0:1]))


for i in range(total_iterations):
    print("iteration", iteration, "random to ", initial_randomness * (1 - (iteration / total_iterations)))
    if i > total_iterations - 2:
        wave_obj = sa.WaveObject.from_wave_file("ding1.wav")
        play_obj = wave_obj.play()
        play_obj.wait_done()
        FPS = 4
    pair_history = []

    pygame.init()





    # THE GAME SCREEN ITSELF
    game_display = pygame.display.set_mode((display_size, display_size))
    pygame.display.set_caption("Timberlee's Journey")
    clock = pygame.time.Clock()






    game_exit = False

    user = Bot(tile_size, (0, 0))
    goal = Finish(tile_size, (tile_location_coord[-1], tile_location_coord[-1]))
    pellet1 = Pellet(tile_size, pellet_loc)

    destructables = [pellet1]


    while not game_exit:
        total_reward = 0

        new_q_dict = move_block(user, dict=q_dict, iter=iteration)
        q_dict = new_q_dict

        total_reward -= 1


        game_display.fill(WHITE)

        if is_collision(user, goal) and destructables == []:
            game_exit = True
            total_reward += 1000

        if is_collision(user, destructables):
            destructables.remove(pellet1)
            total_reward += 1000000
        elif destructables != []:
            pygame.draw.rect(game_display, YELLOW, pellet1.get_rect())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True




        pygame.draw.rect(game_display, BLUE, user.get_rect())
        pygame.draw.rect(game_display, GREEN, goal.get_rect())


        pygame.display.update()
        clock.tick(FPS)






    iteration += 1
    update_dict(q_dict, pair_history, total_reward)
    pygame.quit()


quit()
