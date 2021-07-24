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
from SimpleSimulation import ActionType
import cProfile, pstats


#%% ELEMENTOS DE SIMULACION

board = create_simple_board(8, 8)
move_actions = get_all_move_actions(board)
containers_to_extract_id = [30, 100, 21, 53, 67, 5, 80, 40, 101, 4, 3, 2, 1, 0]
#containers_to_extract_id = [30, 100, 21, 53]
containers_to_extract_id_size = len(containers_to_extract_id)

simulation = init_simulation((0, 0), board, 0, euclidian_distance, containers_to_extract_id, move_actions)

#%% EXPLORACION DEL ARBOL DE DECISIONES

profiler = cProfile.Profile()
profiler.enable()

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
    offline_player = MontecarloPlayer(
        offline_simulation,
        selectionFunction,
        expansionFunction,
        retropropagationFunction,
        simulationFunction,
        movementChoiceFunction
        )
    
    finish_explore = False
    
    while not finish_explore:
        offline_player.exploreActionTree(30, log=False)
        offline_bestMoveSequence = offline_player.getBestMoveSequence()
        finish_explore = offline_bestMoveSequence[-1].action.type == ActionType.END
    
    is_end_action = False
    j = 0
    while not is_end_action and j < 11:
        
        if j == 10:
            print("ERROR")
        
        if offline_bestMoveSequence[j].action.type == ActionType.END:
            is_end_action = True
        else:    
            actions.append(offline_bestMoveSequence[j].action)
            offline_simulation.execute_action(offline_bestMoveSequence[j].action)
        j += 1

    if (i + 1) < containers_to_extract_id_size:

        offline_simulation = Simulation(
            offline_simulation.crane_position,
            offline_simulation.board,
            offline_simulation.time,
            offline_simulation.distance_function,
            [containers_to_extract_id[i+1]],
            offline_simulation.move_actions)
 

    i += 1

profiler.disable()

#%%

for i, x in enumerate(actions):
    if x.type.name == "MOVE":
        print(i, (x.source_cell.get_position(), x.target_cell.get_position(), x.type))
    elif x.type.name == "EXTRACT":
        print(i, (x.source_cell.get_position(), "-", x.type))
    elif x.type.name == "END":
        print(i, ("-", "-", x.action.type))

#%%
original_simulation = init_simulation((0, 0), board, 0, euclidian_distance, containers_to_extract_id, move_actions)
for action in actions:
    original_simulation.run_one_epoch(action)
    
#%%

print(original_simulation.time)
