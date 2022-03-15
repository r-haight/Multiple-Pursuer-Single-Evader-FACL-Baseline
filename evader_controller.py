import numpy as np
from FACL import FACL

class evader_controller(FACL):

    def __init__(self, state, max, min, num_mf):
        self.state = state.copy()
        self.path = state.copy()
        self.initial_position = state.copy()
        self.r = 1 #radius of the territory
        self.v = 1.0  # unit velocity
        self.reward_track =[] # to keep track of the rewards
        self.distance_away_from_p1_t = self.distance_from_a_pursuer([0, -5]) #maybe change this later to make it dynamic
        self.distance_away_from_p2_t = self.distance_from_a_pursuer([8,8])
        self.captured_flag = 0
        FACL.__init__(self, max, min, num_mf) #explicit call to the base class constructor
    def get_reward(self, p1_coor,p2_coor):
        self.distance_away_from_p1_t1 = self.distance_from_a_pursuer(p1_coor)
        self.distance_away_from_p2_t1 = self.distance_from_a_pursuer(p2_coor)
        # print('evader distance from p1:', self.distance_away_from_p1_t1)
        # print('evader distance from p2:', self.distance_away_from_p2_t1)
        # new position - the current position

        if(self.distance_away_from_p1_t1<self.r):
            self.captured_flag=1
            r=0
        elif(self.distance_away_from_p2_t1<self.r):
            self.captured_flag=2
            r=0
        else:
            self.distance_away_from_p1_t = self.distance_away_from_p1_t1
            self.distance_away_from_p2_t = self.distance_away_from_p2_t1
            r = (self.distance_away_from_p1_t1 - self.distance_away_from_p1_t) + (
                        self.distance_away_from_p2_t1 - self.distance_away_from_p2_t)
        r = (self.distance_away_from_p1_t1 - self.distance_away_from_p1_t) + (
                self.distance_away_from_p2_t1 - self.distance_away_from_p2_t)
        self.update_reward_graph(r)
        return r

    def update_state(self):
        self.state[0] = self.state[0] + self.v * np.cos(self.u_t)
        self.state[1] = self.state[1] + self.v * np.sin(self.u_t)
        self.update_path(self.state)
        pass

    def reset(self):
        # Edited for each controller
        self.captured_flag=0
        self.state = self.initial_position.copy() # set to self.initial_state, debug later???
        self.path = []
        self.path = self.state.copy()
        self.reward_track = []
        self.distance_away_from_p1_t = self.distance_from_a_pursuer([0, -5])  # maybe change this later to make it dynamic
        self.distance_away_from_p2_t = self.distance_from_a_pursuer([8, 8])
        # print('evader reset')
        pass

    def update_path(self, state):
        self.path = np.vstack([self.path, state])
        pass

    def update_reward_graph(self, r):
        self.reward_track.append(r)

    def distance_from_a_pursuer(self,pursuer_coordinate):
        distance_away_from_target = np.sqrt(
            (self.state[0] - pursuer_coordinate[0]) ** 2 + (
                        self.state[1] - pursuer_coordinate[1]) ** 2)
        return distance_away_from_target