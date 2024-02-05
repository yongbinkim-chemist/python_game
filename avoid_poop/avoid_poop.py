import pygame
import random

def add_enemy(n):
    n_enemy = n
    enemies = [pygame.image.load("./poop.png") for _ in range(n_enemy)]
    enemy_size = enemies[0].get_rect().size
    enemy_width = enemy_size[0]
    enemy_x_pos = [random.randint(0, screen_width) for _ in range(n_enemy)]
    enemy_x_pos = [x if x <= screen_width-enemy_width else screen_width-enemy_width for x in enemy_x_pos]
    enemy_y_pos = [0 for _ in range(n_enemy)]
    enemy_speed = [random.randint(1,5)/15 for _ in range(n_enemy)]
    return enemies, enemy_x_pos, enemy_y_pos, enemy_speed, enemy_width

# ESSENTIAL: pygame initialization
pygame.init()

# set screen size
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

# set screen title
pygame.display.set_caption("Orange County Kyle")

# FPS
clock = pygame.time.Clock()

# character image
character = pygame.image.load("./hero.png")
# character can move
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width // 2 - character_width // 2 # center of the screen
character_y_pos = screen_height - character_height
character_speed = 0.6

# destination coordinates
to_x = 0
to_y = 0

# enemy character
enemies, enemy_x_pos, enemy_y_pos, enemy_speed, enemy_width = add_enemy(1)

# font
game_font = pygame.font.Font(None, 30) # font instance (font, size)

# start time
total_time = 90
start_time = pygame.time.get_ticks() # start time, unit: ms

# Event loop
running = True
n_avoid = 0
pygame.time.delay(8000) # unit ms -> 2000ms = 2s
while running:
    dt = clock.tick(30) # frame per second (FPS)
    # print(f"FPS: {clock.get_fps()}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # when click 'x' button
            running = False

        if event.type == pygame.KEYDOWN: # when press key
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed

        if event.type == pygame.KEYUP: # when unpress stop moving
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0

    character_x_pos += to_x * dt
    # x boundary condition
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width # think about how pygame draw image
    
    enemy_y_pos = [enemy_speed[i]*dt + y for i,y in enumerate(enemy_y_pos)]
    # enemy boundary condition
    for i,y in enumerate(enemy_y_pos):
        if y > screen_height:
            new_x = random.randint(0, screen_width)
            enemy_x_pos[i] = new_x if new_x <= screen_width-enemy_width else screen_width-enemy_width
            enemy_y_pos[i] = 0
            enemy_speed[i] = random.randint(1,5)/15
            n_avoid += 1

    # collision process
    # character coordinate update
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for i,enemy in enumerate(enemies):
        enemy_rect = enemy.get_rect()
        enemy_rect.left = enemy_x_pos[i]
        enemy_rect.top = enemy_y_pos[i]
        if character_rect.colliderect(enemy_rect):
            game_over_font = pygame.font.Font(None, 60) # font instance (font, size)
            game_over = game_over_font.render("GAME OVER", True, (255,0,0))
            screen.blit(game_over, (120,310)) 
            pygame.display.update() # background image while loop
            pygame.time.delay(2000) # unit ms -> 500ms = 0.5s
            running = False

    screen.fill((255,255,255)) # background color (RGB)
    screen.blit(character, (character_x_pos,character_y_pos)) 
    for i, enemy in enumerate(enemies):
        screen.blit(enemy, (enemy_x_pos[i],enemy_y_pos[i])) 

    # put timer
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000 # ms -> s
    timer = game_font.render("Timer: " + str(int(elapsed_time)) +'/'+ str(total_time), True, (255,0,0))
    score = game_font.render("Number Avoided: " + str(n_avoid), True, (0,0,255))
    screen.blit(timer, (10,10)) 
    screen.blit(score, (10,40)) 
    
    # increase difficulty
    if elapsed_time > 1 and elapsed_time % 5 <= 0.05:
        n_enemies, n_enemy_x_pos, n_enemy_y_pos, n_enemy_speed, _ = add_enemy(1)
        enemies.extend(n_enemies)
        enemy_x_pos.extend(n_enemy_x_pos)
        enemy_y_pos.extend(n_enemy_y_pos)
        enemy_speed.extend(n_enemy_speed)

    if total_time-elapsed_time <= 0:
        game_over_font = pygame.font.Font(None, 60) # font instance (font, size)
        game_over = game_over_font.render("CLEAR!", True, (255,0,0))
        screen.blit(game_over, (170,310)) 
        pygame.display.update() # background image while loop
        pygame.time.delay(2000) # unit ms -> 500ms = 0.5s
        running = False
    
    pygame.display.update() # background image while loop

pygame.quit()
