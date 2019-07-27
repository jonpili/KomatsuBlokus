import pygame
import sys
import re
import numpy as np

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

#パスリスト
turnPassedList = [False, False] # GREEN, YELLOWの順番

#スコア表
scoreTable = {'a':1, 'b':2, 'c':3, 'd':3, 'e':4, 'f':4, 'g':4, 'h':4, 'i':4, 'j':5, 'k':5, 'l':5, 'm':5, 'n':5, 'o':5, 'p':5, 'q':5, 'r':5, 's':5, 't':5, 'u':5}

# TODO: Gameクラスのプロパティに格納する
GREEN  = 'green'
YELLOW = 'yellow'
RED    = 'red' # 将来的に実装
BLUE   = 'blue' # 将来的に実装

class Game():
    TILE_LENGTH = 50
    TILE_NUMBER = 8

    BLANK   = 0 # ブロックは置かれていない
    CANTSET = 1 # ブロックが置かれている or 自分のブロックが隣接している
    ABLESET = 2 # 自分のブロックが角で接している

    def __init__(self):
        # 初期位置を設定
        self.green_board = self.make_board()
        self.green_board[3][3] = self.ABLESET

        self.yellow_board = self.make_board()
        self.yellow_board[6][6] = self.ABLESET

    def make_board(self):
        board  = [[self.BLANK for width in range(self.TILE_NUMBER + 2)] for height in range(self.TILE_NUMBER + 2)]
        # 枠を作成
        for i in range(self.TILE_NUMBER + 2):
            board[0][i]              = self.CANTSET
            board[self.TILE_NUMBER + 1][i] = self.CANTSET
        for i in range(self.TILE_NUMBER):
            board[i + 1][0]              = self.CANTSET
            board[i + 1][self.TILE_NUMBER + 1] = self.CANTSET
        board = np.asarray(board)
        return board

    # タイルの設置はボード外エラー回避の為2マス広く
    SCREEN_WIDTH  = TILE_LENGTH * (TILE_NUMBER + 2)
    SCREEN_HEIGHT = TILE_LENGTH * (TILE_NUMBER + 2)
    TILE_LIMIT    = TILE_LENGTH * TILE_NUMBER

    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    surface.fill((0,0,0)) # 黒で塗りつぶし

    pygame.init()
    pygame.display.set_caption('Komatsu Blokus')
    pygame.mouse.set_visible(True) #マウスポインターの表示をオン

    TILE_IMAGE   = pygame.image.load('image/tile.bmp').convert()
    GREEN_IMAGE  = pygame.image.load('image/green.bmp').convert()
    YELLOW_IMAGE = pygame.image.load('image/yellow.bmp').convert()

    TILE_RECT   = TILE_IMAGE.get_rect() # 画像と同じサイズの長方形座標を取得
    GREEN_RECT  = GREEN_IMAGE.get_rect()
    YELLOW_RECT = YELLOW_IMAGE.get_rect()

    # タイルで画面を埋める
    for i in range(0, TILE_LIMIT, TILE_LENGTH):
        for j in range(0, TILE_LIMIT, TILE_LENGTH):
            # 枠の分はスキップ
            surface.blit(TILE_IMAGE, TILE_RECT.move((i + TILE_LENGTH), (j + TILE_LENGTH)))

def skipTurn(game, whoTurn):
    if whoTurn == GREEN:
        nextPlayer = YELLOW
    elif whoTurn == YELLOW:
        nextPlayer = GREEN

    whoTurn, selectedBlock, selectedDirection = selectBlock(game, nextPlayer)
    rotatedBlockShape                         = rotateBlock(selectedBlock, selectedDirection)
    selectedBlock, selectedDirection          = blockUsableCheck(game, whoTurn, selectedBlock, selectedDirection, rotatedBlockShape)

    if whoTurn == GREEN:
        color2 = 'green'
    elif whoTurn == YELLOW:
        color2 = 'yellow'
    eval(color2 + 'UsedBlocks').pop()

    return whoTurn, selectedBlock, selectedDirection

