import numpy as np

# array = [
#         [1,2,3,4,5],
#         [1,2,3,4,5],
#         [1,2,3,4,5],
#         [1,2,3,4,5],
#         [1,2,3,4,5]
#         ]
#
# array = np.asarray(array)

BLANK   = 0 # ブロックは置かれていない
CANTSET = 1 # ブロックが置かれている or 自分のブロックが隣接している
ABLESET = 2 # 自分のブロックが角で接している

TILE_NUMBER = 8

def make_board():
    board  = [[[BLANK, BLANK] for width in range(TILE_NUMBER + 2)] for height in range(TILE_NUMBER + 2)]
    # 枠を作成
    for i in range(TILE_NUMBER + 2):
        board[0][i]              = [CANTSET, CANTSET]
        board[TILE_NUMBER + 1][i] = [CANTSET, CANTSET]
    for i in range(TILE_NUMBER):
        board[i + 1][0]              = [CANTSET, CANTSET]
        board[i + 1][TILE_NUMBER + 1] = [CANTSET, CANTSET]
    board = np.asarray(board)
    return board

board = make_board()

green_board = list(map(lambda x: list(map(lambda y: y[1], x)), board))
print(green_board)
