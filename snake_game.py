import random
import time
import os
import pygame

pygame.mixer.init()
pygame.init()  # initializes all modules from pygame module

# setting program icon
programIcon = pygame.image.load(os.path.join('Assets', 'cartoon_snake.jpg'))
programIcon = pygame.transform.scale(programIcon, (30, 30))
pygame.display.set_icon(programIcon)

# setting screen size
screen_width = 550
screen_height = 600

# Creating window
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")
pygame.display.update()

# background title image
bgimg = pygame.image.load(os.path.join('Assets', 'bck_image.jpg'))
bgimg =pygame.transform.scale(bgimg, (screen_width,screen_height)).convert_alpha() # .convert alpha is for video mode

# game sounds
game_music = pygame.mixer.Sound('Assets/back_sound.mp3')
eat_music = pygame.mixer.Sound('Assets/ting_sound.mp3')
explode_music = pygame.mixer.Sound('Assets/explode_sound.mp3')

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 200, 0)
light_green = (144,238,144)


# clock bnyngy ta k is k time k hisab sy is game ka frame update kr skyn
clock = pygame.time.Clock()


def text_screen(text, color, x, y,f):  # x, y text ki location btayengy screen pr
    font = pygame.font.SysFont(None,
                               f)  # none lenay sy font style by default system wala hee ajyga, aur 55 font size hai
    screen_text = font.render(text, True,color)
    # in above render function,
    # antialias is set true to adjust high resolution object to low resolution object accord to screen
    gameWindow.blit(screen_text, [x,y]) # it will update the screen


# snake ki movement k coordinates plot krny ki liye following function
def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        # locating and kalay rang ka snake screen py dikhanay k liye
        # aur sath sath snk_list ki value brhtay hee increment lgta jyga
        # aur x,y coordinates add hotay jyngy
        # aur hr x,y coordinate py aik aik rectangle bnta jyga aur rec add hota jyga
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


