from Functions import selectionFunction, retropropagationFunction
from Functions import movementChoiceFunction, expansionFunction
from Functions import simulationFunction, infinity_distance
from MCTSAgent import MontecarloPlayer
from Initializer import create_random_board, init_simulation


board = create_random_board(4, 4)

simulation = init_simulation((0, 0), board, 0, infinity_distance, [10, 2, 15, 5])
#%%

player = MontecarloPlayer(
    simulation,
    selectionFunction,
    expansionFunction,
    retropropagationFunction,
    simulationFunctionDummy,
    #simulationFunction,
    movementChoiceFunction
    )
#%%
print(simulation.board.find_container_by_id(10))
print(simulation.board.find_container_by_id(2))
print(simulation.board.find_container_by_id(15))
print(simulation.board.find_container_by_id(5))

#%%
print(simulation.board.get_board_row_view(0))

#%% Profundidad arbol

print(player.actionTreeDepth)

#%% Exploracion del arbol

player.exploreActionTree(200)

#%% Exploracion hasta cierta profundidad

i = 1

while player.actionTreeDepth < 16 and i < 10000:
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


#%% hijos del nodo padre
node = player.actionTree

print("Level: " + str(node.childs[0].level))
for i, x in enumerate(node.childs):
    if x.action.type.name == "MOVE":
        print(i, x.id, x.action.source_cell.get_position(), x.action.target_cell.get_position(), x.action.type, x.value, x.visits)
    elif x.action.type.name == "EXTRACT":
        print(i, x.id, x.action.source_cell.get_position(), "-", x.action.type, x.value, x.visits)
    elif x.action.type.name == "END":
        print(i, x.id, "-", "-", x.action.type, x.value, x.visits)



#%%
print(player.getBestMove())

#%% Simulacion completa
epochs = 600
i = 1
while not player.originalSimulation.is_simulation_end():
    print(i)
    player.exploreActionTree(epochs)
    best_move = player.getBestMove()
    child = player.getChildById(best_move.id)
    action = child.action
    player.originalSimulation.run_one_epoch(action)
    child.parent = None
    player.actionTree = child
    '''
    if epochs > 100:
        epochs = int(epochs / (1.2))
    else:
        epochs = 100
    '''
    i += 1

#%%

for action in player.originalSimulation.history.values():
    print(str(action))

#%%

print(simulation.board.get_board_top_level())
#%%
simulation.run_one_epoch(player.originalSimulation.history.get(6))
