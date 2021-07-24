from enum import Enum


class Container():
    def __init__(self, container_id, container_type):
        self.id = container_id
        self.type = container_type

class Crane():
    def __init__(self, position_x, position_y, reach):
        self.x = position_x
        self.y = position_y
        self.reach = reach

    def get_position(self):
        return (self.x, self.y)

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def can_reach_container(self, cell, container):
        return self.reach <= max(abs(self.x - cell.x), abs(self.y - cell.y))


class CellType(Enum):
    BLOCK = 1 # permite containers, la grua puede moverse por aca si no hay bloques
    FLOOR = 2 # no permite containers, si puede pasar la grua
    DISABLED = 3 # no se puede acceder a esta celda


class Cell():
    def __init__(self, position_x, position_y, container_list, cell_type):
        self.x = position_x
        self.y = position_y
        self.container_list = container_list
        self.container_id_list = self.get_container_id_list()
        self.cell_type = cell_type

    def __str__(self):
        return str(self.get_position())

    def get_position(self):
        return (self.x, self.y)

    def is_not_empty(self):
        return len(self.container_list) > 0

    def get_top_container_id(self):
        return self.container_list[0].id if self.is_not_empty() else -1

    def container_quantity(self):
        return len(self.container_list)

    def has_container(self, container_id):
        return container_id in self.container_id_list

    def get_container_id_list(self):
        return list(map(lambda container: container.id, self.container_list))

    def find_container_level(self, container_id):
        if self.has_container(container_id):
            return self.container_id_list.index(container_id)
        else:
            return -1

    def find_containers(self, container_id_list):
        containers = []

        for i, container_id in enumerate(self.container_id_list):
            if container_id in container_id_list:
                containers.append(container_id)

        return containers


class Board():
    def __init__(self, height, width, cell_matrix):
        self.height = height
        self.width = width
        self.cell_matrix = cell_matrix
        self.container_map = self.build_container_map()

    def build_container_map(self):
        container_map = {}
        for i in range(self.width):
            for j in range(self.height):
                cell = self.cell_matrix[i][j]
                for container in cell.container_list:
                    container_map[container.id] = container
        return container_map

    def get_board_top_view(self):
        board = []
        for i in range(self.width):
            row = []
            for j in range(self.height):
                row.append(self.cell_matrix[i][j].get_top_container_id())
            board.append(row)
        return board

    def find_container_by_id(self, container_id):
        for i in range(self.width):
            for j in range(self.height):
                cell = self.cell_matrix[i][j]
                container_level = cell.find_container_level(container_id)
                if container_level != -1:
                    return (cell.x, cell.y, container_level)
        return -1

    def find_container_list_by_id(self, container_id_list):
        container_dict = {}

        for i in range(self.width):
            for j in range(self.height):
                cell = self.cell_matrix[i][j]
                containers = cell.find_containers(container_id_list)
                for container_id in containers:
                    container_dict[container_id] = (cell.x, cell.y)

        return container_dict

    def get_board_row_view(self, row_index):
        row = []

        for j in range(self.height):
            cell = self.cell_matrix[row_index][j]
            row.append(cell.get_container_id_list())

        return row