# class: Judge():
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

def checkBoard(game, whoTurn):
    if scoreCheck():
        return True
    else:
        print('')
        print('ーーーーー緑色の盤面ーーーーー')
        for width in game.green_board:
            print(width)
        print('ーーーーー黄色の盤面ーーーーー')
        for width in game.yellow_board:
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

blockSpells  = [chr(ord('a') + i) for i in range(21)] # aからuの配列
blockNumbers = [str(n) for n in range(8)] # 0から7の配列

def selectBlock(game, whoTurn):
    if whoTurn == GREEN:
        color = 'green'
    elif whoTurn == YELLOW:
        color = 'yellow'

    print('既に使っているブロック')
    print(sorted(eval(color + 'UsedBlocks')))
    print('')

    # Xキーが入力されたらターンスキップ
    selectedBlock = input('ブロックを選択してください：')
    while not selectedBlock in blockSpells:
        if selectedBlock == 'x':
            if whoTurn == GREEN:
                turnPassedList[0] = True
            elif whoTurn == YELLOW:
                turnPassedList[1] = True

            if scoreCheck():
                sys.exit()
            else:
                whoTurn, selectedBlock, selectedDirection = skipTurn(game, whoTurn)
                return whoTurn, selectedBlock, selectedDirection
        else:
            print('入力が間違っています')
            selectedBlock = input('ブロックを選択してください：')

    selectedDirection = input('向きを選択してください：')
    while not selectedDirection in blockNumbers:
        print('入力が間違っています')
        selectedDirection = input('向きを選択してください：')
    selectedDirection = int(selectedDirection)

    eval(selectedBlock + '_block').display(selectedDirection)

    return whoTurn, selectedBlock, selectedDirection

def rotateBlock(selectedBlock, selectedDirection):
    blockShape, blockInfluences = eval(selectedBlock + '_block').setBlockInfo()

    if selectedDirection == 0: # 初期向き
        rotatedBlockShape      = blockShape
        rotatedBlockInfluences = blockInfluences
    elif selectedDirection == 1: # 裏向き
        rotatedBlockShape      = np.rot90(blockShape.T, -1)
        rotatedBlockInfluences = np.rot90(blockInfluences.T, -1)
    elif selectedDirection == 2: # 初期向きから90°時計回りに
        rotatedBlockShape      = np.rot90(blockShape, -1)
        rotatedBlockInfluences = np.rot90(blockInfluences, -1)
    elif selectedDirection == 3: # 裏向きから90°反時計回りに
        rotatedBlockShape      = blockShape.T
        rotatedBlockInfluences = blockInfluences.T
    elif selectedDirection == 4: # 初期向きから180°時計回りに
        rotatedBlockShape      = np.rot90(blockShape, -2)
        rotatedBlockInfluences = np.rot90(blockInfluences, -2)
    elif selectedDirection == 5: # 裏向きから180°反時計回りに
        rotatedBlockShape      = np.rot90(blockShape.T, -3)
        rotatedBlockInfluences = np.rot90(blockInfluences.T, -3)
    elif selectedDirection == 6: # 初期向きから270°時計回りに
        rotatedBlockShape      = np.rot90(blockShape, -3)
        rotatedBlockInfluences = np.rot90(blockInfluences, -3)
    elif selectedDirection == 7: # 裏向きから270°反時計回りに
        rotatedBlockShape      = np.rot90(blockShape.T, -2)
        rotatedBlockInfluences = np.rot90(blockInfluences.T, -2)

    return rotatedBlockShape

