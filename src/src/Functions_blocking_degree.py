import random
import numpy as np
from SimpleSimulation import Action, ActionType
import Utils

def selectionFunction(treeNodes):
    UCTConstant = 0.0000001
    selectedNode = treeNodes

    while selectedNode.hasChilds():

        selectionValueUCT = -1
        winnerNode = None

#        best_childs = select_best_childs_by_blocking_degree(selectedNode)
        best_childs = selectedNode.childs
        best_childs_without_love = list(filter(lambda x: x.visits == 0, best_childs))

        if len(best_childs_without_love) > 0:
            selectedNode = random.choice(best_childs_without_love)
#            init_node_simulation(selectedNode)

        else:
            for child in best_childs:
                childSuccessRatio = (child.value + 1) / (child.visits + 1)

                logRatio = (np.log(selectedNode.visits) / child.visits) ** 0.5

                childValueUCT = childSuccessRatio + UCTConstant * logRatio

                if childValueUCT > selectionValueUCT:
                    selectionValueUCT = childValueUCT
                    winnerNode = child

            selectedNode = winnerNode

    return selectedNode

def selectionFunctionJiang(treeNodes):
    UCTConstant = 0.0000000001
    selectedNode = treeNodes

    while selectedNode.hasChilds():

# Recorro todos los hijos y les calculo del blocking degree, ordenándolos de mayor a menor
            
        best_childs = select_best_childs_by_blocking_degree_Jiang(selectedNode)
#         best_childs = selectedNode.childs
#         best_childs_without_love = list(filter(lambda x: x.visits == 0, best_childs))

#         if len(best_childs_without_love) > 0:
#             selectedNode = random.choice(best_childs_without_love)
# #            init_node_simulation(selectedNode)

#         else:
#             for child in best_childs:
#                 childSuccessRatio = (child.value + 1) / (child.visits + 1)

#                 logRatio = (np.log(selectedNode.visits) / child.visits) ** 0.5

#                 childValueUCT = childSuccessRatio + UCTConstant * logRatio

#                 if childValueUCT > selectionValueUCT:
#                     selectionValueUCT = childValueUCT
#                     winnerNode = child

#             selectedNode = winnerNode

    return selectedNode

def select_best_childs_by_blocking_degree_Jiang(parent_node):
    blocking_degree_childs_dict = {}
    for child in parent_node.childs:
        child_blocking_degree = child.simulationCopy.blocking_degree
        if child_blocking_degree in blocking_degree_childs_dict:
            blocking_degree_childs_dict.get(child_blocking_degree).append(child)
        else:
            blocking_degree_childs_dict[child_blocking_degree] = [child]

    best_blocking_degree_value = min(blocking_degree_childs_dict.keys())

    return blocking_degree_childs_dict[best_blocking_degree_value]



def select_best_childs_by_blocking_degree(parent_node):
    blocking_degree_childs_dict = {}
    for child in parent_node.childs:
        child_blocking_degree = child.simulationCopy.blocking_degree
        if child_blocking_degree in blocking_degree_childs_dict:
            blocking_degree_childs_dict.get(child_blocking_degree).append(child)
        else:
            blocking_degree_childs_dict[child_blocking_degree] = [child]

    best_blocking_degree_value = min(blocking_degree_childs_dict.keys())

    return blocking_degree_childs_dict[best_blocking_degree_value]


def expansionFunction(node):

    return node.visits > 2 or len(node.childs) == 1

def simulationFunction(actionNode):
    # Simulacion random (ver de utilizar otra)

    _simulationCopy = Utils.copySimulation(actionNode.simulationCopy)
    i = 1

    while not _simulationCopy.is_simulation_end():

        possibleActions = _simulationCopy.get_possible_actions()
        action = None
        for _action in possibleActions:
            if _action.type == ActionType.EXTRACT:
                action = _action
        if action == None:
            action = random.choice(possibleActions)
        _simulationCopy.run_one_epoch(action)
        i += 1

    return _simulationCopy

def simulationFunctionDummy(actionNode):

    return actionNode.simulationCopy

def retropropagationFunction(originalSimulation, simulationFinished, actionNode):
    #valueNode = 1 / simulationFinished.time # Mejorar
    #valueNode = 1.0 / (abs(simulationFinished.blocking_degree) * simulationFinished.time)
    original_containers_to_extract_id = len(originalSimulation.containers_to_extract_id)
    containers_to_extract_id = len(simulationFinished.containers_to_extract_id)

    containers_extracted = (original_containers_to_extract_id - containers_to_extract_id) / original_containers_to_extract_id if original_containers_to_extract_id != 0 else 100

#    valueNode = (simulationFinished.epochs * containers_extracted**2) / (simulationFinished.epochs * simulationFinished.blocking_degree + simulationFinished.time)
    
    delta_blocking_degree = originalSimulation.blocking_degree - simulationFinished.blocking_degree
    
    valueNode = containers_extracted * delta_blocking_degree / simulationFinished.time

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

def manhattan_distance(x_position, y_position):
    return  abs(x_position[0] - y_position[0]) + abs(x_position[1] - y_position[1]) # distancia infinito
    
def square_euclidian_distance(x_position, y_position):
    return  (x_position[0] - y_position[0]) ** 2 + (x_position[1] - y_position[1]) ** 2 # distancia euclidea

def euclidian_distance(x_position, y_position):
    return  ((x_position[0] - y_position[0]) ** 2 + (x_position[1] - y_position[1]) ** 2) ** (1/2) # distancia euclidea


def manhattan_distance(x_position, y_position):
    return  abs(x_position[0] - y_position[0]) + abs(x_position[1] - y_position[1]) # distancia manhattan

