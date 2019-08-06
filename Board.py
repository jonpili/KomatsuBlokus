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

        if game.player_number == 2:
            start_number = (game.TILE_NUMBER + 1) // 3
            self.status[0][start_number][start_number]         = self.ABLESET # 緑色のスタート地点
            self.status[1][start_number * 2][start_number * 2] = self.ABLESET # 黄色のスタート地点
        elif game.player_number == 4:
            start_number = game.TILE_NUMBER
            self.status[0][1][1]                       = self.ABLESET # 緑色のスタート地点
            self.status[1][1][start_number]            = self.ABLESET # 黄色のスタート地点
            self.status[2][start_number][start_number] = self.ABLESET # 赤色のスタート地点
            self.status[3][start_number][1]            = self.ABLESET # 青色のスタート地点

    def make_board(self):
        board  = [[self.BLANK for width in range(self.TILE_NUMBER + 2)] for height in range(self.TILE_NUMBER + 2)]
        # 枠を作成
        for i in range(self.TILE_NUMBER + 2):
            board[0][i]                    = self.CANTSET
            board[self.TILE_NUMBER + 1][i] = self.CANTSET
        for i in range(self.TILE_NUMBER):
            board[i + 1][0]                    = self.CANTSET
            board[i + 1][self.TILE_NUMBER + 1] = self.CANTSET

        boards = []
        for color in self.COLOR_LIST:
            boards.append(board)

        boards = np.asarray(boards)
        return boards

    def check_status(self, game):
        # テスト用に残しておく
        # print('')
        # print('ーーーーー緑色の盤面ーーーーー')
        # for row in self.status[0]:
        #     print(row)
        # print('ーーーーー黄色の盤面ーーーーー')
        # for row in self.status[1]:
        #     print(row)

        print('\n＝＝＝＝＝＝＝＝＝＝' + game.current_player.color.name + '\'s Turn＝＝＝＝＝＝＝＝＝＝')

        for number in range(game.player_number):
            print(game.players[number].color.name + ':' + str(game.players[number].score), end='  ')
        print('')

    def any_block_settable_check(self, player):
        if player.passed:
            return False
        else:
            player.usable_blocks.clear()
            for block_shape_index in [i for i in player.block_shape_index_list if i not in player.used_blocks]:
                for block_direction_index in range(8):
                    block_for_check = Block.Block(block_shape_index, block_direction_index, False)
                    settable_position = self.settable_area_exist_check(player.color, block_for_check)
                    if len(settable_position) > 0:
                        player.usable_blocks.append([block_shape_index, block_direction_index, settable_position])
            if len(player.usable_blocks) > 0:
                return True
            else:
                player.passed = True
                return False

    def settable_area_exist_check(self, color, block_for_check):
        settable_position = []

        for x in range(1, self.TILE_NUMBER + 1):
            for y in range(1, self.TILE_NUMBER + 1):
                if self.status[color.value][y][x] != self.CANTSET:
                    if self.settable_check(color, block_for_check.selected['shape'], x, y):
                        settable_position.append([x, y])

        return settable_position

    def settable_check(self, color, block_shape, x, y):
        # 1つでもCANTSETがあれば置けない
        for coord in np.argwhere(block_shape == self.CANTSET):
            if self.status[color.value][y + coord[0] - 2][x + coord[1] - 2] == self.CANTSET:
                return False
        # 1つでもABLESETがあれば置ける
        for coord in np.argwhere(block_shape == self.CANTSET):
            if self.status[color.value][y + coord[0] - 2][x + coord[1] - 2] == self.ABLESET:
                return True
        return False

    def change_status(self, color, block_shape, block_influence, x, y):
        # ブロックの影響を自分のボードに適用
        for coord in np.argwhere(block_influence == self.CANTSET):
            self.status[color.value][y + coord[0] - 3][x + coord[1] - 3] = self.CANTSET
        for coord in np.argwhere(block_influence == self.ABLESET):
            if self.status[color.value][y + coord[0] - 3][x + coord[1] - 3] == self.BLANK:
                self.status[color.value][y + coord[0] - 3][x + coord[1] - 3] = self.ABLESET

        # ブロックの影響を自分以外のボードに適用
        opponent_colors = [i for i in self.COLOR_LIST if i != color]
        for board_opponent_color in opponent_colors:
            for coord in np.argwhere(block_shape == self.CANTSET):
                self.status[board_opponent_color.value][y + coord[0] - 2][x + coord[1] - 2] = self.CANTSET
