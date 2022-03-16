import matplotlib.pyplot as plt
import numpy as np
import FACL
from Agent import Agent
from pursuer_controller import pursuer_controller
from evader_controller import evader_controller

# creation of penelope, the agent who goes to a location
state = [5, 5]  # start position on the grid
state_max = [50, 50]  # max values of the grid [x,y]
state_min = [-50, -50]  # smallest value of the grid [x,y]
num_of_mf = [9, 9]  # breaking up the state space (grid in this case) into 29 membership functions
action_space = [0.785375, 2.356125, -1.57075, -0.785375, 0, 1.57075, -2.356125]

evader_controller = evader_controller([0, 0], state_max, state_min, num_of_mf)
elizabeth = Agent(evader_controller)

pursuer1_controller = pursuer_controller([5, 5], state_max, state_min, num_of_mf)  # create the FACL controller
penelope = Agent(pursuer1_controller)  # create the agent with the above controller

pursuer2_controller = pursuer_controller([-5, 5], state_max, state_min, num_of_mf)  # create the FACL controller
piper = Agent(pursuer2_controller)  # create the agent with the above controller

# print out all the rule sets
print("rules:")
print(penelope.controller.rules)

pen_flag = 0
pip_flag = 0

for i in range(1500):
    # Reset the game
    elizabeth.controller.reset()
    penelope.controller.reset()
    piper.controller.reset()
    pen_flag = 0
    pip_flag = 0
    # This function calls the controller iterator
    for i in range(penelope.training_iterations_max):
        pursuer_coordinate = [penelope.controller.state[0], penelope.controller.state[1], piper.controller.state[0],
                              piper.controller.state[1]]
        elizabeth.controller.iterate([20, 20])
        penelope.controller.iterate(elizabeth.controller.state)
        piper.controller.iterate(elizabeth.controller.state)
        if (penelope.controller.distance_from_target(
                elizabeth.controller.state) < 1):  ##change to a check capture / completion function later
            penelope.success += 1
            pen_flag = 1
            break
        elif (piper.controller.distance_from_target(elizabeth.controller.state) < 1):
            piper.success += 1
            pip_flag = 1
        if (pip_flag == 1 or pen_flag == 1):
            break
    penelope.end_of_epoch()
    piper.end_of_epoch()
    elizabeth.end_of_epoch()

print('penelope success: ', penelope.success)
print('piper success', piper.success)
print('total capture = ', piper.success + penelope.success)
# Print the path that our agent penelope took in her last epoch
print(penelope.controller.path)
# penelope.print_path()
penelope.print_reward_graph()
# piper.print_path()
piper.print_reward_graph()
x_e = [0] * (len(elizabeth.controller.path))
y_e = [0] * (len(elizabeth.controller.path))
x_p1 = [0] * (len(penelope.controller.path))
y_p1 = [0] * (len(penelope.controller.path))
x_p2 = [0] * (len(piper.controller.path))
y_p2 = [0] * (len(piper.controller.path))
print(len(piper.controller.path))
for i in range(len(piper.controller.path)):
    x_e[i] = elizabeth.controller.path[i][0]
    y_e[i] = elizabeth.controller.path[i][1]
    x_p2[i] = piper.controller.path[i][0]
    y_p2[i] = piper.controller.path[i][1]
    x_p1[i] = penelope.controller.path[i][0]
    y_p1[i] = penelope.controller.path[i][1]
# plt.clf()
fig, ax = plt.subplots()
ax.plot(x_p2, y_p2)
plt.plot(x_p1, y_p1)
plt.plot(x_e, y_e)
# add circle
circle = plt.Circle((elizabeth.controller.state[0], elizabeth.controller.state[1]),
                    piper.controller.r, color='g', fill=False)
plt.plot(elizabeth.controller.state[0], elizabeth.controller.state[1], 'ro')
ax.add_patch(circle)
plt.show()