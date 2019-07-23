import pygame
import sys
import re
import numpy as np

import Game
import Board
import Block

#使ったブロックのリスト
greenUsedBlocks = []
yellowUsedBlocks = []

# TODO: Playerクラスのプロパティから引っ張ってくる
turn_passed_list = [False, False] # GREEN, YELLOWの順番

#TODO: Block.pyのblock_tableから引っ張ってくる
scoreTable = {'a':1, 'b':2, 'c':3, 'd':3, 'e':4, 'f':4, 'g':4, 'h':4, 'i':4, 'j':5, 'k':5, 'l':5, 'm':5, 'n':5, 'o':5, 'p':5, 'q':5, 'r':5, 's':5, 't':5, 'u':5}

# TODO: Gameクラスのプロパティから引っ張ってくる
GREEN  = 'green'
YELLOW = 'yellow'
RED    = 'red' # 将来的に実装
BLUE   = 'blue' # 将来的に実装
who_turn = ''

# TODO: Gameクラスのプロパティから引っ張ってくる
TILE_NUMBER = 8

class Player():
    block_shape_index_list     = [chr(ord('a') + i) for i in range(21)] # aからuの配列
    block_direction_index_list = [str(n) for n in range(8)] # 0から7の配列

    def __init__(self):
        self.passed = ''
        self.selected_shape_index = ''
        self.selected_direction_index = ''

    def select_block(self, board, who_turn):
        print('既に使っているブロック')
        print(sorted(eval(who_turn + 'UsedBlocks')))
        print('')

        self.selected_shape_index = input('ブロックを選択してください：')

        while True:
            if self.check_input(board, who_turn):
                break

        if not self.passed:
            self.selected_direction_index = input('向きを選択してください：')
            while not self.selected_direction_index in self.block_direction_index_list:
                print('入力が間違っています')
                self.selected_direction_index = input('向きを選択してください：')
            self.selected_direction_index = int(self.selected_direction_index)

        block = Block.Block(self.selected_shape_index, self.selected_direction_index)
        eval(who_turn + 'UsedBlocks').append(self.selected_shape_index)

        return block, who_turn

    def check_input(self, board, who_turn):
        if self.selected_shape_index in eval(who_turn + 'UsedBlocks') or not self.selected_shape_index in self.block_shape_index_list:
            if self.selected_shape_index in eval(who_turn + 'UsedBlocks'):
                print('そのブロックは既に使っています\n')
                self.selected_shape_index = input('ブロックを選択してください：')
            else:
                # Xキーが入力されたらターンスキップ
                if self.selected_shape_index == 'x':
                    if who_turn == GREEN:
                        turn_passed_list[0] = True
                    elif who_turn == YELLOW:
                        turn_passed_list[1] = True

                    if self.score_check():
                        sys.exit()
                    else:
                        block, who_turn = self.pass_my_turn(board, who_turn)
                        self.passed = True
                else:
                    print('入力が間違っています\n')
                    self.selected_shape_index = input('ブロックを選択してください：')
            return False
        else:
            return True

    # def select_block(self, board, who_turn):
    #     print('既に使っているブロック')
    #     print(sorted(eval(who_turn + 'UsedBlocks')))
    #     print('')
    #
    #     selected_shape_index = input('ブロックを選択してください：')
    #
    #     while selected_shape_index in eval(who_turn + 'UsedBlocks') or not selected_shape_index in self.block_shape_index_list:
    #         if selected_shape_index in eval(who_turn + 'UsedBlocks'):
    #             print('そのブロックは既に使っています\n')
    #             selected_shape_index = input('ブロックを選択してください：')
    #         else:
    #             # Xキーが入力されたらターンスキップ
    #             if selected_shape_index == 'x':
    #                 if who_turn == GREEN:
    #                     turn_passed_list[0] = True
    #                 elif who_turn == YELLOW:
    #                     turn_passed_list[1] = True
    #
    #                 if self.score_check():
    #                     sys.exit()
    #                 else:
    #                     block, who_turn = self.pass_my_turn(board, who_turn)
    #                     return block, who_turn
    #             else:
    #                 print('入力が間違っています\n')
    #                 selected_shape_index = input('ブロックを選択してください：')
    #
    #     selected_direction_index = input('向きを選択してください：')
    #     while not selected_direction_index in self.block_direction_index_list:
    #         print('入力が間違っています')
    #         selected_direction_index = input('向きを選択してください：')
    #     print('ここではselected_shape_indexは' + selected_shape_index)
    #     selected_direction_index = int(selected_direction_index)
    #
    #     block = Block.Block(selected_shape_index, selected_direction_index)
    #     eval(who_turn + 'UsedBlocks').append(selected_shape_index)
    #
    #     return block, who_turn

    def cancel_selected(self, board, block, who_turn):
        print('\n選択がキャンセルされました\n')
        eval(who_turn + 'UsedBlocks').pop()
        block, who_turn = self.select_block(board, who_turn)
        block, who_turn = self.block_usable_check(board, block, who_turn)
        return block, who_turn

    def pass_my_turn(self, board, who_turn):
        if who_turn == GREEN:
            next_player = YELLOW
        elif who_turn == YELLOW:
            next_player = GREEN

        print('\n＝＝＝＝＝' + next_player + '\'s Turn＝＝＝＝＝')
        print('相手がパスしました\n')
        block, who_turn = self.select_block(board, next_player)
        block, who_turn = self.block_usable_check(board, block, who_turn)

        return block, who_turn

    def block_usable_check(self, board, block, who_turn):
        while not board.settable_area_exist_check(TILE_NUMBER, block.selected['shape'], eval('board.' + who_turn + '_board')):
            print('そのブロックを置く場所がありません')
            eval(who_turn + 'UsedBlocks').pop()
            block, who_turn = self.select_block(board, who_turn)
        return block, who_turn

    def score_check(self):
        if all(turn_passed_list):
            #スコアチェック
            greenRemainingBlock = list(set(self.block_shape_index_list) - set(greenUsedBlocks))
            yellowRemainingBlock = list(set(self.block_shape_index_list) - set(yellowUsedBlocks))
            greenScore = sum(list(map(lambda alphabet: scoreTable[alphabet], greenRemainingBlock)))
            yellowScore = sum(list(map(lambda alphabet: scoreTable[alphabet], yellowRemainingBlock)))
            #結果発表
            print('ゲームは終了です')
            print('緑色の点数は' + str(greenScore) + '点です')
            print('黄色の点数は' + str(yellowScore) + '点です')

            if greenScore < yellowScore:
                print('勝者は「緑色」です')
            elif greenScore > yellowScore:
                print('勝者は「黄色」です')
            else:
                if len(greenRemainingBlock) < len(yellowRemainingBlock):
                    print('勝者は「緑色」です')
                elif len(greenRemainingBlock) > len(yellowRemainingBlock):
                    print('勝者は「黄色」です')
                else:
                    print('引き分けです')

            turn_passed_list[0] = False
            return True
        else:
            return False

