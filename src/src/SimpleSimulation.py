from enum import Enum

class ActionType(Enum):
    MOVE = 1
    EXTRACT = 2
    END = 3

class Action():
    def __init__(self, source_cell, target_cell, action_type):
        self.source_cell = source_cell
        self.target_cell = target_cell
        self.type = action_type

    def __str__(self):
        if self.type == ActionType.MOVE:
            return str((self.source_cell.get_position(), self.target_cell.get_position(), self.type))
        elif self.type == ActionType.EXTRACT:
            return str((self.source_cell.get_position(), self.type))
        elif self.type == ActionType.END:
            return "Simulation is end"


class Simulation():
    def __init__(self, crane_position, board, time, distance_function, containers_to_extract_id, move_actions):
        self.crane_position = crane_position
        self.board = board
        self.time = time
        self.distance_function = distance_function
        self.epochs = 0
        self.containers_to_extract_id = containers_to_extract_id
        self.containers_to_extract_position_dict = self.init_containers_to_extract_position_dict(containers_to_extract_id)
        self.blocking_degree = self.calculate_blocking_degree()
        self.history = {}
        self.move_actions = move_actions
        self.move_actions_dict_by_source = self.build_move_actions_dict_by_source(move_actions)


    def init_containers_to_extract_position_dict(self, containers_to_extract_id):
        return self.board.find_container_list_by_id(containers_to_extract_id)

    def build_move_actions_dict_by_source(self, move_actions):
        move_actions_dict_by_source = {}

        for action in move_actions:
            if action.source_cell.get_position() in move_actions_dict_by_source:
                move_actions_dict_by_source.get(action.source_cell.get_position()).append(action)
            else:
                move_actions_dict_by_source[action.source_cell.get_position()] = [action]
        return move_actions_dict_by_source

    def move_container(self, source_cell, target_cell):
        container = source_cell.container_list.pop(0)
        source_cell.container_id_list.pop(0)
        target_cell.container_list.insert(0, container)
        target_cell.container_id_list.insert(0, container.id)

        if container.id in self.containers_to_extract_id:
            self.containers_to_extract_position_dict[container.id] = target_cell.get_position()

        self.crane_position = target_cell.get_position()

    def extract_container(self, source_cell):
        container = source_cell.container_list[0]
        if not container.id in self.containers_to_extract_id:
            print("Error container: " + str(container.id))
        else:
            source_cell.container_list.pop(0)
            source_cell.container_id_list.pop(0)
            self.containers_to_extract_id.remove(container.id)
            del self.containers_to_extract_position_dict[container.id]
            self.crane_position = source_cell.get_position()

    def run_one_epoch(self, action):
        if self.is_invalid_action(action):
            self.blocking_degree = 10000000
            return False
        else:
            self.execute_action(action)
            self.history[self.epochs] = action
            self.blocking_degree = self.calculate_blocking_degree()
            return True

    def is_invalid_action(self, action):
        return action.type == ActionType.MOVE and not self.get_cell(action.source_cell.x, action.source_cell.y).container_list

    def execute_action(self, action):
        action_cost = 0
        if action.type == ActionType.MOVE:
            source_cell = self.get_cell(action.source_cell.x, action.source_cell.y)
            target_cell = self.get_cell(action.target_cell.x, action.target_cell.y)
            action_cost = self.calculate_move_cost(source_cell, target_cell)
            self.move_container(source_cell, target_cell)
        elif action.type == ActionType.EXTRACT:
            source_cell = self.get_cell(action.source_cell.x, action.source_cell.y)
            action_cost = self.calculate_extract_cost(source_cell)
            self.extract_container(source_cell)

        self.time += action_cost
        self.epochs += 1


    # Funciones de calculo de coste
    def calculate_move_cost(self, source_cell, target_cell):
        distance_crane_to_source = self.distance_function(self.crane_position, source_cell.get_position())
        distance_source_to_target = self.distance_function(source_cell.get_position(), target_cell.get_position())
        return distance_crane_to_source + distance_source_to_target

    def calculate_extract_cost(self, source_cell):
        distance_crane_to_source = self.distance_function(self.crane_position, source_cell.get_position())
        return distance_crane_to_source + 1


    '''
    def get_possible_actions(self):
        actions = []

        if self.is_simulation_end():
            actions.append(Action(None, None, ActionType.END))
            return actions
        else:
            for i in range(self.board.width):
                for j in range(self.board.height):
                    cell = self.board.cell_matrix[i][j]
                    if cell.is_not_empty():
                        if cell.container_list[0].id == self.containers_to_extract_id[0]:
                            actions.append(Action(cell, None, ActionType.EXTRACT))

            actions.extend(self.move_actions)
        return actions

    def get_all_move_actions_from_cell(self, source_cell):

        actions = [Action(source_cell, self.board.cell_matrix[i][j], ActionType.MOVE) for i in range(self.board.width) for j in range(self.board.height) if source_cell.x != i or source_cell.y != j]

        return actions
    '''

    def get_possible_actions(self):
        actions = []

        if self.is_simulation_end():
            actions.append(Action(None, None, ActionType.END))
            return actions
        else:
            for i in range(self.board.width):
                for j in range(self.board.height):
                    cell = self.board.cell_matrix[i][j]
                    if cell.is_not_empty():
                        if cell.container_list[0].id == self.containers_to_extract_id[0]:
                            actions.append(Action(cell, None, ActionType.EXTRACT))

            important_cells = set(self.containers_to_extract_position_dict.values())

            for cell in important_cells:
                actions.extend(self.move_actions_dict_by_source.get(cell))
            '''
            for action in self.move_actions:
                if action.source_cell.get_position() in important_cells:
                    actions.append(action)
            '''
        return actions

    def get_all_move_actions_from_cell(self, source_cell):
        actions = [Action(source_cell, self.board.cell_matrix[i][j], ActionType.MOVE) for i in range(self.board.width) for j in range(self.board.height) if source_cell.x != i or source_cell.y != j]
        return actions

    def get_cell(self, x, y):
        return self.board.cell_matrix[x][y]

    def is_simulation_end(self):
        return len(self.containers_to_extract_id) == 0


    def calculate_blocking_degree(self):
        blocking_degree = 1

        containers_level_by_cell_dict = {}


        for i, container_id in enumerate(reversed(self.containers_to_extract_id)):
            container_position = self.containers_to_extract_position_dict.get(container_id)
            container_level = self.board.cell_matrix[container_position[0]][container_position[1]].find_container_level(container_id)
            
            if container_position in containers_level_by_cell_dict:
                containers_level_by_cell_dict.get(container_position).append(container_level * (i + 1))
            else:
                containers_level_by_cell_dict[container_position] = [container_level * (i + 1)]

        for containers_level in containers_level_by_cell_dict.values():
            blocking_degree += max(containers_level) + 1

        return blocking_degree
    
    '''
    def calculate_blocking_degree(self):
        #from Functions_blocking_degree import getBlockingDegreeJiangOld
        from Functions_blocking_degree import getBlockingDegreeJiang
        
        #return getBlockingDegreeJiang(self.board, self.containers_to_extract_id)
        return getBlockingDegreeJiang(self.board, self.containers_to_extract_position_dict)
    '''

    def execute_inverse_move(self, action):
        source_cell = self.get_cell(action.target_cell.x, action.target_cell.y)
        target_cell = self.get_cell(action.source_cell.x, action.source_cell.y)
        self.move_container(source_cell, target_cell)

    #CORREGIR
    def get_containers_to_extract_position_dict(self, containers_to_extract_id):
        containers_to_extract_position_dict = {}
        for container_id in containers_to_extract_id:
            containers_to_extract_position_dict[container_id] = self.board.find_container_by_id(container_id)
        return containers_to_extract_position_dict