def get_actions_to_node(childNode):

    current_node = childNode
    actions = []

    while current_node.hasParent():
        actions.insert(0, childNode.parent.action)
        current_node = childNode.parent

    return (current_node, actions[1:])

def init_node_simulation(node):
    root_node_and_actions = get_actions_to_node(node)
    root_node, actions_to_node = root_node_and_actions[0], root_node_and_actions[1]
    _simulation_copy = Utils.copySimulation(root_node.simulationCopy)

    for action in actions_to_node:
        _simulation_copy.run_one_epoch(action)

    node.simulationCopy = _simulation_copy

def calculateBlockingDegree(simulation):

    blocking_degree = 1

    containers_level_by_cell_dict = {}

    for container_id in simulation.containers_to_extract_id:
        container_position = simulation.board.find_container_by_id(container_id)
        if container_position[0:2] in containers_level_by_cell_dict:
            containers_level_by_cell_dict.get(container_position[0:2]).append(container_position[2])
        else:
            containers_level_by_cell_dict[container_position[0:2]] = [container_position[2]]

    for containers_level in containers_level_by_cell_dict.values():
        blocking_degree += max(containers_level) + 1

    return blocking_degree

def get_all_move_actions(board):
    actions = []
    for i in range(board.width):
        for j in range(board.height):
            source_cell = board.cell_matrix[i][j]
            cell_move_actions = [Action(source_cell, board.cell_matrix[k][l], ActionType.MOVE) for k in range(board.width) for l in range(board.height) if source_cell.x != k or source_cell.y != l]
            actions.extend(cell_move_actions)

    return actions

# def getBlockingDegreeJiangOld(board, extract_list):
#     width = board.width
#     height = board.height

#     blocking_degree = [[0 for j in range(width)] for i in range(height)]
#     total_blocking_degree = 0

#     priorityBoard = getPriorityBoardOld(board, extract_list)

#     for i in range(height):
#        for j in range(width):

#             #cell_list = list(x.id for x in board.cell_matrix[i][j].container_list)
#             cell_list = priorityBoard[i][j]
            
#             while len(cell_list) > 1: #Si la pila tiene un solo elemento (o ninguno), el blocking degree es 0 

#                 min_index = cell_list.index(min(cell_list))

#                 upper_list = cell_list[:min_index+1]
#                 cell_list = cell_list[min_index+1:]

#                 # if len(upper_list > 1): #Si la lista superior solo tiene al elemento divisor, entonces el blocking degree es 0
#                 #Calculo el blocking degree de la parte superior
#                 for k in range(len(upper_list)-1):
#                     blocking_degree[i][j] += upper_list[-1] - upper_list[k]

#             total_blocking_degree += blocking_degree[i][j]

#     return abs(total_blocking_degree - 1)


# def getPriorityBoardOld(board, extract_list):
#     width = board.width
#     height = board.height

#     #Los contenedores a extraer tienen prioridad según el orden en la lista extract_List
#     #(es decir, si en la lista son N elementos, las prioridades irán de 0 a N-1)
#     #Todos los contenedores que no hay que extraer tendrán prioridad N
#     minPriority = len(extract_list) + 1

#     #Si no hay contenedor en una celda, la prioridad es 0
#     priorityBoard = [[[] for j in range(width)] for i in range(height)]
    
#     for i in range(height):
#         for j in range(width):
#             stack = list(x.id for x in board.cell_matrix[i][j].container_list)
#             for k in range(len(stack)):
#                 if stack[k] in extract_list:
#                     priority = extract_list.index(stack[k]) + 1
#                 else:
#                     priority = minPriority
            
#                 priorityBoard[i][j].append(priority)

#     return priorityBoard


def uniqueCoordinatesList(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def getBlockingDegreeJiang(generalboard, extract_dict):
    
    extract_list = list(extract_dict.keys())

    stacks_with_containers_to_extract = uniqueCoordinatesList(extract_dict.values())
    number_of_stacks_with_containers_to_extract = len(stacks_with_containers_to_extract)
    
    blocking_degree = [0 for i in range(number_of_stacks_with_containers_to_extract)]
    total_blocking_degree = 0

    priorityBoard = getPriorityBoard(generalboard, extract_list, stacks_with_containers_to_extract)
#------------------------

    for i in range(len(priorityBoard)):
        stack = priorityBoard[i]

        while len(stack) > 0:
            min_index = stack.index(min(stack))
            
            upper_stack = stack[:min_index+1]
            stack = stack[min_index+1:]

            for k in range(len(upper_stack)-1):
                blocking_degree[i] += upper_stack[-1] - upper_stack[k]
        
        total_blocking_degree += blocking_degree[i]


    return abs(total_blocking_degree - 1)


def getPriorityBoard(board, extract_list, stacks_coordinates):

    stacks_length = len(stacks_coordinates)

    #Los contenedores a extraer tienen prioridad según el orden en la lista extract_List
    #(es decir, si en la lista son N elementos, las prioridades irán de 0 a N-1)
    #Todos los contenedores que no hay que extraer tendrán prioridad N
    minPriority = len(extract_list) + 1

    #Si no hay contenedor en una celda, la prioridad es 0
    #priorityBoard = [[[] for j in range(width)] for i in range(height)]
    priorityBoard = [[] for i in range(stacks_length)]
    
    for i in range(stacks_length):
        stack_pos = stacks_coordinates[i]
        
        x = stack_pos[0]
        y = stack_pos[1]

        stack = list(z.id for z in board.cell_matrix[x][y].container_list)

        for k in range(len(stack)):
            if stack[k] in extract_list:
                priority = extract_list.index(stack[k]) + 1
            else:
                priority = minPriority

            priorityBoard[i].append(priority)

    return priorityBoard


    #for container_id in extract_list:
    #    x, y, level = board.find_container_by_id(container_id)
