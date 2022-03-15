# import evader_controller
# import pursuer_controller
import FACL
import matplotlib.pyplot as plt
import numpy as np
# Maybe this class should have been named Agent but anyways, it exists so that we can plug a low level controller (FACL or FQL) into the agent
# Its purpose is to
class Agent:
    def __init__(self, controller):
        # default values
        self.training_iterations_max = 700 # number of milliseconds in a training/simulation episode
        self.controller = controller # this is the controller (FACL or FQL) that gets passed into the actor object
        self.success = 0 # this will count the number of sucesses (to be taken out later)
        self.reward_total = []

    def run_one_epoch(self,pos): # runs a single epoch of training
        # Reset the game
        self.controller.reset()
        # This function calls the controller iterator
        for i in range(self.training_iterations_max):
            self.controller.iterate()
            #if (): #need to define a stop case, maybe if the car is able to keep the slip close to 0 for 5 seconds end training early?
            #    self.success +=1
            #    #print('success -- end')
            #    break
        self.controller.updates_after_an_epoch() # decrease learning / increase exploitation
        self.reward_total.append(self.reward_sum_for_a_single_epoch())

        #print(self.controller.path)
    def run_action_selection(self):
        self.controller.complete_state_change()
    def compute_reward(self):
        self.controller.get_reward()
    def update_actor_critic(self):
        self.controller.update_actor_and_critic()
    def save_epoch_training_info(self):
        # finish later
        # gonna call a controller function so that we know what to save
        pass
    def end_of_epoch_calls(self):
        self.controller.updates_after_an_epoch()  # decrease learning / increase exploitation
        self.reward_total.append(self.reward_sum_for_a_single_epoch())

    def print_path(self): # thfig, ax = plt.subplots()
        x = [0] * (len(self.controller.path) - 1)
        y = [0] * (len(self.controller.path) - 1)
        print(len(self.controller.path))
        for i in range(len(self.controller.path) - 1):
            x[i] = self.controller.path[i][0]
            y[i] = self.controller.path[i][1]
        # plt.clf()
        fig, ax = plt.subplots()
        ax.plot(x, y)
        # add circle
        # circle = plt.Circle((self.controller.territory_coordinates[0], self.controller.territory_coordinates[1]),
        #                     self.controller.r, color='g', fill=False)
        #plt.plot(self.controller.territory_coordinates[0], self.controller.territory_coordinates[1], 'ro')
        # ax.add_patch(circle)
        plt.show()
        pass

    def reward_sum_for_a_single_epoch(self):
        total_rewards = sum(self.controller.reward_track)
        return total_rewards

    def print_reward_graph(self):
        fig, ax = plt.subplots()
        ax.plot(self.reward_total)
        plt.show()