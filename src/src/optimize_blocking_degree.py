#%%

from Initializer import create_simple_board, init_simulation

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

# #Main program
# from Functions_blocking_degree import getBlockingDegreeJiang as gbdJiang

# board = create_simple_board(4, 4)
# containers_to_extract_id = [15, 2, 10, 5, 30, 1, 20]
# containers_to_extract_id_dict = {
#     15: (1, 1),
#     2: (0, 0),
#     10: (0, 3),
#     5: (0, 1),
#     30: (2, 2),
#     1: (0, 0),
#     20: (1, 2)}

# #%%
# %%timeit

# result = getBlockingDegreeJiang(board, containers_to_extract_id_dict)
# #%%
# %%timeit
# result2 = gbdJiang(board, containers_to_extract_id)
# #%%

# result = getBlockingDegreeJiang(board, containers_to_extract_id_dict)
# print("HOLA", result)
# # %%
