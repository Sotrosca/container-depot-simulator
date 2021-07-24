import random
import numpy as np
import copy

def selectionFunction(treeNodes):
    UCTConstant = 0.1
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



def selectionFunctionBlockingDegree(treeNodes):

    selectedNode = treeNodes

    while selectedNode.hasChilds():
        maxBlockingDegree = -1000000
        for child in selectedNode.childs: #Recorro cada hijo para ver su Blocking Degree
            blockingDegree = getBlockingDegree(child.simulationCopy.board)
            if blockingDegree > maxBlockingDegree:
                selectedNode = child
                maxBlockingDegree = blockingDegree

    return selectedNode



def expansionFunction(node):
    return node.visits > 0

def simulationFunction(actionNode):
    # Simulacion random (ver de utilizar otra)
    _simulationCopy = copy.deepcopy(actionNode.simulationCopy)
    while not _simulationCopy.is_simulation_end():
        possibleActions = _simulationCopy.get_possible_actions()
        action = None
        for _action in possibleActions:
            if _action.type.name == "EXTRACT":
                action = _action
        if action == None:
            action = random.choice(possibleActions)
        _simulationCopy.run_one_epoch(action)

    return _simulationCopy

def simulationFunctionDummy(actionNode):
    return actionNode.simulationCopy

def retropropagationFunction(originalSimulation, simulationFinished, actionNode):

    #valueNode = 1 / simulationFinished.time # Mejorar
    valueNode = 1.0 / abs(getBlockingDegree(simulationFinished.board))

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

def getBlockingDegree(board):
    width = board.width
    height = board.height

    blocking_degree = [[0 for j in range(width)] for i in range(height)]
    total_blocking_degree = 0

    for i in range(height):
        for j in range(width):

            cell_list = list(x.id for x in board.cell_matrix[i][j].container_list)
            
            while len(cell_list) > 1: #Si la pila tiene un solo elemento (o ninguno), el blocking degree es 0 

                min_index = cell_list.index(min(cell_list))

                upper_list = cell_list[:min_index+1]
                cell_list = cell_list[min_index+1:]

                # if len(upper_list > 1): #Si la lista superior solo tiene al elemento divisor, entonces el blocking degree es 0
                #Calculo el blocking degree de la parte superior
                for k in range(len(upper_list)-1):
                    blocking_degree[i][j] += upper_list[-1] - upper_list[k]

            total_blocking_degree += blocking_degree[i][j]

    return total_blocking_degree - 1
