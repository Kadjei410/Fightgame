import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

# create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000


#Player 1 and 2 are called warrior and huntress but can be named anything

#define fighter variables.
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [70, 55]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
HUNTRESS_SIZE = 150
HUNTRESS_SCALE = 4
HUNTRESS_OFFSET = [58, 51]
HUNTRESS_DATA = [HUNTRESS_SIZE, HUNTRESS_SCALE, HUNTRESS_OFFSET]

#load music and sounds
sword_fx1 = pygame.mixer.Sound(r"C:\Users\Kwame\Music\Sound Effects\mixkit-swift-sword-strike-2166.wav")
sword_fx1.set_volume(0.5)
sword_fx2 = pygame.mixer.Sound(r"C:\Users\Kwame\Music\Sound Effects\mixkit-sword-slash-swoosh-1476.mp3")
sword_fx2.set_volume(0.5)
pygame.mixer.music.set_volume(0.5)

#load background image
bg_image = pygame.image.load(
    r"C:\Users\Kwame\PycharmProjects\Fightgame\venv\Images\fightgamebackground.jpg").convert_alpha()

#load spritesheets
huntress_sheet = pygame.image.load(
    r"C:\Users\Kwame\PycharmProjects\Fightgame\venv\Images\Huntress\Huntress\Sprites\huntress.png").convert_alpha()
warrior_sheet = pygame.image.load(
    r"C:\Users\Kwame\PycharmProjects\Fightgame\venv\Images\Fantasy Warrior\Fantasy Warrior\Sprites\warrior.png").convert_alpha()

#Load victory image
victory_img = pygame.image.load(r"C:\Users\Kwame\PycharmProjects\Fightgame\venv\Images\victory.png").convert_alpha()

# define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [9, 7, 7, 7, 8, 8, 10]
HUNTRESS_ANIMATION_STEPS = [8, 2, 8, 3, 2, 8, 5, 5, 8]

#define font
count_font = pygame.font.SysFont('Verdana', 60)
score_font = pygame.font.SysFont('Verdana', 60)

#function for drawing text
def draw_text(text, font, text_col, x , y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))


# function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


# create two instances of fighters
fighter_1 = Fighter(1, 200, 360, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx1)
fighter_2 = Fighter(2, 700, 360, True, HUNTRESS_DATA, huntress_sheet, HUNTRESS_ANIMATION_STEPS, sword_fx2)

# game loop
run = True
while run:

    clock.tick(FPS)

    # draw background
    draw_bg()

    # show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

    #update countdown
    if intro_count <= 0:
        #move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        #display count timer
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        #update count timer
        if(pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
            print(intro_count)

    # update fighters
    fighter_1.update()
    fighter_2.update()

    #draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    #check for player defeat
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
            print(score)

        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
            print(score)

    else:
        screen.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1, 200, 360, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx1)
            fighter_2 = Fighter(2, 700, 360, True, HUNTRESS_DATA, huntress_sheet, HUNTRESS_ANIMATION_STEPS, sword_fx2)


    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display
    pygame.display.update()

# exit pygame
pygame.quit()
