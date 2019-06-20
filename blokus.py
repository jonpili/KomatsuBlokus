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
# from pieces import h_block
# from pieces import i_block
# from pieces import j_block
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

tileLength = 50
tileNumber = 8

BLANK   = 0 # ブロックは置かれていない
CANTSET = 1 # ブロックが置かれている or 自分のブロックが隣接している
ABLESET = 2 # 自分のブロックが角で接している

GREEN  = 1
YELLOW = 2
RED    = 3 # 将来的に実装
BLUE   = 4 # 将来的に実装

# タイルの設置はボード外エラー回避の為2マス広く
screenWidth  = tileLength * (tileNumber + 2)
screenHeight = tileLength * (tileNumber + 2)
tileLimit    = tileLength * tileNumber

#使ったブロックのリスト
greenUsedBlocks = []
yellowUsedBlocks = []

def makeBoard():
    board  = [[BLANK for width in range(tileNumber + 2)] for height in range(tileNumber + 2)]
    # 枠を作成
    for i in range(tileNumber + 2):
        board[0][i]              = CANTSET
        board[tileNumber + 1][i] = CANTSET
    for i in range(tileNumber):
        board[i + 1][0]              = CANTSET
        board[i + 1][tileNumber + 1] = CANTSET
    board = np.asarray(board)
    return board

# 初期位置を設定
boardGreen = makeBoard()
boardGreen[3][3] = ABLESET

boardYellow = makeBoard()
boardYellow[6][6] = ABLESET

surface = pygame.display.set_mode((screenWidth, screenHeight))

def checkBoard(color):
    print('')
    print('ーーーーー緑色の盤面ーーーーー')
    for width in boardGreen:
        print(width)
    print('ーーーーー黄色の盤面ーーーーー')
    for width in boardYellow:
        print(width)

    if color == GREEN:
        whoTurn = GREEN
        print('＝＝＝＝＝緑のターン＝＝＝＝＝')
    elif color == YELLOW:
        whoTurn = YELLOW
        print('＝＝＝＝＝黄のターン＝＝＝＝＝')

    pygame.display.flip()
    return whoTurn

def selectBlock(whoTurn):
    blockSpells = [chr(ord('a') + i) for i in range(21)] # aからuの配列
    blockNumbers = str(list(range(8))) # 0から7の配列

    selectedBlock = input('ブロックを選択してください：')
    while not selectedBlock in blockSpells:
        print('入力が間違っています')
        selectedBlock = input('ブロックを選択してください：')

    # if whoTurn == GREEN:
    #     while selectedBlock in greenUsedBlocks:
    #         print('そのブロックは既に使っています')
    #         selectedBlock = input('ブロックを選択してください：')
    #     greenUsedBlocks.append(selectedBlock)
    #
    # if whoTurn == YELLOW:
    #     while selectedBlock in yellowUsedBlocks:
    #         print('そのブロックは既に使っています')
    #         selectedBlock = input('ブロックを選択してください：')
    #     yellowUsedBlocks.append(selectedBlock)

    selectedDirection = input('向きを選択してください：')
    while not selectedDirection in blockNumbers:
        print('入力が間違っています')
        selectedDirection = input('向きを選択してください：')
    selectedDirection = int(selectedDirection)
    displayBlock(selectedBlock, selectedDirection)

    return selectedBlock, selectedDirection

def rotateBlock(selectedBlock, selectedDirection):
    blockShape, blockInfluences = eval(selectedBlock + '_block').setBlockInfo()

    if selectedDirection == 0: # 初期向き
        rotatedBlockShape = blockShape
        rotatedBlockInfluences = blockInfluences
    elif selectedDirection == 1: # 裏向き
        rotatedBlockShape = np.rot90(blockShape.T, -1)
        rotatedBlockInfluences = np.rot90(blockInfluences.T, -1)
    elif selectedDirection == 2: # 初期向きから90°時計回りに
        rotatedBlockShape = np.rot90(blockShape, -1)
        rotatedBlockInfluences = np.rot90(blockInfluences, -1)
    elif selectedDirection == 3: # 裏向きから90°反時計回りに
        rotatedBlockShape = blockShape.T
        rotatedBlockInfluences = blockInfluences.T
    elif selectedDirection == 4: # 初期向きから180°時計回りに
        rotatedBlockShape = np.rot90(blockShape, -2)
        rotatedBlockInfluences = np.rot90(blockInfluences, -2)
    elif selectedDirection == 5: # 裏向きから180°反時計回りに
        rotatedBlockShape = np.rot90(blockShape.T, -3)
        rotatedBlockInfluences = np.rot90(blockInfluences.T, -3)
    elif selectedDirection == 6: # 初期向きから270°時計回りに
        rotatedBlockShape = np.rot90(blockShape, -3)
        rotatedBlockInfluences = np.rot90(blockInfluences, -3)
    elif selectedDirection == 7: # 裏向きから270°反時計回りに
        rotatedBlockShape = np.rot90(blockShape.T, -2)
        rotatedBlockInfluences = np.rot90(blockInfluences.T, -2)

    return rotatedBlockShape, rotatedBlockInfluences

