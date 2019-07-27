import pygame
import numpy as np
import Block

class Board():
    BLANK   = 0 # ブロックは置かれていない
    CANTSET = 1 # ブロックが置かれている or 自分のブロックが隣接している
    ABLESET = 2 # 自分のブロックが角で接している

    def __init__(self, game):
        self.TILE_NUMBER = game.TILE_NUMBER
        self.COLOR_LIST  = game.COLOR_LIST

        self.status = self.make_board()
        # 緑色のスタート地点
        self.status[3][3][0] = self.ABLESET
        # 黄色のスタート地点
        self.status[6][6][1] = self.ABLESET

        self.green_board = list(map(lambda x: list(map(lambda y: y[0], x)), self.status))
        self.yellow_board = list(map(lambda x: list(map(lambda y: y[1], x)), self.status))

    def make_board(self):
        board  = [[[self.BLANK, self.BLANK] for width in range(self.TILE_NUMBER + 2)] for height in range(self.TILE_NUMBER + 2)]
        # 枠を作成
        for i in range(self.TILE_NUMBER + 2):
            board[0][i]              = [self.CANTSET, self.CANTSET]
            board[self.TILE_NUMBER + 1][i] = [self.CANTSET, self.CANTSET]
        for i in range(self.TILE_NUMBER):
            board[i + 1][0]              = [self.CANTSET, self.CANTSET]
            board[i + 1][self.TILE_NUMBER + 1] = [self.CANTSET, self.CANTSET]
        board = np.asarray(board)
        return board

    def check_status(self, game):
        # テスト用に便利なので残しておく
        # print('')
        # print('ーーーーー緑色の盤面ーーーーー')
        # for width in self.green_board:
        #     print(width)
        # print('ーーーーー黄色の盤面ーーーーー')
        # for width in self.yellow_board:
        #     print(width)

        print('\n＝＝＝＝＝＝＝＝＝＝' + game.current_player.color + '\'s Turn＝＝＝＝＝＝＝＝＝＝\n')

        pygame.display.flip()

    def any_block_settable_check(self, player):
        # passed = Trueであればパスする
        if player.passed:
            return False
        else:
            # 持ち駒のうち一つでも置けるものがあればターン続行
            for block_shape_index in [i for i in player.block_shape_index_list if i not in player.used_blocks]:
                for block_direction_index in range(8):
                    block_for_check = Block.Block(block_shape_index, block_direction_index, False)
                    if self.settable_area_exist_check(player.color, block_for_check.selected['shape']):
                        return True
            player.passed = True
            return False

    def settable_area_exist_check(self, color, block_shape):
        for x in range(1, self.TILE_NUMBER + 1):
            for y in range(1, self.TILE_NUMBER + 1):
                if self.settable_check(color, block_shape, x, y):
                    return True
        return False

    def settable_check(self, color, block_shape, x, y):
        # 1つでもCANTSETがあれば置けない
        for coord in np.argwhere(block_shape == self.CANTSET):
            if eval('self.' + color + '_board')[y + coord[0] - 2][x + coord[1] - 2] == self.CANTSET:
                return False
        # 1つでもABLESETがあれば置ける
        for coord in np.argwhere(block_shape == self.CANTSET):
            if eval('self.' + color + '_board')[y + coord[0] - 2][x + coord[1] - 2] == self.ABLESET:
                return True
        return False

    def change_status(self, color, block_shape, block_influence, x, y):
        # ブロックの影響を自分のボードに適用
        for coord in np.argwhere(block_influence == self.CANTSET):
            eval('self.' + color + '_board')[y + coord[0] - 3][x + coord[1] - 3] = self.CANTSET
        for coord in np.argwhere(block_influence == self.ABLESET):
            if eval('self.' + color + '_board')[y + coord[0] - 3][x + coord[1] - 3] == self.BLANK:
                eval('self.' + color + '_board')[y + coord[0] - 3][x + coord[1] - 3] = self.ABLESET

        # ブロックの影響を自分以外のボードに適用
        opponent_colors = [i for i in self.COLOR_LIST if i != color]
        for opponent_color in opponent_colors:
            for coord in np.argwhere(block_shape == self.CANTSET):
                eval('self.' + opponent_color + '_board')[y + coord[0] - 2][x + coord[1] - 2] = self.CANTSET
