import pygame
import sys
import re
import numpy as np

from pieces import a_block
from pieces import b_block
from pieces import k_block
from pieces import q_block

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

    if color == YELLOW:
        whoTurn = GREEN
        print('＝＝＝＝＝緑のターン＝＝＝＝＝')
    elif color == GREEN:
        whoTurn = YELLOW
        print('＝＝＝＝＝黄のターン＝＝＝＝＝')

    pygame.display.flip()
    return whoTurn

def selectBlock():
    selectedBlock = input('ブロックを選択してください：')
    while not re.match('[a-u]{1}', selectedBlock):
        print('入力が間違っています')
        selectedBlock = input('ブロックを選択してください：')

    selectedDirection = input('向きを選択してください：')
    while not re.match('[0-7]{1}', selectedDirection):
        print('入力が間違っています')
        selectedDirection = input('向きを選択してください：')
    selectedDirection = int(selectedDirection)
    displayBlock(selectedBlock, selectedDirection)

    return selectedBlock, selectedDirection

def displayBlock(selectedBlock, selectedDirection):
    if selectedBlock == 'a':
        a_block.display()
    elif selectedBlock == 'b':
        b_block.display(selectedDirection)
    elif selectedBlock == 'k':
        k_block.display(selectedDirection)
    elif selectedBlock == 'q':
        q_block.display(selectedDirection)

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

    whoTurn = checkBoard(YELLOW)
    selectedBlock, selectedDirection = selectBlock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit() # ESCAPEキーが押されたら終了
            if event.type == pygame.MOUSEBUTTONDOWN:
                # ボード外エラー回避の為1マス右下に
                xpos = int(pygame.mouse.get_pos()[0]/tileLength) # 右方向に正
                ypos = int(pygame.mouse.get_pos()[1]/tileLength) # 下方向に正
                if whoTurn == GREEN:
                    if boardGreen[ypos][xpos] != CANTSET:
                        if selectedBlock == 'a':
                            if a_block.main(greenImage, greenRect, boardGreen, boardYellow, xpos, ypos, surface, tileLength):
                                whoTurn = checkBoard(GREEN)
                                selectedBlock, selectedDirection = selectBlock()
                        elif selectedBlock == 'b':
                            if b_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength):
                                whoTurn = checkBoard(GREEN)
                                selectedBlock, selectedDirection = selectBlock()
                        elif selectedBlock == 'k':
                            if k_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength):
                                whoTurn = checkBoard(GREEN)
                                selectedBlock, selectedDirection = selectBlock()
                        elif selectedBlock == 'q':
                            if q_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength):
                                whoTurn = checkBoard(GREEN)
                                selectedBlock, selectedDirection = selectBlock()

                elif whoTurn == YELLOW:
                    if boardYellow[ypos][xpos] != CANTSET:
                        if selectedBlock == 'a':
                            if a_block.main(yellowImage, yellowRect, boardYellow, boardGreen, xpos, ypos, surface, tileLength):
                                whoTurn = checkBoard(YELLOW)
                                selectedBlock, selectedDirection = selectBlock()
                        elif selectedBlock == 'b':
                            if b_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength):
                                whoTurn = checkBoard(YELLOW)
                                selectedBlock, selectedDirection = selectBlock()
                        elif selectedBlock == 'k':
                            if k_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength):
                                whoTurn = checkBoard(YELLOW)
                                selectedBlock, selectedDirection = selectBlock()
                        elif selectedBlock == 'q':
                            if q_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength):
                                whoTurn = checkBoard(YELLOW)
                                selectedBlock, selectedDirection = selectBlock()

if __name__ == '__main__':
    main()
