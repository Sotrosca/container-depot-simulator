#%% IMPORTS

from Functions_blocking_degree import manhattan_distance
from Functions_blocking_degree import get_all_move_actions
from Initializer import init_simulation, create_simple_board
import Utils
from SimpleSimulation import Simulation
import random
from SimpleSimulation import ActionType

#%%

print_moves = True

#%% SIMULACION

board = create_simple_board(5, 5)
move_actions = get_all_move_actions(board)
#containers_to_extract_id = [49, 114, 57, 92, 82, 27, 123, 59, 56, 84, 89, 96, 4, 10, 116, 83, 119, 36, 7, 48, 37, 72, 41, 79, 52, 1, 50, 94, 24, 11, 23, 107, 30, 118, 45, 62, 112, 76, 100, 117, 95, 69, 108, 35, 31, 29, 66, 40, 73, 54]
containers_to_extract_id = [42, 24, 23, 39, 40, 2, 35, 41, 9, 20, 16, 6, 30, 37, 15, 19, 0, 22, 31, 3]
containers_to_extract_id_size = len(containers_to_extract_id)

simulation = init_simulation((0, 0), board, 0, manhattan_distance, containers_to_extract_id, move_actions)

#%%
offline_original_simulation = Utils.copySimulation(simulation)

i = 0

actions = []

offline_simulation = Utils.copySimulation(offline_original_simulation)

offline_simulation = Simulation(
    offline_simulation.crane_position,
    offline_simulation.board,
    offline_simulation.time,
    offline_simulation.distance_function,
    [containers_to_extract_id[0]],
    offline_simulation.move_actions)

while i < containers_to_extract_id_size:
    end_container = False
    while not end_container:
        possible_actions = offline_simulation.get_possible_actions()
        possible_actions_size = len(possible_actions)
        there_is_extract = False
        action_extract = None
        k = 0
        while not there_is_extract and k < possible_actions_size:

            there_is_extract = possible_actions[k].type == ActionType.EXTRACT
            if there_is_extract:
                action_extract = possible_actions[k]
            k += 1
        
        if there_is_extract:
            action = action_extract
        else:
            best_actions = {}
            for _action in possible_actions:
                cost = offline_simulation.distance_function(_action.source_cell.get_position(), _action.target_cell.get_position())
                if cost in best_actions:
                    best_actions.get(cost).append(_action)
                else:
                    best_actions[cost] = [_action]
                
            best_actions_list = best_actions.get(min(best_actions))
            action = random.choice(best_actions_list)
            
        actions.append(action)
        offline_simulation.execute_action(action)
        
        if there_is_extract and (i + 1) < containers_to_extract_id_size:
            offline_simulation = Simulation(
                offline_simulation.crane_position,
                offline_simulation.board,
                offline_simulation.time,
                offline_simulation.distance_function,
                [containers_to_extract_id[i+1]],
                offline_simulation.move_actions)      
            end_container = True
        elif there_is_extract and (i + 1) == containers_to_extract_id_size:
            end_container = True
        

    i += 1
    
#%%

original_simulation = init_simulation((0, 0), board, 0, manhattan_distance, containers_to_extract_id, move_actions)

for i, action in enumerate(actions):
    original_simulation.run_one_epoch(action)
    if print_moves:
        print(i, Utils.get_printable_action(action), original_simulation.time, original_simulation.blocking_degree)

offline_time = original_simulation.time
#%%
print("OFFLINE: ", original_simulation.time)
    