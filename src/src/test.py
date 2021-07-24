from Initializer import create_board, init_simulation
from Functions import infinity_distance
#%%
board = create_board(3, 3)
simulation = init_simulation((0, 0), board, 0, infinity_distance, [2, 4])
actions = simulation.get_possible_actions()

#%%
actions = simulation.get_possible_actions()

for i, action in enumerate(actions):
    print(str(i) + ' ' + str(action.type))
#%%

print(simulation.board.print_board())
#%%
action = actions[13]
if action.type.name == "MOVE":

    print(str(action.source_cell.get_position()) + ' -> ' + str(action.target_cell.get_position()))
else:
    print(str(action.source_cell.get_position()))
#%%
simulation.run_one_epoch(action)

#%%
print(simulation.is_simulation_end())