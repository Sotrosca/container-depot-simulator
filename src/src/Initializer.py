from Entities import Cell, CellType, Container, Board
from SimpleSimulation import Simulation
import random

def create_random_board(width, height):
    id_container = 0
    cell_matrix = []
    for i in range(width):
        row = []
        for j in range(height):
            containers_quantity = random.randint(0, 5)
            container_list = []
            for k in range(containers_quantity):
                container_list.append(Container(id_container, None))
                id_container += 1
            row.append(Cell(i, j, container_list, CellType.BLOCK))
        cell_matrix.append(row)

    board = Board(height, width, cell_matrix)
    return board


    return cell_matrix

def create_custom_board():
    cell_matrix = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append(Cell(i, j, [], CellType.BLOCK))
        cell_matrix.append(row)

    cell_matrix[0][1].container_list.append(Container(1, None))
    cell_matrix[0][1].container_list.append(Container(2, None))
    cell_matrix[0][0].container_list.append(Container(3, None))
    cell_matrix[0][0].container_list.append(Container(4, None))
    cell_matrix[0][2].container_list.append(Container(5, None))
    cell_matrix[1][0].container_list.append(Container(6, None))
    cell_matrix[1][1].container_list.append(Container(7, None))
    cell_matrix[1][2].container_list.append(Container(8, None))
    cell_matrix[2][0].container_list.append(Container(9, None))
    cell_matrix[2][1].container_list.append(Container(10, None))
    cell_matrix[2][2].container_list.append(Container(11, None))

    board = Board(3, 3, cell_matrix)

    return board

def create_simple_board(width, height):
    id_container = 0
    cell_matrix = []
    for i in range(width):
        row = []
        for j in range(height):
            containers_quantity = 5
            container_list = []
            for k in range(containers_quantity):
                container_list.append(Container(id_container, None))
                id_container += 1
            row.append(Cell(i, j, container_list, CellType.BLOCK))
        cell_matrix.append(row)

    board = Board(height, width, cell_matrix)
    return board

def init_simulation(crane_position, board, time, distance_function, containers_to_extract_id, move_actions):
    return Simulation(crane_position, board, time, distance_function, containers_to_extract_id, move_actions)
