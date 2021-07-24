#%% IMPORTS

from Functions_blocking_degree import selectionFunction
from Functions_blocking_degree import expansionFunction
from Functions_blocking_degree import simulationFunction
from Functions_blocking_degree import retropropagationFunction
from Functions_blocking_degree import movementChoiceFunction
from Functions_blocking_degree import manhattan_distance
from Functions_blocking_degree import calculateBlockingDegree
from Functions_blocking_degree import get_all_move_actions
from MCTSAgent import MontecarloPlayer
from Initializer import init_simulation, create_simple_board
import cProfile, pstats


#%% SIMULACION

board = create_simple_board(5, 5)
move_actions = get_all_move_actions(board)
#containers_to_extract_id = [30, 100, 21, 53, 67, 5, 80, 40, 101, 4, 3, 2, 1, 0]
#containers_to_extract_id = [30, 100, 21, 53]
#containers_to_extract_id = [49, 114, 57, 92, 82, 27, 123, 59, 56, 84, 89, 96, 4, 10, 116, 83, 119, 36, 7, 48, 37, 72, 41, 79, 52, 1, 50, 94, 24, 11, 23, 107, 30, 118, 45, 62, 112, 76, 100, 117, 95, 69, 108, 35, 31, 29, 66, 40, 73, 54]

containers_to_extract_id = [42, 24, 23, 39, 40, 2, 35, 41, 9, 20, 16, 6, 30, 37, 15, 19, 0, 22, 31, 3]
simulation = init_simulation((0, 0), board, 0, manhattan_distance, containers_to_extract_id, move_actions)
#%% AGENTE
player = MontecarloPlayer(
    simulation,
    selectionFunction,
    expansionFunction,
    retropropagationFunction,
    simulationFunction,
    movementChoiceFunction
    )
#%% BLOCKING DEGREE DE PRIMOGENITOS

print(calculateBlockingDegree(player.originalSimulation))
for i, child in enumerate(player.actionTree.childs):
    print(i, calculateBlockingDegree(child.simulationCopy), child.action)


#%% VISUALIZACION DE UBICACION CONTAINERS

infimum = 0

for container_id in containers_to_extract_id:
    container_position = simulation.board.find_container_by_id(container_id)
    infimum += 1 + container_position[2]
    print(container_id, container_position)
    
print(infimum)
#%% EXPLORACION DEL ARBOL DE DECISIONES

profiler = cProfile.Profile()
profiler.enable()

i = 1

while player.actionTreeDepth < 60:
    player.exploreActionTree(1, log=False)
    if i % 20 == 0:
        print((i, player.actionTreeDepth))
    i += 1

profiler.disable()

#%% PROFILER STATS
stats = pstats.Stats(profiler).strip_dirs()
#%% TIEMPO DE EJECUCION PROFILER
stats.sort_stats('tottime').print_stats()

#%%
stats.sort_stats('cumtime').print_stats()
#%% CALLERS
stats.print_callers()

#%% CALLEES
stats.print_callees()


#%% Mejor secuencia de movimientos

bestMoveSequence = player.getBestMoveSequence()

for i, x in enumerate(bestMoveSequence):
    if x.action.type.name == "MOVE":
        print(i, (x.id, x.action.source_cell.get_position(), x.action.target_cell.get_position(), x.action.type, x.value, x.visits), x.simulationCopy.time, x.simulationCopy.blocking_degree)
    elif x.action.type.name == "EXTRACT":
        print(i, (x.id, x.action.source_cell.get_position(), "-", x.action.type, x.value, x.visits), x.simulationCopy.time, x.simulationCopy.blocking_degree)
    elif x.action.type.name == "END":
        print(i, (x.id, "-", "-", x.action.type, x.value, x.visits), x.simulationCopy.time, x.simulationCopy.blocking_degree)

#%%

print('TIME: ', bestMoveSequence[-1].simulationCopy.time)

#%% VISUALIZACION DE NODOS DEL ARBOL DE DECISION
node = player.actionTree


node = bestMoveSequence[1]

_childs = node.childs
_level = node.level

print("Level: " + str(_level))
for i, x in enumerate(_childs):
    if x.action.type.name == "MOVE":
        print(i, x.id, x.action.source_cell.get_position(), x.action.target_cell.get_position(), x.action.type, x.value, x.visits)
    elif x.action.type.name == "EXTRACT":
        print(i, x.id, x.action.source_cell.get_position(), "-", x.action.type, x.value, x.visits)
    elif x.action.type.name == "END":
        print(i, x.id, "-", "-", x.action.type, x.value, x.visits)

#%% EJECUCION DE MOVIMIENTOS SOBRE LA SIMULACION
'''
for node in bestMoveSequence[0:2]:
    simulation.run_one_epoch(node.action)
#%%
player = MontecarloPlayer(
    simulation,
    selectionFunction,
    expansionFunction,
    retropropagationFunction,
    simulationFunction,
    movementChoiceFunction
    )
'''
#%%

import random
print(random.sample(range(0, 45), 45))
