#Sudoku solver using BACKTRACKING ALGORITHM

puzzle = [[5,3,0,0,7,0,0,0,0],
          [6,0,0,1,9,5,0,0,0],
          [0,9,8,0,0,0,0,6,0],
          [8,0,0,0,6,0,0,0,3],
          [4,0,0,8,0,3,0,0,1],
          [7,0,0,0,2,0,0,0,6],
          [0,6,0,0,0,0,2,8,0],
          [0,0,0,4,1,9,0,0,5],
          [0,0,0,0,8,0,0,7,9]]

def show_board(puzzle):
    for i in range(len(puzzle)):
        if i % 3 == 0 and i != 0:
            print ("---------------------")

        for j in range(len(puzzle[0])):
            if j % 3 == 0 and j != 0:
                print ("|", end=" ")
                print (puzzle[i][j], end=" ")
            elif j == 8:
                print (puzzle[i][j])
            else:
                print (puzzle[i][j], end=" ")


def find_empty(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            if puzzle[i][j] == 0:
                return (i,j)
    return None


def valid(puzzle, num, pos):
    #checking row
    for i in range(len(puzzle[0])):
        if puzzle[pos[0]][i] == num and pos[1] != i:
            return False
    #checking column
    for i in range(len(puzzle)):
        if puzzle[i][pos[1]] == num and pos[0] != i:
            return False

    #checking box
    x_box = pos[1] // 3
    y_box = pos[0] // 3

    for i in range(y_box*3,y_box*3 + 3):
        for j in range(x_box*3,x_box*3 + 3):
            if puzzle[i][j] == num and (i,j) != pos:
                return False

    return True


def solve(puzzle):

    find = find_empty(puzzle)
    if not find:
        return True
    else:
        row,col = find

    for i in range(1,10):
        if valid(puzzle, i, (row,col)):
            puzzle[row][col] = i

            if solve(puzzle):
                return True

            puzzle[row][col] = 0

    return False

print(solve(puzzle))
show_board(puzzle)