def start(game, board):
    player = Player()
    # ゲームスタート処理
    board.check_status(game, turn_passed_list, GREEN)
    block, who_turn = player.select_block(board, GREEN)
    block, who_turn = player.block_usable_check(board, block, who_turn)

    while True:
        for event in pygame.event.get():
            # ESCAPEキーが押されたらゲーム終了
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # Zキーが押されたらブロック選択キャンセル
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                block, who_turn = player.cancel_selected(board, block, who_turn)
            # クリックしたらブロックを配置
            if event.type == pygame.MOUSEBUTTONDOWN:
                xpos = int(pygame.mouse.get_pos()[0]/game.TILE_LENGTH) # 右方向に正
                ypos = int(pygame.mouse.get_pos()[1]/game.TILE_LENGTH) # 下方向に正
                if who_turn == GREEN:
                    if board.settable_check(block.selected['shape'], board.green_board, xpos, ypos):
                        board.change_status(block.selected['shape'], block.selected['influence'], board.green_board, board.yellow_board, xpos, ypos)
                        board.change_image(block.selected['shape'], game.GREEN_IMAGE, game.GREEN_RECT, xpos, ypos, game.surface, game.TILE_LENGTH)
                        board.check_status(game, turn_passed_list, YELLOW)
                        block, who_turn = player.select_block(board, YELLOW)
                        block, who_turn = player.block_usable_check(board, block, who_turn)
                    else: print('ここには置けません')

                elif who_turn == YELLOW:
                    if board.settable_check(block.selected['shape'], board.yellow_board, xpos, ypos):
                        board.change_status(block.selected['shape'], block.selected['influence'], board.yellow_board, board.green_board, xpos, ypos)
                        board.change_image(block.selected['shape'], game.YELLOW_IMAGE, game.YELLOW_RECT, xpos, ypos, game.surface, game.TILE_LENGTH)
                        board.check_status(game, turn_passed_list, GREEN)
                        block, who_turn = player.select_block(board, GREEN)
                        block, who_turn = player.block_usable_check(board, block, who_turn)
                    else: print('ここには置けません')

def main():
    game  = Game.Game()
    board = Board.Board(game.TILE_NUMBER)
    start(game, board)

if __name__ == '__main__':
    main()