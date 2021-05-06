import random
from constants import *

class game:
    def __init__(self):
        self.ball_y = WINDOW_HEIGHT - BALL_RADIUS # y position of ball
        self.ball_x = BALL_X_POS # x position of ball
        self.y_change = 0 # change in y of the ball
        self.score = 0 # score of the game
        self.obstacles = [] # list of obstacles
        self.is_over = False # is the game over
        self.jumped = False # represents whether the ball was jumped
        self.in_air = False # represents whether the ball is in the air
        self.current_obstacle = 0 # represents index of current obstacle
        self.generation = 0 # generation of networks
        self.top_score = 0 # top score of all networks

    def get_top_score(self):
        return self.top_score

    def set_top_score(self, networks):
        '''
        Updates top score based on hit networks from previous generation
        '''
        new_score = networks[0]['score']
        if new_score > self.top_score:
            self.top_score = new_score

    def get_generation(self):
        return self.generation

    def increment_generation(self):
        '''
        Increments self.generation by one
        '''
        self.generation += 1
    
    def move_ball(self):
        ''' Moves ball vertically according to gravity by changing ball_y
            field.
        '''
        # ball on the floor and in_air is True  
        if self.in_air and self.ball_y >= WINDOW_HEIGHT - (BALL_RADIUS * 2):
            self.jumped = False 
            self.in_air = False
            self.y_change = 0
        # ball on the floor and jumped is True
        elif self.ball_y >= WINDOW_HEIGHT - (BALL_RADIUS * 2) and self.jumped:
            self.ball_y += self.y_change
            self.y_change += GRAVITY
            self.in_air = True
        elif self.ball_y >= WINDOW_HEIGHT - (BALL_RADIUS * 2) and not self.jumped:
            self.y_change = 0
        else:
            self.ball_y += self.y_change
            self.y_change += GRAVITY
        
    def jump_ball(self):
        ''' Makes the ball jump up by changing y_change
        '''
        # only jump if y_change is zero
        if not self.jumped:
            self.y_change -= 25
            self.jumped = True
            
    def generate_obstacle(self):
        ''' Generates an obstacle to be added to self.obstacles
            with random heights within a range
        '''
        height = random.randint(HEIGHT_MIN, HEIGHT_MAX)
        o = obstacle(height, OBSTACLE_WIDTH)
        self.obstacles.append(o)

    def clear_obstacles(self):
        self.obstacles = []
    
    def move_obstacles(self):
        '''
        Moves every obstacle across the screen
        '''
        for obs in self.obstacles:
            obs.x_loc -= OBSTACLE_X_CHANGE
    
    def is_collision(self, obstacles):
        '''
        Checks if a collision occured between ball and current obstacle
        '''
        # confirm that obstacle is created
        if len(obstacles) > self.current_obstacle:
            current_obs = obstacles[self.current_obstacle]
            # True if right wall of ball is past left wall of obstacle
            passed_left_wall = (self.ball_x + BALL_RADIUS) >= current_obs.x_loc
            # True if bottom of ball is below the wall height
            below_wall_height = (self.ball_y + BALL_RADIUS) >= (WINDOW_HEIGHT - current_obs.height)
            # True if left wall of ball is not passed right wall of obstacle
            not_passed_right_wall = (self.ball_x - BALL_RADIUS) <= current_obs.x_loc + current_obs.width

            if passed_left_wall and below_wall_height and not_passed_right_wall:
                print('hit')
                #self.is_over = True
                return True
            elif not not_passed_right_wall:
                self.current_obstacle += 1
                self.score += 1
                return False

    def get_inputs(self, obstacles):
        if len(obstacles) > self.current_obstacle:
            current_obs = obstacles[self.current_obstacle]
            x_obstacle = current_obs.x_loc # x location of current obstacle
            height_obstacle = current_obs.height

            return x_obstacle - self.ball_x, height_obstacle
        else:
            return None

class obstacle:
    def __init__(self, height, width):
        self.x_loc = INIT_X_LOC 
        self.height = height
        self.width = width