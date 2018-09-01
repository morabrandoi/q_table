import pygame
import random
from actors import Player, Finish, Randos, Bot


def move_block(actor, dir=None, dict=None):
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


for _ in range(4):
    pygame.init()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # display parameters
    display_size = 700
    grid_tile_length = 12 # random.randint(10, 14)

    # THE GAME SCREEN ITSELF
    game_display = pygame.display.set_mode((display_size, display_size))
    pygame.display.set_caption("GAME TIME")
    clock = pygame.time.Clock()

    # defining stage variables
    tile_size = display_size // grid_tile_length
    tile_location_coord = [iter * tile_size for iter in range(grid_tile_length)]




    game_exit = False

    user = Player(tile_size, (0, 0))
    goal = Finish(tile_size, (tile_location_coord[-1], tile_location_coord[-1]))
    rando1 = Randos(tile_size, (tile_location_coord[3],
                                tile_location_coord[3]))
    rando2 = Randos(tile_size, (tile_location_coord[5],
                                tile_location_coord[5]))
    rando3 = Randos(tile_size, (tile_location_coord[7],
                                tile_location_coord[7]))
    rando4 = Randos(tile_size, (tile_location_coord[9],
                                tile_location_coord[9]))
    rando5 = Randos(tile_size, (tile_location_coord[-1],
                                tile_location_coord[-2]))
    rando6 = Randos(tile_size, (random.choice(tile_location_coord[1:-2]),
                               random.choice(tile_location_coord[1:-2])))

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            elif event.type == pygame.KEYDOWN:
                move_block(rando1)
                move_block(rando2)
                move_block(rando3)
                move_block(rando4)
                move_block(rando5)
                move_block(rando6)

                if event.key == pygame.K_LEFT:
                    move_block(user, "left")
                elif event.key == pygame.K_RIGHT:
                    move_block(user, "right")
                elif event.key == pygame.K_UP:
                    move_block(user, "up")
                elif event.key == pygame.K_DOWN:
                    move_block(user, "down")


            if is_collision(user, goal):
                game_exit = True



            if is_collision(user, [rando1, rando2, rando3, rando4, rando5, rando6]):
                game_exit = True


            if event.type == pygame.KEYUP:
                pass

        game_display.fill(WHITE)
        pygame.draw.rect(game_display, BLUE, user.get_rect())
        pygame.draw.rect(game_display, GREEN, goal.get_rect())
        pygame.draw.rect(game_display, RED, rando1.get_rect())
        pygame.draw.rect(game_display, RED, rando2.get_rect())
        pygame.draw.rect(game_display, RED, rando3.get_rect())
        pygame.draw.rect(game_display, RED, rando4.get_rect())
        pygame.draw.rect(game_display, RED, rando5.get_rect())
        pygame.display.update()
        clock.tick(60)







    pygame.quit()

quit()
