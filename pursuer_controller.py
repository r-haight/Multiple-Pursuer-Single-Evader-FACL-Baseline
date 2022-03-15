import numpy as np
from FACL import FACL


class pursuer_controller(FACL):
    pursuer_count = 0
    def __init__(self, state, max, min, num_mf):
        pursuer_controller.pursuer_count=pursuer_controller.pursuer_count + 1
        self.pursuer_number = pursuer_controller.pursuer_count
        self.state = state.copy()
        self.path = state.copy()
        self.initial_position = state.copy()
        self.r = 1 #radius of the territory
        self.v = 1.2 # unit velocity
        self.reward_track =[] # to keep track of the rewards
        self.distance_away_from_evader_t = self.distance_from_an_evader([0, 0]) #maybe change this later to make it dynamic
        FACL.__init__(self, max, min, num_mf) #explicit call to the base class constructor
        print('constructor initial pos',self.initial_position)

    def get_reward(self, evader_coor,flag):
        self.distance_away_from_evader_t1 = self.distance_from_an_evader(evader_coor)
        if(flag==1 and self.pursuer_number==1):
            r=0
            #print('pursuer 1 captured evader')
        elif (flag == 2 and self.pursuer_number == 2):
            r = 0
            #print('pursuer 2 captured evader')
        elif (flag == 3 and self.pursuer_number == 3):
            r = 0
        else:
            # new position - the current position
            r = ( self.distance_away_from_evader_t - self.distance_away_from_evader_t1)
        self.distance_away_from_evader_t = self.distance_away_from_evader_t1
        self.update_reward_graph(r)
        return r

    def update_state(self):
        self.state[0] = self.state[0] + self.v * np.cos(self.u_t)
        self.state[1] = self.state[1] + self.v * np.sin(self.u_t)
        self.update_path(self.state)

        pass

    def reset(self):
        # Edited for each controller
        self.state = self.initial_position.copy()
        self.path = []
        self.path = self.state
        self.reward_track = []
        self.distance_away_from_evader_t= self.distance_from_an_evader([0, 0])  # maybe change this later to make it dynamic
        # print('reset called pursuer state', self.state)
        # print('initial pos in reset',self.initial_position)
        pass

    def update_path(self, state):
        self.path = np.vstack([self.path, state])
        pass

    def update_reward_graph(self, r):
        self.reward_track.append(r)

    def distance_from_an_evader(self, pursuer_coordinate):
        distance_away_from_target = np.sqrt(
            (self.state[0] - pursuer_coordinate[0]) ** 2 + (
                        self.state[1] - pursuer_coordinate[1]) ** 2)
        return distance_away_from_target

