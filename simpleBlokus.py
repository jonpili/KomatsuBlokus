import pygame
import sys

tileLength = 50
tileNumber = 5

BLANK   = 0 # ブロックは置かれていない
CANTSET = 1 # ブロックが置かれている or 自分のブロックが隣接している
ABLESET = 2 # 自分のブロックが角で接している

GREEN  = 1
YELLOW = 2

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
    return board

# 初期位置を設定
boardGreen = makeBoard()
boardGreen[2][2] = ABLESET

boardYellow = makeBoard()
boardYellow[4][4] = ABLESET

surface = pygame.display.set_mode((screenWidth, screenHeight))

def changeTileStatus(x, y, board1, board2):
    # ブロック自体を左上から時計回りに
    board1[y][x] = CANTSET

    # ブロックと辺で接する地点を左上から時計回りに
    board1[y][x-1] = CANTSET
    board1[y-1][x] = CANTSET
    board1[y][x+1] = CANTSET
    board1[y+1][x] = CANTSET

    # ブロックと角で接する地点を左上から時計回りに
    if board1[y-1][x-1] != CANTSET:
        board1[y-1][x-1] = ABLESET

    if board1[y-1][x+1] != CANTSET:
        board1[y-1][x+1] = ABLESET

    if board1[y+1][x+1] != CANTSET:
        board1[y+1][x+1] = ABLESET

    if board1[y+1][x-1] != CANTSET:
        board1[y+1][x-1] = ABLESET

    # ブロック自体を左上から時計回りに
    board2[y][x] = CANTSET

def pointBlock(x, y, color, colorImage, colorRect):
    if color == GREEN:
        if boardGreen[y][x] == ABLESET:
            surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * y))
            changeTileStatus(x, y, boardGreen, boardYellow)
            return True

    elif color == YELLOW:
        if boardYellow[y][x] == ABLESET:
            surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * y))
            changeTileStatus(x, y, boardYellow, boardGreen)
            return True

class Game():
    def __init__(self):
        pygame.init()
        surface.fill((0,0,0)) # 黒で塗りつぶし
        pygame.display.set_caption('Mini Blokus')

        self.tileImage   = pygame.image.load('tile.bmp').convert()
        self.greenImage  = pygame.image.load('green.bmp').convert()
        self.yellowImage = pygame.image.load('yellow.bmp').convert()

        self.tileRect   = self.tileImage.get_rect() # 画像と同じサイズの長方形座標を取得
        self.greenRect  = self.greenImage.get_rect()
        self.yellowRect = self.yellowImage.get_rect()

        pygame.mouse.set_visible(True) #マウスポインターの表示をオン

        # タイルで画面を埋める
        for i in range(0, tileLimit, tileLength):
            for j in range(0, tileLimit, tileLength):
                # 枠の分はスキップ
                surface.blit(self.tileImage, self.tileRect.move((i + tileLength), (j + tileLength)))

    def start(self):
        whoTurn = self.checkBoard(GREEN)

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
                            if pointBlock(xpos, ypos, GREEN, self.greenImage, self.greenRect):
                                whoTurn = self.checkBoard(YELLOW)

                    elif whoTurn == YELLOW:
                        if boardYellow[ypos][xpos] != CANTSET:
                            if pointBlock(xpos, ypos, YELLOW, self.yellowImage, self.yellowRect):
                                whoTurn = self.checkBoard(GREEN)

    def checkBoard(self, color):
        print('')
        print('ーーーー緑の盤面ーーーー')
        for width in boardGreen:
            print(width)
        print('ーーーー黄の盤面ーーーー')
        for width in boardYellow:
            print(width)

        if color == GREEN:
            print('＝＝＝緑色のターン＝＝＝')
        elif color == YELLOW:
            print('＝＝＝黄色のターン＝＝＝')

        pygame.display.flip()
        return color

def main():
    game = Game()
    print('＝＝＝＝＝ゲーム開始＝＝＝＝＝')
    game.start()

if __name__ == '__main__':
    main()
