import pygame
import numpy as np

class Board():
    BLANK   = 0 # ブロックは置かれていない
    CANTSET = 1 # ブロックが置かれている or 自分のブロックが隣接している
    ABLESET = 2 # 自分のブロックが角で接している

    def __init__(self, TILE_NUMBER):
        self.TILE_NUMBER = TILE_NUMBER

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
        print('')
        print('ーーーーー緑色の盤面ーーーーー')
        for width in self.green_board:
            print(width)
        print('ーーーーー黄色の盤面ーーーーー')
        for width in self.yellow_board:
            print(width)

        print('＝＝＝＝＝' + game.who_turn + '\'s Turn＝＝＝＝＝')

        # if game.who_turn == game.GREEN:
        #     if turn_passed_list[0]:
        #         print('あなたは既にパスしたので、xを入力してください')
        #         print('')
        # elif game.who_turn == game.YELLOW:
        #     if turn_passed_list[1]:
        #         print('あなたは既にパスしたので、xを入力してください')
        #         print('')

        pygame.display.flip()

    def settable_area_exist_check(self, color, block_shape):
        settable_area_exist = False

        for x in range(1, self.TILE_NUMBER + 1):
            for y in range(1, self.TILE_NUMBER + 1):
                if self.settable_check(color, block_shape, x, y):
                    settable_area_exist = True

        return settable_area_exist

    def settable_check(self, color, block_shape, x, y):
        # 1つでもCANTSETがあれば置けない
        for coord in np.argwhere(block_shape == self.CANTSET):
            if eval('self.' + color + '_board')[y + coord[0] - 2][x + coord[1] - 2] == self.CANTSET:
                return False
        # 1つでもABLESETがあれば置ける
        for coord in np.argwhere(block_shape == self.CANTSET):
            if eval('self.' + color + '_board')[y + coord[0] - 2][x + coord[1] - 2] == self.ABLESET:
                return True

    def change_status(self, block_shape, block_influence, board_mine, board_opponent, x, y):
        # ブロックの影響を自分のボードに適用
        for coord in np.argwhere(block_influence == self.CANTSET):
            board_mine[y + coord[0] - 3][x + coord[1] - 3] = self.CANTSET
        for coord in np.argwhere(block_influence == self.ABLESET):
            if board_mine[y + coord[0] - 3][x + coord[1] - 3] == self.BLANK:
                board_mine[y + coord[0] - 3][x + coord[1] - 3] = self.ABLESET

        # ブロックの影響を自分以外のボードに適用
        for coord in np.argwhere(block_shape == self.CANTSET):
            board_opponent[y + coord[0] - 2][x + coord[1] - 2] = self.CANTSET

    def change_image(self, block_shape, color_image, color_rect, x, y, surface, TILE_LENGTH):
        for coord in np.argwhere(block_shape == self.CANTSET):
            surface.blit(color_image, color_rect.move(TILE_LENGTH * (x + coord[1] - 2), TILE_LENGTH * (y + coord[0] - 2)))
