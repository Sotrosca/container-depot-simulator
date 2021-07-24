#%%
from Functions_4_Moves import selectionFunction, retropropagationFunction
from Functions_4_Moves import movementChoiceFunction, expansionFunction
from Functions_4_Moves import simulationFunction, infinity_distance, simulationFunctionDummy
from Functions_4_Moves import selectionFunctionBlockingDegree
from Functions_4_Moves import calculateBlockingDegree
from MCTSAgent import MontecarloPlayer
from Initializer import init_simulation, create_custom_board, create_random_board
import time

start_time = time.time()

#%%
#board = create_custom_board() # Escenario creado a mano
#simulation = init_simulation((0, 0), board, 0, infinity_distance, [2, 4, 8])
#simulation = init_simulation((0, 0), board, 0, infinity_distance, [2])

#%%

board = create_random_board(10, 10)

simulation = init_simulation((0, 0), board, 0, infinity_distance, [10, 2, 15, 5])

player = MontecarloPlayer(
    simulation,
    selectionFunction,
    expansionFunction,
    retropropagationFunction,
    simulationFunctionDummy,
    movementChoiceFunction
    )
#%%

print(calculateBlockingDegree(simulation))
for i, child in enumerate(player.actionTree.childs):
    print(i, calculateBlockingDegree(child.simulationCopy), child.action)
#%%

print(simulation.board.find_container_by_id(10))
print(simulation.board.find_container_by_id(2))
print(simulation.board.find_container_by_id(15))
print(simulation.board.find_container_by_id(5))

#%%
print(simulation.board.get_board_row_view(0))

#%% Exploracion hasta cierta profundidad

i = 1

while player.actionTreeDepth < 10 and i < 5000:
    player.exploreActionTree(1, log=False)
    if i % 50 == 0:
        print((i, player.actionTreeDepth))
    i += 1

#%% Mejor secuencia de movimientos

bestMoveSequence = player.getBestMoveSequence()

for x in bestMoveSequence:
    if x.action.type.name == "MOVE":
        print((x.id, x.action.source_cell.get_position(), x.action.target_cell.get_position(), x.action.type, x.value, x.visits))
    elif x.action.type.name == "EXTRACT":
        print((x.id, x.action.source_cell.get_position(), "-", x.action.type, x.value, x.visits))
    elif x.action.type.name == "END":
        print((x.id, "-", "-", x.action.type, x.value, x.visits))




#%% Simulacion completa
i = 1
while not player.originalSimulation.is_simulation_end():
    print(i)
    player.exploreActionTree(1000)
    best_move = player.getBestMove()
    child = player.getChildById(best_move.id)
    action = child.action
    player.originalSimulation.run_one_epoch(action)
    child.parent = None
    player.actionTree = child

    i += 1

#%%

for action in player.originalSimulation.history.values():
    print(str(action))

print("Program finished in ", time.time() - start_time)
#%%

print(simulation.board.get_board_top_level())

#%%

simulation.run_one_epoch(player.originalSimulation.history.get(4))
