# $ -- Queen
# ! -- visited
# 0 -- path
import sys
def canPlace(board,n,current_col,current_row):
    for j in range(0,current_col): # block right , left
        if board[current_row][j] == '$':
            return False
    
    diagonal_i  = current_row
    diagonal_j  = current_col 
    
    while True: # block diagonal down
        if diagonal_i >= n or diagonal_j < 0:
            break
        if board[diagonal_i][diagonal_j] == '$':
            return False
        diagonal_i +=1
        diagonal_j -=1
    
    diagonal_i  = current_row - 1
    diagonal_j  = current_col - 1
    
    while True: # block diagonal up
        if diagonal_i < 0 or diagonal_j < 0:
            break
        if board[diagonal_i][diagonal_j] == '$':
            return False
        diagonal_i -=1
        diagonal_j -=1
    return True

def nQueen(board,n,current_col):
    if current_col >= n:
        return True
    for i in range(0,n):
        if board[i][current_col] == '0':
            if canPlace(board,n,current_col,i):
                board[i][current_col] = '$'
                if nQueen(board,n,current_col+1):
                    return True
                board[i][current_col] = '0'
    return False

def display(board,n):
    for i in range(0,n):
        for j in range(0,n):
            print(board[i][j],end="    ")
        print()

if __name__ == "__main__":
    n = int(input('N : '))
    board = [['0' for i in range(n)] for j in range(n)]
    
    if nQueen(board,n,0):
        display(board,n)
    else:
        print('Not Possible')   