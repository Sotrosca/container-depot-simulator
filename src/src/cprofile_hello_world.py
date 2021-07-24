import cProfile, pstats

def loop():
    for i in range(10000):
        print(i)

profiler = cProfile.Profile()
profiler.enable()
loop()
profiler.disable()

stats = pstats.Stats(profiler)

#stats.dump_stats('C:/Users/fserna/Documents/42/Trabajo/CONTOPSA/container-depot-simulator/src/reports/data')

stats.strip_dirs()
stats.print_stats()
stats.print_callers()
stats.print_callees()

#%%

import ujson
from Initializer import init_simulation, create_random_board
from Functions_blocking_degree import get_all_move_actions


board = create_random_board(3, 3)
move_actions = get_all_move_actions(board)

simulation = init_simulation((0, 0), board, 0, infinity_distance, [10, 2, 15, 5], move_actions)

ujson.loads(ujson.dumps(board.__dict__))

#%%
import _pickle as cPickle
from Initializer import init_simulation, create_random_board
from Functions_blocking_degree import get_all_move_actions

board = create_random_board(3, 3)
move_actions = get_all_move_actions(board)

simulation = init_simulation((0, 0), board, 0, infinity_distance, [10, 2, 15, 5], move_actions)

profiler = cProfile.Profile()
profiler.enable()
for i in range(10000):
    cPickle.loads(cPickle.dumps(simulation, -1))
profiler.disable()

stats = pstats.Stats(profiler).strip_dirs()

stats.sort_stats('tottime').print_stats()

#%%

import pickle as pickle
from Initializer import init_simulation, create_random_board
from Functions_blocking_degree import get_all_move_actions

board = create_random_board(3, 3)
move_actions = get_all_move_actions(board)

simulation = init_simulation((0, 0), board, 0, infinity_distance, [10, 2, 15, 5], move_actions)

profiler = cProfile.Profile()
profiler.enable()
for i in range(10000):
    pickle.loads(pickle.dumps(simulation, -1))
profiler.disable()

stats = pstats.Stats(profiler).strip_dirs()

stats.sort_stats('tottime').print_stats()

#%%

import copy
from Initializer import init_simulation, create_random_board
from Functions_blocking_degree import get_all_move_actions

board = create_random_board(3, 3)
move_actions = get_all_move_actions(board)

simulation = init_simulation((0, 0), board, 0, infinity_distance, [10, 2, 15, 5], move_actions)

profiler = cProfile.Profile()
profiler.enable()
for i in range(10000):
    copy.deepcopy(simulation)
profiler.disable()

stats = pstats.Stats(profiler).strip_dirs()

stats.sort_stats('tottime').print_stats()
#%%
stats = pstats.Stats(profiler).strip_dirs()
#%% TIME
stats.sort_stats('tottime').print_stats()