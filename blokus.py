import pygame
import sys
import re
import numpy as np

import Game
import Board
import Block

from pieces import a_block
from pieces import b_block
from pieces import c_block
from pieces import d_block
from pieces import e_block
from pieces import f_block
from pieces import g_block
from pieces import h_block
from pieces import i_block
from pieces import j_block
from pieces import k_block
from pieces import l_block
from pieces import m_block
from pieces import n_block
from pieces import o_block
from pieces import p_block
from pieces import q_block
from pieces import r_block
from pieces import s_block
from pieces import t_block
from pieces import u_block

#使ったブロックのリスト
greenUsedBlocks = []
yellowUsedBlocks = []

# TODO: Playerクラスのプロパティから引っ張ってくる
#パスリスト
turnPassedList = [False, False] # GREEN, YELLOWの順番

#スコア表
scoreTable = {'a':1, 'b':2, 'c':3, 'd':3, 'e':4, 'f':4, 'g':4, 'h':4, 'i':4, 'j':5, 'k':5, 'l':5, 'm':5, 'n':5, 'o':5, 'p':5, 'q':5, 'r':5, 's':5, 't':5, 'u':5}

# TODO: Gameクラスのプロパティから引っ張ってくる
GREEN  = 'green'
YELLOW = 'yellow'
RED    = 'red' # 将来的に実装
BLUE   = 'blue' # 将来的に実装

# TODO: Gameクラスのプロパティから引っ張ってくる
TILE_NUMBER = 8

def skipTurn(game, board, whoTurn):
    if whoTurn == GREEN:
        nextPlayer = YELLOW
    elif whoTurn == YELLOW:
        nextPlayer = GREEN

    block, whoTurn, selected_block, selectedDirection = selectBlock(game, board, nextPlayer)
    selected_block, selectedDirection          = blockUsableCheck(game, board, block, whoTurn, selected_block, selectedDirection)

    eval(whoTurn + 'UsedBlocks').pop()

    return block, whoTurn, selected_block, selectedDirection

# TODO: scoreCheckの実装
def scoreCheck():
    if all(turnPassedList):
        #スコアチェック
        greenRemainingBlock = list(set(blockSpells) - set(greenUsedBlocks))
        yellowRemainingBlock = list(set(blockSpells) - set(yellowUsedBlocks))
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

        turnPassedList[0] = False
        return True
    else:
        return False


blockSpells  = [chr(ord('a') + i) for i in range(21)] # aからuの配列
blockNumbers = [str(n) for n in range(8)] # 0から7の配列

def selectBlock(game, board, whoTurn):
    print('既に使っているブロック')
    print(sorted(eval(whoTurn + 'UsedBlocks')))
    print('')

    # Xキーが入力されたらターンスキップ
    selected_block = input('ブロックを選択してください：')
    while not selected_block in blockSpells:
        if selected_block == 'x':
            if whoTurn == GREEN:
                turnPassedList[0] = True
            elif whoTurn == YELLOW:
                turnPassedList[1] = True

            if scoreCheck():
                sys.exit()
            else:
                block, whoTurn, selected_block, selectedDirection = skipTurn(game, board, whoTurn)
                return block, whoTurn, selected_block, selectedDirection
        else:
            print('入力が間違っています')
            selected_block = input('ブロックを選択してください：')

    selectedDirection = input('向きを選択してください：')
    while not selectedDirection in blockNumbers:
        print('入力が間違っています')
        selectedDirection = input('向きを選択してください：')
    selectedDirection = int(selectedDirection)

    block = Block.Block(selected_block, selectedDirection)

    return block, whoTurn, selected_block, selectedDirection

def blockUsableCheck(game, board, block, whoTurn, selected_block, selectedDirection):
    while selected_block in eval(whoTurn + 'UsedBlocks'):
        print('そのブロックは既に使っています')
        block, whoTurn, selected_block, selectedDirection = selectBlock(game, board, whoTurn)

    while not board.settable_area_exist_check(block.selected['shape'], eval('board.' + whoTurn + '_board')):
        print('そのブロックを置く場所がありません')
        block, whoTurn, selected_block, selectedDirection = selectBlock(game, board, whoTurn)

    eval(whoTurn + 'UsedBlocks').append(selected_block)

    return selected_block, selectedDirection

def start(game, board):
    # ゲームスタート処理
    board.check_status(game, GREEN)
    block, whoTurn, selected_block, selectedDirection = selectBlock(game, board, GREEN)
    selected_block, selectedDirection          = blockUsableCheck(game, board, block, whoTurn, selected_block, selectedDirection)

    while True:
        for event in pygame.event.get():
            # ESCAPEキーが押されたらゲーム終了
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # Zキーが押されたらブロック選択キャンセル
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                print('\n選択がキャンセルされました\n')
                eval(whoTurn + 'UsedBlocks').pop()
                block, whoTurn, selected_block, selectedDirection = selectBlock(game, board, whoTurn)
                selected_block, selectedDirection          = blockUsableCheck(game, board, block, whoTurn, selected_block, selectedDirection)
            # クリックしたらブロックを配置
            if event.type == pygame.MOUSEBUTTONDOWN:
                xpos = int(pygame.mouse.get_pos()[0]/game.TILE_LENGTH) # 右方向に正
                ypos = int(pygame.mouse.get_pos()[1]/game.TILE_LENGTH) # 下方向に正
                if whoTurn == GREEN:
                    if board.green_board[ypos][xpos] != board.CANTSET:
                        # if eval(selected_block + '_block').main(game.GREEN_IMAGE, game.GREEN_RECT, board.green_board, board.yellow_board, selectedDirection, xpos, ypos, game.surface, game.TILE_LENGTH):
                        if board.settable_check(block.selected['shape'], board.green_board, xpos, ypos):
                            board.change_status(block.selected['shape'], block.selected['influence'], board.green_board, board.yellow_board, xpos, ypos)
                            board.change_image(block.selected['shape'], game.GREEN_IMAGE, game.GREEN_RECT, xpos, ypos, game.surface, game.TILE_LENGTH)
                            board.check_status(game, YELLOW)
                            block, whoTurn, selected_block, selectedDirection = selectBlock(game, board, YELLOW)
                            selected_block, selectedDirection          = blockUsableCheck(game, board, block, whoTurn, selected_block, selectedDirection)
                        else: print('ここには置けません')
                    else: print('ここには置けません')

                elif whoTurn == YELLOW:
                    if board.yellow_board[ypos][xpos] != board.CANTSET:
                        if board.settable_check(block.selected['shape'], board.yellow_board, xpos, ypos):
                            board.change_status(block.selected['shape'], block.selected['influence'], board.yellow_board, board.green_board, xpos, ypos)
                            board.change_image(block.selected['shape'], game.YELLOW_IMAGE, game.YELLOW_RECT, xpos, ypos, game.surface, game.TILE_LENGTH)
                            board.check_status(game,GREEN)
                            block, whoTurn, selected_block, selectedDirection = selectBlock(game, board, GREEN)
                            selected_block, selectedDirection          = blockUsableCheck(game, board, block, whoTurn, selected_block, selectedDirection)
                        else: print('ここには置けません')
                    else: print('ここには置けません')

def main():
    game  = Game.Game()
    board = Board.Board()
    start(game, board)

if __name__ == '__main__':
    main()
