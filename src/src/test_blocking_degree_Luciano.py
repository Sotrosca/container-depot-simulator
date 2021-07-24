#%% IMPORTS

from Functions_blocking_degree import manhattan_distance, selectionFunction
from Functions_blocking_degree import expansionFunction
from Functions_blocking_degree import simulationFunction
from Functions_blocking_degree import retropropagationFunction
from Functions_blocking_degree import movementChoiceFunction
from Functions_blocking_degree import infinity_distance
from Functions_blocking_degree import calculateBlockingDegree
from Functions_blocking_degree import get_all_move_actions
from MCTSAgent import MontecarloPlayer
from Initializer import init_simulation, create_simple_board
import cProfile, pstats

#%% SIMULACION

board = create_simple_board(10, 10)
move_actions = get_all_move_actions(board)
containers_to_extract_id = [15, 2, 10, 5, 30, 1, 20]
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

for container_id in containers_to_extract_id:
    print(container_id, simulation.board.find_container_by_id(container_id))
#%% EXPLORACION DEL ARBOL DE DECISIONES
%%time
profiler = cProfile.Profile()
profiler.enable()

i = 1

while player.actionTreeDepth < 20:
    player.exploreActionTree(1, log=False)
    if i % 50 == 0:
        print((i, player.actionTreeDepth))
    i += 1

profiler.disable()

#%% PROFILER STATS
stats = pstats.Stats(profiler).strip_dirs()
#%% TIEMPO DE EJECUCION PROFILER
stats.sort_stats('tottime').print_stats()

#%% CALLERS
stats.print_callers()

#%% CALLEES
stats.print_callees()


#%% Mejor secuencia de movimientos

bestMoveSequence = player.getBestMoveSequence()

for i, x in enumerate(bestMoveSequence):
    if x.action.type.name == "MOVE":
        print(i, (x.id, x.action.source_cell.get_position(), x.action.target_cell.get_position(), x.action.type, x.value, x.visits))
    elif x.action.type.name == "EXTRACT":
        print(i, (x.id, x.action.source_cell.get_position(), "-", x.action.type, x.value, x.visits))
    elif x.action.type.name == "END":
        print(i, (x.id, "-", "-", x.action.type, x.value, x.visits))

#%% VISUALIZACION DE NODOS DEL ARBOL DE DECISION
node = player.actionTree


_node = bestMoveSequence[4]

_childs = _node.childs
_level = _node.level

print("Level: " + str(_level))
for i, x in enumerate(_childs):
    if x.action.type.name == "MOVE":
        print(i, x.id, x.action.source_cell.get_position(), x.action.target_cell.get_position(), x.action.type, x.value, x.visits)
    elif x.action.type.name == "EXTRACT":
        print(i, x.id, x.action.source_cell.get_position(), "-", x.action.type, x.value, x.visits)
    elif x.action.type.name == "END":
        print(i, x.id, "-", "-", x.action.type, x.value, x.visits)

#%% EJECUCION DE MOVIMIENTOS SOBRE LA SIMULACION

for node in bestMoveSequence[0:14]:
    player.originalSimulation.run_one_epoch(node.action)

# %%
player.originalSimulation.time