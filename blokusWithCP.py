import pygame
import sys
import re
import numpy as np
import random

from pieces import a_block
from pieces import b_block
from pieces import c_block
# from pieces import d_block
# from pieces import e_block
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
# from pieces import r_block
from pieces import s_block
# from pieces import t_block
# from pieces import u_block

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

def selectPositionByPlayer(selectedBlock, selectedDirection, greenImage, greenRect, yellowImage, yellowRect):
    while True:
        for event in pygame.event.get():
            # ESCAPEキーが押されたらゲーム終了
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # Zキーが押されたらブロック選択キャンセル
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                print('\n選択がキャンセルされました\n')
                selectedBlock, selectedDirection = selectBlock()
            # クリックしたらブロックを配置
            if event.type == pygame.MOUSEBUTTONDOWN:
                # ボード外エラー回避の為1マス右下に
                xpos = int(pygame.mouse.get_pos()[0]/tileLength) # 右方向に正
                ypos = int(pygame.mouse.get_pos()[1]/tileLength) # 下方向に正
                if boardGreen[ypos][xpos] != CANTSET:
                    if (
                    (selectedBlock == 'a' and a_block.main(greenImage, greenRect, boardGreen, boardYellow, xpos, ypos, surface, tileLength))
                    or (selectedBlock == 'b' and b_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength))
                    or (selectedBlock == 'c' and c_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength))
                    # or (selectedBlock == 'd' and d_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength))
                    # or (selectedBlock == 'e' and e_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength))
                    or (selectedBlock == 'f' and f_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength))
                    or (selectedBlock == 'g' and g_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength))
                    # or (selectedBlock == 'h' and h_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength))
                    # or (selectedBlock == 'i' and i_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength))
                    # or (selectedBlock == 'j' and j_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength))
                    or (selectedBlock == 'k' and k_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength))
                    or (selectedBlock == 'l' and l_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength))
                    or (selectedBlock == 'm' and m_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength))
                    or (selectedBlock == 'n' and n_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength))
                    or (selectedBlock == 'o' and o_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength))
                    or (selectedBlock == 'p' and p_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength))
                    or (selectedBlock == 'q' and q_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength))
                    # or (selectedBlock == 'r' and r_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength))
                    or (selectedBlock == 's' and s_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength))
                    # or (selectedBlock == 't' and t_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength))
                    # or (selectedBlock == 'u' and u_block.main(greenImage, greenRect, boardGreen, boardYellow, selectedDirection, xpos, ypos, surface, tileLength))
                    ):
                        whoTurn = checkBoard(GREEN)
                        selectedBlock, selectedDirection = selectBlockByCP()
                        selectPositionByCP(selectedBlock, selectedDirection, greenImage, greenRect, yellowImage, yellowRect)

                    else: print('ここには置けません')
                else: print('ここには置けません')

def selectBlockByCP():
    selectedBlock = 'a'
    selectedDirection = 0
    displayBlock(selectedBlock, selectedDirection)

    return selectedBlock, selectedDirection

def selectPositionByCP(selectedBlock, selectedDirection, greenImage, greenRect, yellowImage, yellowRect):
    while True:
        xpos = random.randint(1, 8)
        ypos = random.randint(1, 8)
        print(str(xpos) + ',' + str(ypos))
        if boardYellow[ypos][xpos] != CANTSET:
            if (
            (selectedBlock == 'a' and a_block.main(yellowImage, yellowRect, boardYellow, boardGreen, xpos, ypos, surface, tileLength))
            or (selectedBlock == 'b' and b_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength))
            or (selectedBlock == 'c' and c_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength))
            # or (selectedBlock == 'd' and d_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength))
            # or (selectedBlock == 'e' and e_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength))
            or (selectedBlock == 'f' and f_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength))
            or (selectedBlock == 'g' and g_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength))
            # or (selectedBlock == 'h' and h_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength))
            # or (selectedBlock == 'i' and i_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength))
            # or (selectedBlock == 'j' and j_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength))
            or (selectedBlock == 'k' and k_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength))
            or (selectedBlock == 'l' and l_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength))
            or (selectedBlock == 'm' and m_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength))
            or (selectedBlock == 'n' and n_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength))
            or (selectedBlock == 'o' and o_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength))
            or (selectedBlock == 'p' and p_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength))
            or (selectedBlock == 'q' and q_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength))
            # or (selectedBlock == 'r' and r_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength))
            or (selectedBlock == 's' and s_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength))
            # or (selectedBlock == 't' and t_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength))
            # or (selectedBlock == 'u' and u_block.main(yellowImage, yellowRect, boardYellow, boardGreen, selectedDirection, xpos, ypos, surface, tileLength))
            ):
                whoTurn = checkBoard(YELLOW)
                selectedBlock, selectedDirection = selectBlock()
                selectPositionByPlayer(selectedBlock, selectedDirection, greenImage, greenRect, yellowImage, yellowRect)

            else: print('ここには置けません')
        else: print('ここには置けません')

def displayBlock(selectedBlock, selectedDirection):
    if selectedBlock == 'a': a_block.display()
    elif selectedBlock == 'b': b_block.display(selectedDirection)
    elif selectedBlock == 'c': c_block.display(selectedDirection)
    # elif selectedBlock == 'd': d_block.display(selectedDirection)
    # elif selectedBlock == 'e': e_block.display(selectedDirection)
    elif selectedBlock == 'f': f_block.display(selectedDirection)
    elif selectedBlock == 'g': g_block.display(selectedDirection)
    # elif selectedBlock == 'h': h_block.display(selectedDirection)
    # elif selectedBlock == 'i': i_block.display(selectedDirection)
    # elif selectedBlock == 'j': j_block.display(selectedDirection)
    elif selectedBlock == 'k': k_block.display(selectedDirection)
    elif selectedBlock == 'l': l_block.display(selectedDirection)
    elif selectedBlock == 'm': m_block.display(selectedDirection)
    elif selectedBlock == 'n': n_block.display(selectedDirection)
    elif selectedBlock == 'o': o_block.display(selectedDirection)
    elif selectedBlock == 'p': p_block.display(selectedDirection)
    elif selectedBlock == 'q': q_block.display(selectedDirection)
    # elif selectedBlock == 'r': r_block.display(selectedDirection)
    elif selectedBlock == 's': s_block.display(selectedDirection)
    # elif selectedBlock == 't': t_block.display(selectedDirection)
    # elif selectedBlock == 'u': u_block.display(selectedDirection)

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
    selectPositionByPlayer(selectedBlock, selectedDirection, greenImage, greenRect, yellowImage, yellowRect)

if __name__ == '__main__':
    main()