# Welcome function
def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(white)
        gameWindow.blit(bgimg, (0, 0))
        text_screen("Welcome to Snakes", black, screen_width/3, screen_height/2.5, 35)
        pygame.draw.rect(gameWindow, green, [screen_width / 2.7, screen_height / 2.1, 150, 40])
        text_screen("Enter to Play", white, screen_width / 2.5, screen_height / 2, 25)
        pygame.draw.rect(gameWindow, red,[screen_width / 2.45, screen_height / 1.8, 90, 30 ] )
        text_screen("End", white, screen_width / 2.15, screen_height / 1.75, 20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_END:  # Esc key press krny py game quit hojygi
                    exit_game = True
                if event.key == pygame.K_RETURN: # Enter key press krny py game start hojygi
                    gameloop()
        pygame.display.update()
        clock.tick(30)


# Game's main function
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    initial_vel = 5
    food_x = random.randint(10, screen_width - 20)
    food_y = random.randint(50, screen_height - 20)
    score = 0
    snake_size = 8
    food_size = 6
    fps = 30  # fps = frame per sec
    # snake length brhanay k liye aik list variable define krdia
    snk_body = []  # empty snake list
    snk_length = 1

    game_music.play() # plays sound when you start playing
    # check if highscore file exists:
    if (not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f: # if not exits then this will create it
            f.write("0")
    # To read high score:
    with open("highscore.txt", "r") as f: # yeh game k main loop sy bahir isliye ta k srf sik baar read kry...
        highscore = f.read()
    # program k timer on krny k liye
    t1 = time.perf_counter()
    # Game ka main loop
    while not exit_game:

        # if game_over becomes True this will occur:
        if game_over:
            gameWindow.fill(light_green)
            text_screen("Game Over !", red, screen_width/2.5, screen_height/2.3, 30)
            pygame.draw.rect(gameWindow, green, [screen_width / 2.7, screen_height / 2.1, 190, 40])
            text_screen("Enter to Continue", white, screen_width / 2.5, screen_height / 2, 25)
            pygame.draw.rect(gameWindow, red, [screen_width / 2.45, screen_height / 1.8, 100, 30])
            text_screen("Esc to quit", white, screen_width / 2.4, screen_height / 1.75, 25)
            text_screen("Time Taken {} ".format(str(t1_stop))+" sec", red, 310, 8, 25)


            # Handling quit event of the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # agr game window k cross py click kryngy tou game close hojygi
                    exit_game = True

            # Handling key press events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # Enter key press krny py game phir sy start hojygi
                    welcome()

                if event.key == pygame.K_ESCAPE: # Esc key press krny py game quit hojygi
                    exit_game = True



        else:
            # timer lganay k liye
            t1_start = time.perf_counter()

            # follwng for loop condition to get any event on console which occurs on the screen e.g mouse move or any key press
            for event in pygame.event.get():

                # Handling key press events
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RIGHT: # agr right right arrow key press ki tou
                        velocity_x = + initial_vel # snake 10 pixel agay brh jyga along x-axis
                        velocity_y = 0 # jb jb x ko value milygi y ki 0 krni hogi ta k snake diagonal mai na move kry
                    if event.key == pygame.K_LEFT:
                        velocity_x = - initial_vel
                        velocity_y = 0 # jb jb x ko value milygi y ki 0 krni hogi ta k snake diagonal mai na move kry
                    if event.key == pygame.K_UP:
                        velocity_y = - initial_vel
                        velocity_x = 0 # jb jb y ko value milygi x ki 0 krni hogi ta k snake diagonal mai na move kry
                    if event.key == pygame.K_DOWN:
                        velocity_y = + initial_vel # jb jb y ko value milygi x ki 0 krni hogi ta k snake diagonal mai na move kry
                        velocity_x = 0 # is sy snake at a time srf aik direction mai move kryga jesay yahan srf downward y direction mai


                # Handling quit event of the game
                if event.type == pygame.QUIT:
                    exit_game = True

            # snake ko chalatay rehnay k liye aur snake k x,y update krnay k liye
            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            # food and snake ki location distinct rkhny k liye ta k food snake ki location pr hee na bn jaye
            # agr food aur snake k apas ka fasla 8 pixel sy km reh jaye tou score brhyga aur food ki new location ajygi
            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                score += 10  # aur jesay hee snake food k paas aye mtlb khata jaye tou score brhta jyga
                # for reappearance of food at new location  after snake has eaten
                food_x = random.randint(10, screen_width - 20) # new x value for location of food
                food_y = random.randint(50, screen_height - 20)  # new y value for location of food
                # food khanay k baad snake ki length brhanay k liye
                snk_length += 4
                eat_music.play()    # plays sound when snake eats


            # while screen bnanay k liye
            gameWindow.fill(light_green) # asigning color to screen
            # Score screen py dikhanay k liye
            text_screen("Score " + str(score), black, 5, 5, 20)

            # high score likhnay k liye
            if int(highscore) < score:
                highscore = score
            with open("highscore.txt" , "w") as f:
                    f.write(str(highscore))
            text_screen("High Score " + str(highscore), black, 130, 5,20)

            t1_round1 = round(t1_start - t1, 2)
            text_screen("Time " + str(t1_round1), black, 350, 5, 20) # to show timer on screen
            t1_stop = t1_round1
            # food screen py dikhanay k liye
            pygame.draw.circle(gameWindow, red, [food_x, food_y] , food_size)

            # snake head: screen py dikhanay k liye
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_body.append(head)
            plot_snake(gameWindow, black, snk_body, snake_size) # snake ki length brhygi

            # to control snake length
            if len(snk_body) > snk_length:
                del snk_body[0]

            # agr snake ka head apni hee body sy takraye tb bh game over hojaye
            if head in snk_body[0:-1]:
                game_over = True
                explode_music.play()  # plays sound when snake dies

            # to keep snake within screen
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                explode_music.play()  # plays sound when snake dies


        # For screen update
        pygame.display.update() # if any change is applied then this sttmnt necsry
        clock.tick(fps) # yeh aik sec mai utni baar upr wala frame update kr dyga jitna fps set kiya hy


    pygame.quit()
    quit()

welcome()

