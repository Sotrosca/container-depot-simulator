from Initializer import create_custom_board2

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
    

    return total_blocking_degree

board = create_custom_board2() # Escenario creado a mano

print(board.print_board())

print(getBlockingDegree(board))