def blockUsableCheck(game, whoTurn, selectedBlock, selectedDirection, rotatedBlockShape):
    if whoTurn == GREEN:
        color = 'green'
    elif whoTurn == YELLOW:
        color = 'yellow'

    while selectedBlock in eval(color + 'UsedBlocks'):
        print('そのブロックは既に使っています')
        whoTurn, selectedBlock, selectedDirection = selectBlock(game, whoTurn)
        rotatedBlockShape                         = rotateBlock(selectedBlock, selectedDirection)

    while not settableAreaExistCheck(game, selectedBlock, rotatedBlockShape, eval('game.' + color + '_board')):
        print('そのブロックを置く場所がありません')
        whoTurn, selectedBlock, selectedDirection = selectBlock(game, whoTurn)
        rotatedBlockShape                         = rotateBlock(selectedBlock, selectedDirection)

    eval(color + 'UsedBlocks').append(selectedBlock)

    return selectedBlock, selectedDirection

def settableAreaExistCheck(game, selectedBlock, rotatedBlockShape, boardMine):
    settableAreaExist = False

    for x in range(1, game.TILE_NUMBER + 1):
        for y in range(1, game.TILE_NUMBER + 1):
            if eval(selectedBlock + '_block').settableCheck(rotatedBlockShape, boardMine, x, y):
                settableAreaExist = True

    return settableAreaExist

def start(game):
    # ゲームスタート処理
    checkBoard(game, GREEN)
    whoTurn, selectedBlock, selectedDirection = selectBlock(game, GREEN)
    rotatedBlockShape                         = rotateBlock(selectedBlock, selectedDirection)
    selectedBlock, selectedDirection          = blockUsableCheck(game, whoTurn, selectedBlock, selectedDirection, rotatedBlockShape)

    while True:
        for event in pygame.event.get():
            # ESCAPEキーが押されたらゲーム終了
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # Zキーが押されたらブロック選択キャンセル
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                if whoTurn == 1:
                    color = 'green'
                elif whoTurn == 2:
                    color = 'yellow'
                print('\n選択がキャンセルされました\n')
                eval(color + 'UsedBlocks').pop()
                whoTurn, selectedBlock, selectedDirection = selectBlock(game, whoTurn)
                rotatedBlockShape                         = rotateBlock(selectedBlock, selectedDirection)
                selectedBlock, selectedDirection          = blockUsableCheck(game, whoTurn, selectedBlock, selectedDirection, rotatedBlockShape)
            # クリックしたらブロックを配置
            if event.type == pygame.MOUSEBUTTONDOWN:
                xpos = int(pygame.mouse.get_pos()[0]/game.TILE_LENGTH) # 右方向に正
                ypos = int(pygame.mouse.get_pos()[1]/game.TILE_LENGTH) # 下方向に正
                if whoTurn == GREEN:
                    if game.green_board[ypos][xpos] != game.CANTSET:
                        if eval(selectedBlock + '_block').main(game.GREEN_IMAGE, game.GREEN_RECT, game.green_board, game.yellow_board, selectedDirection, xpos, ypos, game.surface, game.TILE_LENGTH):
                            checkBoard(game, YELLOW)
                            whoTurn, selectedBlock, selectedDirection = selectBlock(game, YELLOW)
                            rotatedBlockShape                         = rotateBlock(selectedBlock, selectedDirection)
                            selectedBlock, selectedDirection          = blockUsableCheck(game, whoTurn, selectedBlock, selectedDirection, rotatedBlockShape)
                        else: print('ここには置けません')
                    else: print('ここには置けません')

                elif whoTurn == YELLOW:
                    if game.yellow_board[ypos][xpos] != game.CANTSET:
                        if eval(selectedBlock + '_block').main(game.YELLOW_IMAGE, game.YELLOW_RECT, game.yellow_board, game.green_board, selectedDirection, xpos, ypos, game.surface, game.TILE_LENGTH):
                            checkBoard(game,GREEN)
                            whoTurn, selectedBlock, selectedDirection = selectBlock(game, GREEN)
                            rotatedBlockShape                         = rotateBlock(selectedBlock, selectedDirection)
                            selectedBlock, selectedDirection          = blockUsableCheck(game, whoTurn, selectedBlock, selectedDirection, rotatedBlockShape)
                        else: print('ここには置けません')
                    else: print('ここには置けません')

def main():
    game = Game()
    start(game)

if __name__ == '__main__':
    main()
