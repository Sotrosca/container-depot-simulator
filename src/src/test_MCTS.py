from Functions import selectionFunction, retropropagationFunction
from Functions import movementChoiceFunction, expansionFunction
from Functions import simulationFunction, infinity_distance
from MCTSAgent import MontecarloPlayer
from Initializer import create_random_board, init_simulation, create_custom_board


#board = create_random_board(3, 3)
board = create_custom_board() # Escenario creado a mano
simulation = init_simulation((0, 0), board, 0, infinity_distance, [2, 4])

player = MontecarloPlayer(
    simulation,
    selectionFunction,
    expansionFunction,
    retropropagationFunction,
    simulationFunction,
    movementChoiceFunction
    )

#%%
print("Época: " + str(simulation.epochs))
print("Tiempo: " + str(simulation.time))
print(board)
best_move = player.getBestMove(1000)

child = player.getChildById(best_move.id)

#%%
action = child.action
if action.type.name == "MOVE":
    print(str(action.source_cell.get_position()) + ' -> ' + str(action.target_cell.get_position()))
else:
    print(str(action.source_cell.get_position()))

#%% hijos del nodo padre

for l in map(lambda x : (x.action.source_cell.get_position(), x.action.target_cell.get_position(), x.action.type, x.value, x.visits), player.actionTree.childs):
    print(l)

#%% hijos del mejor hijo

for l in map(lambda x : (x.action.source_cell.get_position(), x.action.target_cell.get_position(), x.action.type, x.value, x.visits), child.childs):
    print(l)

#%%
child_2 = movementChoiceFunction(child)

#%%
print(child_2)
#%%

action_2 = child_2.action

if action_2.type.name == "MOVE":
    print(str(action_2.source_cell.get_position()) + ' -> ' + str(action_2.target_cell.get_position()))
else:
    print(str(action_2.source_cell.get_position()))

#%% hijos child_2
for l in map(lambda x : (x.action.source_cell.get_position(), x.action.target_cell.get_position(), x.action.type, x.value, x.visits) if x.action.type.name == "MOVE" else (x.action.type, x.value, x.visits), child_2.childs):
    print(l)

#%%
print(board.print_board())


#%%
simulation.run_one_epoch(action)
print("----")
print("Época: " + str(simulation.epochs))
print("Tiempo: " + str(simulation.time))

#%% Simulacion completa

while not simulation.is_simulation_end():
    best_move = player.getBestMove(2000)
    child = player.getChildById(best_move.id)
    action = child.action
    player.originalSimulation.run_one_epoch(action)
    child.parent = None
    player.actionTree = child

#%%

for action in simulation.history.values():
    if action.type.name == "MOVE":
        print((action.source_cell.get_position(), action.target_cell.get_position(), action.type))
    elif action.type.name == "EXTRACT":
        print((action.source_cell.get_position(), action.type))
