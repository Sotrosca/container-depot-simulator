import random
import numpy as np
import copy

def selectionFunction(treeNodes):
    UCTConstant = 0.00000001
    selectedNode = treeNodes

    while selectedNode.hasChilds():
        childsWithoutLove = selectedNode.getChildsWithoutVisits()

        if len(childsWithoutLove) > 0:
            selectedNode = random.choice(childsWithoutLove)

        else:
            selectionValueUCT = -1
            winnerNode = None

            for child in selectedNode.childs:
                childSuccessRatio = child.value / child.visits

                logRatio = (np.log(selectedNode.visits) / child.visits) ** 0.5

                childValueUCT = childSuccessRatio + UCTConstant * logRatio

                if childValueUCT > selectionValueUCT:
                    selectionValueUCT = childValueUCT
                    winnerNode = child

            selectedNode = winnerNode

    return selectedNode

def expansionFunction(node):
    return node.visits > 4

def simulationFunction(actionNode):
    # Simulacion random (ver de utilizar otra)
    _simulationCopy = copy.deepcopy(actionNode.simulationCopy)
    i = 1
    while not _simulationCopy.is_simulation_end() and i < 20:
        possibleActions = _simulationCopy.get_possible_actions()
        action = None
        for _action in possibleActions:
            if _action.type.name == "EXTRACT":
                action = _action
        if action == None:
            action = random.choice(possibleActions)
        _simulationCopy.run_one_epoch(action)
        i += 1

    # funcion de penalizacion
    if not _simulationCopy.is_simulation_end():
        _simulationCopy.time += 1000

    return _simulationCopy

def retropropagationFunction(originalSimulation, simulationFinished, actionNode):

    valueNode = 1 / (simulationFinished.time ** 2) # Mejorar
    actualNode = actionNode

    actualNode.visits += 1
    actualNode.value += valueNode

    while actualNode.hasParent():
        actualNode = actualNode.parent
        actualNode.visits += 1
        actualNode.value += valueNode

def movementChoiceFunction(treeNodes):
    bestChildVisits = -1
    bestChild = None

    for child in treeNodes.childs:
        if child.visits > bestChildVisits:
            bestChildVisits = child.visits
            bestChild = child

    return bestChild

def infinity_distance(x_position, y_position):
    return  max(abs(x_position[0] - y_position[0]), abs(x_position[1] - y_position[1])) # distancia infinito

