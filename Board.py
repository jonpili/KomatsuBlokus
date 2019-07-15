import pygame
import numpy as np

# TODO: Gameクラスのプロパティから引っ張ってくる
GREEN  = 'green'
YELLOW = 'yellow'
RED    = 'red' # 将来的に実装
BLUE   = 'blue' # 将来的に実装

# TODO: Playerクラスのプロパティから引っ張ってくる
#パスリスト
turnPassedList = [False, False] # GREEN, YELLOWの順番

# TODO: Gameクラスのプロパティから引っ張ってくる
TILE_NUMBER = 8

class Board():
    BLANK   = 0 # ブロックは置かれていない
    CANTSET = 1 # ブロックが置かれている or 自分のブロックが隣接している
    ABLESET = 2 # 自分のブロックが角で接している

    def __init__(self):
        self.status = self.make_board()
        # 緑色のスタート地点
        self.status[3][3][0] = self.ABLESET
        # 黄色のスタート地点
        self.status[6][6][1] = self.ABLESET

        self.green_board = list(map(lambda x: list(map(lambda y: y[0], x)), self.status))
        self.yellow_board = list(map(lambda x: list(map(lambda y: y[1], x)), self.status))

    def make_board(self):
        board  = [[[self.BLANK, self.BLANK] for width in range(TILE_NUMBER + 2)] for height in range(TILE_NUMBER + 2)]
        # 枠を作成
        for i in range(TILE_NUMBER + 2):
            board[0][i]              = [self.CANTSET, self.CANTSET]
            board[TILE_NUMBER + 1][i] = [self.CANTSET, self.CANTSET]
        for i in range(TILE_NUMBER):
            board[i + 1][0]              = [self.CANTSET, self.CANTSET]
            board[i + 1][TILE_NUMBER + 1] = [self.CANTSET, self.CANTSET]
        board = np.asarray(board)
        return board

    def check_status(self, game, whoTurn):
        print('')
        print('ーーーーー緑色の盤面ーーーーー')
        for width in self.green_board:
            print(width)
        print('ーーーーー黄色の盤面ーーーーー')
        for width in self.yellow_board:
            print(width)

        if whoTurn == GREEN:
            print('＝＝＝＝＝緑のターン＝＝＝＝＝')
            if turnPassedList[0]:
                print('あなたは既にパスしたので、xを入力してください')
                print('')
        elif whoTurn == YELLOW:
            print('＝＝＝＝＝黄のターン＝＝＝＝＝')
            if turnPassedList[1]:
                print('あなたは既にパスしたので、xを入力してください')
                print('')

        pygame.display.flip()
        return False

    def settable_area_exist_check(self, game, selected_block, rotated_block_shape, board_mine):
        settable_area_exist = False

        for x in range(1, TILE_NUMBER + 1):
            for y in range(1, TILE_NUMBER + 1):
                if self.settable_check(rotated_block_shape, board_mine, x, y):
                    settable_area_exist = True

        return settable_area_exist

    def settable_check(self, block_shape, board_mine, x, y):
        # 1つでもCANTSETがあれば置けない
        for coord in np.argwhere(block_shape == self.CANTSET):
            if board_mine[y + coord[0] - 2][x + coord[1] - 2] == self.CANTSET:
                return False
        # 1つでもABLESETがあれば置ける
        for coord in np.argwhere(block_shape == self.CANTSET):
            if board_mine[y + coord[0] - 2][x + coord[1] - 2] == self.ABLESET:
                return True