def checkBlock(selectedBlockFunction, boardMine):

    checkBlock = False

    blockShape, blockInfluences = selectedBlockFunction.setBlockInfo()

    for x in range(tileNumber + 2):
        for y in range(tileNumber + 2):
            if selectedBlockFunction.settableCheck(blockShape, boardMine, x, y):
                checkBlock = True

    return checkBlock

def displayBlock(selectedBlock, selectedDirection):
    eval(selectedBlock + '_block').display(selectedDirection)

def main():
    pygame.init()
    surface.fill((0,0,0)) # 黒で塗りつぶし
    pygame.display.set_caption('Mini Blokus')

    tileImage   = pygame.image.load('tile.bmp').convert()
    greenImage  = pygame.image.load('green.bmp').convert()
    yellowImage = pygame.image.load('yellow.bmp').convert()

    tileRect   = tileImage.get_rect() # 画像と同じサイズの長方形座標を取得
    greenRect  = greenImage.get_rect()
    yellowRect = yellowImage.get_rect()

    pygame.mouse.set_visible(True) #マウスポインターの表示をオン

    # タイルで画面を埋める
    for i in range(0, tileLimit, tileLength):
        for j in range(0, tileLimit, tileLength):
            # 枠の分はスキップ
            surface.blit(tileImage, tileRect.move((i + tileLength), (j + tileLength)))

    whoTurn = checkBoard(GREEN)
    selectedBlock, selectedDirection = selectBlock(GREEN)
    rotatedBlockShape, rotatedBlockInfluences = rotateBlock(selectedBlock, selectedDirection)
    
    while not checkBlock(k_block, boardGreen):
        print('そのブロックを置く場所がありません')
        selectedBlock, selectedDirection = selectBlock(GREEN)

    while True:
        for event in pygame.event.get():
            # ESCAPEキーが押されたらゲーム終了
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # Zキーが押されたらブロック選択キャンセル
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                if whoTurn == GREEN:
                    print('\n選択がキャンセルされました\n')
                    selectedBlock, selectedDirection = selectBlock(GREEN)
                if whoTurn == YELLOW:
                    print('\n選択がキャンセルされました\n')
                    selectedBlock, selectedDirection = selectBlock(YELLOW)
            # クリックしたらブロックを配置
            if event.type == pygame.MOUSEBUTTONDOWN:
                # ボード外エラー回避の為1マス右下に
                xpos = int(pygame.mouse.get_pos()[0]/tileLength) # 右方向に正
                ypos = int(pygame.mouse.get_pos()[1]/tileLength) # 下方向に正
                if whoTurn == GREEN:
                    if boardGreen[ypos][xpos] != CANTSET:
                        if eval(selectedBlock + '_block').main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength):
                            whoTurn = checkBoard(YELLOW)
                            selectedBlock, selectedDirection = selectBlock(YELLOW)

                            while not checkBlock(k_block, boardYellow):
                                print('そのブロックを置く場所がありません')
                                selectedBlock, selectedDirection = selectBlock(YELLOW)

                        else: print('ここには置けません')
                    else: print('ここには置けません')

                elif whoTurn == YELLOW:
                    if boardYellow[ypos][xpos] != CANTSET:
                        if eval(selectedBlock + '_block').main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength):
                            whoTurn = checkBoard(GREEN)
                            selectedBlock, selectedDirection = selectBlock(GREEN)

                            while not checkBlock(k_block, boardGreen):
                                print('そのブロックを置く場所がありません')
                                selectedBlock, selectedDirection = selectBlock(GREEN)

                        else: print('ここには置けません')
                    else: print('ここには置けません')

if __name__ == '__main__':
    main()
