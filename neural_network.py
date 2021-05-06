import numpy as np
import game
import random


'''
NOTES:
- line 21 and 119: make sure weights are being set in the new neural network object
- line 123: neural network has a score, and game object has a score. Make sure to 
            only use one field

'''
class network_object:
    def __init__(self):
        self.game_object = game.game() # lead game object for all neural networks
        self.networks = self.generate_networks() # list of neural networks
        self.hit_networks = []

    def generate_networks(self, weights = None):
        networks = []
        for i in range(6):
            game_object = game.game()
            if weights is not None:
                n = neural_network(game_object)
                n.set_weights(weights[i])
            else:
                n = neural_network(game_object)
            networks.append(n)
            print(n.sny0)
        '''
        networks = []
        game_object = game.game()
        n = neural_network(game_object)
        networks.append(n)
        '''

        return networks

    def test_create(self):
        # clear hit_networks
        self.hit_networks = []
        # create new network in networks
        print(f'Number of networks: {self.networks}')
        new_game = game.game()
        self.game_object.clear_obstacles()
        self.networks = self.generate_networks()


    # generates new neural networks with mutation
    # mutates self.networks field by assigning new list of networks to it
    def mutate_networks(self):
        # get top three networks

        # map hit_networks to list of dicts holding score and weights
        mapped_networks = map(lambda x: {'score': x.get_score(), 'weights': x.sny0}, 
        self.hit_networks)
        
        # sort networks in decreasing order by score
        sorted_networks = sorted(mapped_networks, key = lambda x: x['score'], reverse=True)
        print(f'sorted: {sorted_networks}')

        # update the top score in game object based on hit networks from previous generation
        self.game_object.set_top_score(sorted_networks)

        # NOTE: if there are three networks with scores greater than 0, then get top three,
        # otherwise, only get the ones with scores to creates new ones with. If all have 
        # a score of 0, create brand new random weights 
        top_networks = []
        for idx, element in enumerate(sorted_networks):
            if element['score'] > 0 and idx <=3:
                top_networks.append(element)
        
        # if all score 0, generate new random weights
        if len(top_networks) == 0:
            self.networks = self.generate_networks()
            #print(f'All 0: {self.networks}')
        else:
            # create list of 10 new weights using top three
            new_weights = []

            # iterate 10 times
            for _ in range(6):
                # randomly choose a top_network and get desired weight, then multiply
                # weight and random number close to 1
                e1 = random.choice(top_networks)['weights'][0] * random.uniform(0.95, 1.05)
                e2 = random.choice(top_networks)['weights'][1] * random.uniform(0.99, 1.01)

                # add new weights to list
                new_weights.append((e1, e2))

            # call generate_networks, pass in weights, set result equal to self.networks
            self.networks = self.generate_networks(new_weights)
            #print(f'Using top: {self.networks}')

        # reset hit networks
        self.hit_networks = []
        # clear obstacles
        self.game_object.clear_obstacles()
        # increment generation
        self.game_object.increment_generation()

    def move_obstacles(self):
        self.game_object.move_obstacles()

    def get_obstacles(self):
        return self.game_object.obstacles

    def get_game_objects(self):
        games = []
        for network in self.networks:
            games.append(network.gm)
        
        return games

    def get_is_over(self):
        ''' True if all networks lost, False if not
        '''
        is_overs = []

        for game in self.get_game_objects():
            is_overs.append(game.is_over)
        
        return sum(is_overs) == len(is_overs)
    
    def move_balls(self):
        for network in self.networks:
            network.move_ball()

    def is_collision(self, obstacles):
        new_networks = [] # updated networks, with hit ones removed
        for network in self.networks:
            is_hit = network.gm.is_collision(obstacles)
            if not is_hit:
                new_networks.append(network)
            else:
                self.hit_networks.append(network)

        self.networks = new_networks
                

    def get_inputs(self):
        inputs = []
        
        for network in self.networks:
            inputs.append(network.get_inputs())

        return inputs


class neural_network:
    # constructor with optional argument for weights, if nothing passed into
    # sny0, weight is randomly generated
    def __init__(self, gm):
        self.gm = gm # represents game object
        self.sny0 = 2 * np.random.random((2,1)) - 1
        #self.score = 0 # score of neural network

    def nonlin(self, x):
        return 1 / (1 + np.exp(-x))

    def guess(self, input1, input2):
        ''' Guesses ouput based on inputs

        Args:
            input1 (int): represents distance of center of ball to the 
                          left wall of the next obstacle
            input2 (int): represents height of next obstacle
        
        Returns:
            guess (float): represents the guessed value
        '''
        X = np.array([input1, input2])
        guess = self.nonlin(np.dot(X, self.sny0))

        return guess

    def set_weights(self, weights):
        self.sny0 = weights
    
    def get_ball_y(self):
        return self.gm.ball_y
    
    def get_ball_x(self):
        return self.gm.ball_x
    
    def get_obstacles(self):
        return self.gm.obstacles

    def get_score(self):
        return self.gm.score

    def generate_obstacle(self):
        self.gm.generate_obstacle()

    def move_ball(self):
        self.gm.move_ball()

    def is_collision(self):
        self.gm.is_collision()

    def jump_ball(self):
        self.gm.jump_ball()
    
    def get_inputs(self, obstacles):
        return self.gm.get_inputs(obstacles)


def test_generate_networks():
    no = network_object()
    networks = no.generate_networks()
    for n in networks:
        print(n.sny0)

def test_mutate_networks():
    no = network_object()
    g1 = game.game()
    n1 = neural_network(g1)
    g2 = game.game()
    n2 = neural_network(g2)
    g3 = game.game()
    n3 = neural_network(g3)

    no.hit_networks.append(n1)
    no.hit_networks.append(n2)
    no.hit_networks.append(n3)

    for network in no.hit_networks:
        print(network.sny0)

    print('---------')

    d = no.mutate_networks()

    for network in d:
        print(network.sny0)


# TESTING
if __name__ == '__main__':
    test_generate_networks()
