import pygame
from constants import *
import neural_network


'''
This file contains functions for displaying the visuals of the game.
'''

my_network = neural_network.network_object()


'''
Initializes the view of the game
'''
pygame.init()
LETTER_FONT = pygame.font.SysFont('comicsans', 30)
# initialize window
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
win.fill(BLACK) # sets black background
pygame.display.set_caption('Bouncing Ball Game')
pygame.display.update() # updates display

clock = pygame.time.Clock() # creates game clock

def draw_information():
    '''
    Draws the game information next to the game animation
    '''
    generation_text = LETTER_FONT.render(f'Generation: {my_network.game_object.get_generation()}', 1, WHITE)
    high_score_text = LETTER_FONT.render(f'High Score: {my_network.game_object.get_top_score()}', 1, WHITE)
    win.blit(generation_text, (20, 20))
    win.blit(high_score_text, (20, 40))

def draw_ball():
    '''
    Draws the ball on the screen
    '''
    win.fill(BLACK)
    for n in my_network.networks:
        x = n.get_ball_x()
        y = n.get_ball_y()
        pygame.draw.circle(win, BALL_COLOR, (x, y), BALL_RADIUS, 0)

def draw_obstacles():
    ''' 
    #Draws the obstacles on the screen
    '''
    obstacles = my_network.get_obstacles()

    for obs in obstacles:
        r = pygame.Rect(obs.x_loc, WINDOW_HEIGHT - obs.height, 20, obs.height)
        pygame.draw.rect(win, OBSTACLE_COLOR, r)

def draw_score():
    score = game_object.score # CHANGE
    text_score = LETTER_FONT.render(f'Score: {score}', 1, WHITE)
    win.blit(text_score, (20, 20))

def draw():
    draw_ball()
    draw_obstacles()
    draw_information()
    #draw_score()
    pygame.display.update()

def create_obstacle(frames):
    if frames % 1300 == 0:
        my_network.game_object.generate_obstacle()

frames = 0
is_quit = False

while not is_quit:
    # FPS
    clock.tick(FPS)
    frames += FPS
    
    create_obstacle(frames) # creates obstacle
    my_network.move_balls() # moves the ball
    my_network.move_obstacles() # moves all the obstacles across the screen
    my_network.is_collision(my_network.get_obstacles()) # checks for collision and changes is_over for every object that has collided
    # NOTE: the obstacles being drawn are the main object obstacles.
    # every network game must check for a collision with its own location and the main object's obstacles
    draw() # draws all game objects on the screen

    obs = my_network.get_obstacles()
    for network in my_network.networks:
        inp = network.get_inputs(obs)

        if inp is not None:
            guess = network.guess(inp[0], inp[1])

            if guess >= 0.5:
                network.jump_ball()
    # handles generating new networks
    # if generation is over (networks list is empty)
    if len(my_network.networks) == 0:
        print('generation over')
        #for network in my_network.hit_networks:
            #print(f'Score: {network.get_score()}')
            #print(f'Weights: {network.sny0}')
        # create a test new network
        # score should be 0
        # should not immediately die in obstacle (current obs should be set to next)
        my_network.mutate_networks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_quit = True
