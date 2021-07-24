#%% IMPORTS

from Functions_blocking_degree import selectionFunction
from Functions_blocking_degree import expansionFunction
from Functions_blocking_degree import simulationFunction
from Functions_blocking_degree import retropropagationFunction
from Functions_blocking_degree import movementChoiceFunction
from Functions_blocking_degree import euclidian_distance
from Functions_blocking_degree import get_all_move_actions
from MCTSAgent import MontecarloPlayer
from Initializer import init_simulation, create_simple_board
import Utils
from SimpleSimulation import Simulation
import random
from SimpleSimulation import ActionType



#%% SIMULACION

board = create_simple_board(5, 5)
move_actions = get_all_move_actions(board)
containers_to_extract_id = [42, 24, 23, 39, 40, 2, 35, 41, 9, 20, 16, 6, 30, 37, 15, 19, 0, 22, 31, 3]
containers_to_extract_id_size = len(containers_to_extract_id)

simulation = init_simulation((0, 0), board, 0, euclidian_distance, containers_to_extract_id, move_actions)

#%% AGENTE ONLINE
player = MontecarloPlayer(
    simulation,
    selectionFunction,
    expansionFunction,
    retropropagationFunction,
    simulationFunction,
    movementChoiceFunction
    )

#%% EXPLORACION DEL ARBOL DE DECISIONES

i = 1

while player.actionTreeDepth < 180:
    player.exploreActionTree(1, log=False)
    if i % 20 == 0:
        print((i, player.actionTreeDepth))
    i += 1


#%% Mejor secuencia de movimientos

bestMoveSequence = player.getBestMoveSequence()
print(bestMoveSequence[-1].simulationCopy.time)
#%%

offline_original_simulation = Utils.copySimulation(simulation)

i = 0

actions = []

original_simulation = init_simulation((0, 0), board, 0, euclidian_distance, [containers_to_extract_id[0]], move_actions)

offline_simulation = Utils.copySimulation(offline_original_simulation)

offline_simulation = Simulation(
    offline_simulation.crane_position,
    offline_simulation.board,
    offline_simulation.time,
    offline_simulation.distance_function,
    [containers_to_extract_id[0]],
    offline_simulation.move_actions)

while i < containers_to_extract_id_size:
    print(i)
    end_container = False
    while not end_container:
        possible_actions = offline_simulation.get_possible_actions()
        possible_actions_size = len(possible_actions)
        there_is_extract = False
        action_extract = None
        k = 0
        while not there_is_extract and k < possible_actions_size:
            _action = possible_actions[k]
            there_is_extract = _action.type == ActionType.EXTRACT
            if there_is_extract:
                action_extract = _action
            k += 1
        
        if there_is_extract:
            action = action_extract
        else:
            action = random.choice(offline_simulation.get_possible_actions())
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
original_simulation = init_simulation((0, 0), board, 0, euclidian_distance, containers_to_extract_id, move_actions)

print("OFFLINE: ")
for i, action in enumerate(actions):
    original_simulation.run_one_epoch(action)
    print(i, Utils.get_printable_action(action), original_simulation.time)

offline_time = original_simulation.time
print("OFFLINE: ", original_simulation.time)
    
#%%

print("ONLINE: ")
for i, node in enumerate(bestMoveSequence):
    action = node.action
    print(i, Utils.get_printable_action(action), node.simulationCopy.time)

online_time = node.simulationCopy.time
print("ONLINE: ", node.simulationCopy.time)

#%%

print("OFFLINE: ", offline_time)
print("ONLINE: ", online_time)
