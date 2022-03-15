# This is a program that simulates 3 slower sursuers and 1 high speed evader
# this will be used as my base to show that co-operation is better than no co-operation in FACL
# This program also centres around the FACL algorithm
import numpy as np
import FACL
from Agent import Agent
from pursuer_controller import pursuer_controller
from evader_controller import evader_controller
import matplotlib.pyplot as plt
# State Variables and Ranges for the FIS

state_max = [50, 50] # max values of the grid [x,y]
state_min = [-50, -50] # smallest value of the grid [x,y]
num_of_mf = [9, 9] # breaking up the state space (grid in this case) into 29 membership functions

# Creation of our 3 Pursuers
Pursuer_1_controller = pursuer_controller([0,-5], state_max, state_min, num_of_mf)  # create the FACL controller
P1 = Agent(Pursuer_1_controller)  # create the agent with the above controller
Pursuer_2_controller = pursuer_controller([-5,5], state_max, state_min, num_of_mf)  # create the FACL controller
P2 = Agent(Pursuer_2_controller)  # create the agent with the above controller
Pursuer_3_controller = pursuer_controller([8,8], state_max, state_min, num_of_mf)  # create the FACL controller
P3 = Agent(Pursuer_3_controller)  # create the agent with the above controller
Evader_controller = evader_controller([0,0], state_max, state_min, num_of_mf)  # create the FACL controller
E = Agent(Evader_controller)  # create the agent with the above controller
# print out all the rule sets
print("rules:")
print(P1.controller.rules)
capture_count = 0
number_of_epochs = 200
#Training Epoch Loop
for n in range(number_of_epochs):
    #reset game
    E.controller.reset()
    P1.controller.reset()
    P2.controller.reset()
    # Game Loop
    for i in range(45):

        E.run_action_selection()
        P1.run_action_selection()
        P2.run_action_selection()

        E.controller.get_reward(P1.controller.state, P2.controller.state)
        P1.controller.get_reward(E.controller.state,E.controller.captured_flag)
        P2.controller.get_reward(E.controller.state,E.controller.captured_flag)

        E.update_actor_critic()
        P1.update_actor_critic()
        P2.update_actor_critic()

        #Call a function to decide when capture has been met
        if(E.controller.captured_flag>0):
            #print('Evader Captured')
            capture_count=capture_count+1
            break

    E.end_of_epoch_calls()
    P1.end_of_epoch_calls()
    P2.end_of_epoch_calls()

print('total number of captures:',capture_count)
print('total number of evasions:', number_of_epochs-capture_count)
# Print the path that our agents took in the last epoch
# E.print_reward_graph()
# P1.print_reward_graph()
# P2.print_reward_graph()

x_e = [0] * (len(E.controller.path) )
y_e = [0] * (len(E.controller.path) )
x_p1 = [0] * (len(P1.controller.path) )
y_p1 = [0] * (len(P1.controller.path) )
x_p2 = [0] * (len(P2.controller.path) )
y_p2 = [0] * (len(P2.controller.path) )
print(len(E.controller.path))
print(len(P1.controller.path))
print(len(P2.controller.path))
for i in range(len(E.controller.path) ):
     x_e[i] = E.controller.path[i][0]
     y_e[i] = E.controller.path[i][1]
     x_p1[i] = P1.controller.path[i][0]
     y_p1[i] = P1.controller.path[i][1]
     x_p2[i] = P2.controller.path[i][0]
     y_p2[i] = P2.controller.path[i][1]
# plt.clf()
fig, ax = plt.subplots()
ax.plot(x_e, y_e)
plt.plot(x_p1,y_p1)
plt.plot(x_p2,y_p2)
circle = plt.Circle((x_e[len(E.controller.path)-1], y_e[len(E.controller.path)-1]),
                     E.controller.r, color='b', fill=False)
ax.add_patch(circle)
ax.legend(['evader','pursuer1','pursuer2'])
plt.show()