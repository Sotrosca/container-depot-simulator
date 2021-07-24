import random
from SimpleSimulation import ActionType, Simulation
import Utils

class NaturalNumbersIterator():
    def __iter__(self):
      self.a = 0
      return self

    def __next__(self):
      x = self.a
      self.a += 1
      return x

class MontecarloPlayer():

    def __init__(self, originalSimulation, selectionFunction, expansionFunction, retropropagationFunction, simulationFunction, movementChoiceFunction):
        self.idsNodes = iter(NaturalNumbersIterator())
        self.originalSimulation = Utils.copySimulation(originalSimulation)
        self.actionTree = Node(None, [], None, Utils.copySimulation(self.originalSimulation), 0, 0)
        self.actionTreeDepth = 0
        self.initTreeNodes()
        self.selectionFunction = selectionFunction
        self.expansionFunction = expansionFunction
        self.simulationFunction = simulationFunction
        self.retropropagationFunction = retropropagationFunction
        self.movementChoiceFunction = movementChoiceFunction

    def initTreeNodes(self):
        self.expand_node(self.actionTree)

    def getChildById(self, idChild):
        for child in self.actionTree.childs:
            if child.id == idChild:
                return child
        return None

    def getChildById(self, idChild, parent):
        for child in parent.childs:
            if child.id == idChild:
                return child
        return None

    def exploreActionTree(self, epochs = 1000, log=True):
        for epoch in range(epochs):
            if log and epoch % 100 == 0:
                print(epoch)
            actionNode = self.selectionFunction(self.actionTree)
            if (self.expansionFunction(actionNode)):
                self.expand_node(actionNode)
                actionNode = self.selectionFunction(actionNode)

            simulationFinished = self.simulationFunction(actionNode)
            self.retropropagationFunction(self.originalSimulation, simulationFinished, actionNode)
            del simulationFinished

    def getBestMove(self):

        bestMove = self.movementChoiceFunction(self.actionTree)

        return bestMove

    def setActionTreeDepth(self, level):
        if level > self.actionTreeDepth:
            self.actionTreeDepth = level

    def getBestMoveSequence(self):

        moveSequence = []

        node = self.actionTree

        while node.hasChilds():
            bestChild = self.movementChoiceFunction(node)
            moveSequence.append(bestChild)
            node = bestChild

        return moveSequence


    # FUNCION DE EXPANSION
    def expand_node(self, actionNode):
        newLevel = actionNode.level + 1

        blocking_degree_action_dict = self.get_actions_child_ordered_by_value(actionNode)

        if not actionNode.hasChilds() and len(blocking_degree_action_dict) > 0: #FORZAR EXTRACT
            best_actions = blocking_degree_action_dict.get(min(blocking_degree_action_dict))
            #keys_dict = list(blocking_degree_action_dict.keys())
            #keys_dict.sort()
            #best_actions = blocking_degree_action_dict.get(keys_dict[0])
            #second_best_actions = blocking_degree_action_dict.get(keys_dict[1])
            len_best_actions = len(best_actions)
#            percentage = 0.5
#            quantity = int(percentage * len_best_actions)
#            quantity = quantity if quantity > 0 else 1
#            quantity = 8 if len_best_actions > 8 else len_best_actions
#            choices = random.sample(blocking_degree_action_dict.get(min(blocking_degree_action_dict)), k=quantity)
            choices = best_actions
            for action in choices:
                _simulation = Utils.copySimulation(actionNode.simulationCopy)
                _simulation.run_one_epoch(action)
                actionNode.childs.append(Node(actionNode, [], action, _simulation, self.idsNodes.__next__(), newLevel))
        self.setActionTreeDepth(newLevel)

    def get_actions_child_ordered_by_value(self, actionNode):
        newLevel = actionNode.level + 1
        
        simulationCopy = Utils.copySimulation(actionNode.simulationCopy)

        posibleActions = simulationCopy.get_possible_actions()

        blocking_degree_action_dict = {}

        blocking_degree_init = simulationCopy.blocking_degree
        crane_position_init = simulationCopy.crane_position
        for action in posibleActions:
            if action.type == ActionType.EXTRACT or action.type == ActionType.END:
                _simulation = Utils.copySimulation(actionNode.simulationCopy)
                _simulation.run_one_epoch(action)
                actionNode.childs.append(Node(actionNode, [], action, _simulation, self.idsNodes.__next__(), newLevel))
            else:

                time_init = simulationCopy.time
                is_action_valid = simulationCopy.run_one_epoch(action)
                if is_action_valid:
                    time_finish = simulationCopy.time
                    blocking_degree_finish = simulationCopy.blocking_degree
                    time_total = time_finish - time_init
                    blocking_degree_total = blocking_degree_finish - blocking_degree_init
                    key = blocking_degree_total / time_total
                    if key in blocking_degree_action_dict:
                        blocking_degree_action_dict.get(key).append(action)
                    else:
                        blocking_degree_action_dict[key] = [action]
                    simulationCopy.execute_inverse_move(action)
                    simulationCopy.crane_position = crane_position_init

        return blocking_degree_action_dict
    #FIN FUNCION DE EXPANSION

class Node():
    def __init__(self, parent, childs, action, simulationCopy, idNode, level):
        self.parent = parent #Node
        self.childs = childs #Node[]
        self.action = action # Accion realizada para llegar al estado representado en simulationCopy
        self.simulationCopy = simulationCopy # Estado de la simulacion con la action ya realizada
        self.visits = 0
        self.value = 0
        self.id = idNode
        self.level = level

    def __str__(self):
        return "Id: " + str(self.id) + " - " + "visits: " + str(self.visits) + " - " + "value: " + str(self.value)

    def hasChilds(self):
        return self.childs != None and len(self.childs) > 0

    def getChildsWithoutVisits(self):
        childsWithoutLove = []

        for child in self.childs:
            if child.visits == 0:
                childsWithoutLove.append(child)

        return childsWithoutLove

    def hasParent(self):
        return self.parent != None


