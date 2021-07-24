import Entities
from enum import Enum

class ActionType(Enum):
    TAKE = 1
    DISPATCH = 2
    MOVE = 3


class Action():
    def __init__(self, action_type, time_cost, target_cell):
        self.type = action_type
        self.time_cost = time_cost
        self.target_cell = target_cell

class Simulation():
    def __init__(self, crane, board, time):
        self.crane = crane
        self.board = board
        self.time = time


    def take_container(self, container_x, container_y):
        cell = self.board[container_x]