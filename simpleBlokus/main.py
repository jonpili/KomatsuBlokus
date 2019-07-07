import pygame
import sys

class Game():
    tileLength = 50
    tileNumber = 5

    BRANK   = 0 # ブロックは置かれていない
    CANTSET = 1 # ブロックが置かれている or 自分のブロックが隣接している
    ABLESET = 2 # 自分のブロックが角で接している

    GREEN  = 1
    YELLOW = 2

    # タイルの設置はボード外エラー回避の為2マス広く
    screenWidth  = tileLength * (tileNumber + 2)
    screenHeight = tileLength * (tileNumber + 2)
    tileLimit    = tileLength * tileNumber

    pygame.init()
    surface = pygame.display.set_mode((screenWidth, screenHeight))

    def __init__(self):
        self.surface.fill((0,0,0)) # 黒で塗りつぶし
        pygame.display.set_caption('Mini Blokus')

        self.tileImage   = pygame.image.load('image/tile.bmp').convert()
        self.GREENImage  = pygame.image.load('image/GREEN.bmp').convert()
        self.YELLOWImage = pygame.image.load('image/YELLOW.bmp').convert()

        self.tileRect   = self.tileImage.get_rect() # 画像と同じサイズの長方形座標を取得
        self.GREENRect  = self.GREENImage.get_rect()
        self.YELLOWRect = self.YELLOWImage.get_rect()

        pygame.mouse.set_visible(True) #マウスポインターの表示をオン

        # タイルで画面を埋める
        for i in range(0, self.tileLimit, self.tileLength):
            for j in range(0, self.tileLimit, self.tileLength):
                # 枠の分はスキップ
                self.surface.blit(self.tileImage, self.tileRect.move((i + self.tileLength), (j + self.tileLength)))

        # 初期位置を設定
        self.boardGREEN = self.makeBoard()
        self.boardGREEN[2][2] = self.ABLESET

        self.boardYELLOW = self.makeBoard()
        self.boardYELLOW[4][4] = self.ABLESET

    def makeBoard(self):
        board  = [[self.BRANK for width in range(self.tileNumber + 2)] for height in range(self.tileNumber + 2)]
        # 枠を作成
        for i in range(self.tileNumber + 2):
            board[0][i]              = self.CANTSET
            board[self.tileNumber + 1][i] = self.CANTSET
        for i in range(self.tileNumber):
            board[i + 1][0]              = self.CANTSET
            board[i + 1][self.tileNumber + 1] = self.CANTSET
        return board

    def start(self):
        whoTurn = self.checkBoard(self.GREEN)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit() # ESCAPEキーが押されたら終了
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # ボード外エラー回避の為1マス右下に
                    xpos = int(pygame.mouse.get_pos()[0]/self.tileLength) # 右方向に正
                    ypos = int(pygame.mouse.get_pos()[1]/self.tileLength) # 下方向に正

                block = PointBlock()
                    if whoTurn == self.GREEN:
                        if self.boardGREEN[ypos][xpos] != self.CANTSET:
                            block.pointBlock()
                            if self.pointBlock(xpos, ypos, self.GREEN, self.GREENImage, self.GREENRect):
                                whoTurn = self.checkBoard(self.YELLOW)

                    elif whoTurn == self.YELLOW:
                        if self.boardYELLOW[ypos][xpos] != self.CANTSET:
                            block.pointBlock()
                            if self.pointBlock(xpos, ypos, self.YELLOW, self.YELLOWImage, self.YELLOWRect):
                                whoTurn = self.checkBoard(self.GREEN)

    def checkBoard(self, color):
        print('')
        print('ーーーー緑の盤面ーーーー')
        for width in self.boardGREEN:
            print(width)
        print('ーーーー黄の盤面ーーーー')
        for width in self.boardYELLOW:
            print(width)

        if color == self.GREEN:
            print('＝＝＝緑色のターン＝＝＝')
        elif color == self.YELLOW:
            print('＝＝＝黄色のターン＝＝＝')

        pygame.display.flip()
        return color

class PointBlock():
    def pointBlock(self, x, y, color, colorImage, colorRect):
        if color == self.GREEN:
            if self.boardGREEN[y][x] == self.ABLESET:
                self.surface.blit(colorImage, colorRect.move(self.tileLength * x, self.tileLength * y))
                self.changeTileStatus(x, y, self.boardGREEN, self.boardYELLOW)
                return True

        elif color == self.YELLOW:
            if self.boardYELLOW[y][x] == self.ABLESET:
                self.surface.blit(colorImage, colorRect.move(self.tileLength * x, self.tileLength * y))
                self.changeTileStatus(x, y, self.boardYELLOW, self.boardGREEN)
                return True

    def changeTileStatus(self, x, y, board1, board2):
        # ブロック自体を左上から時計回りに
        board1[y][x] = self.CANTSET

        # ブロックと辺で接する地点を左上から時計回りに
        board1[y][x-1] = self.CANTSET
        board1[y-1][x] = self.CANTSET
        board1[y][x+1] = self.CANTSET
        board1[y+1][x] = self.CANTSET

        # ブロックと角で接する地点を左上から時計回りに
        if board1[y-1][x-1] != self.CANTSET:
            board1[y-1][x-1] = self.ABLESET

        if board1[y-1][x+1] != self.CANTSET:
            board1[y-1][x+1] = self.ABLESET

        if board1[y+1][x+1] != self.CANTSET:
            board1[y+1][x+1] = self.ABLESET

        if board1[y+1][x-1] != self.CANTSET:
            board1[y+1][x-1] = self.ABLESET

        # ブロック自体を左上から時計回りに
        board2[y][x] = self.CANTSET

def main():
    game = Game()
    print('＝＝＝＝＝ゲーム開始＝＝＝＝＝')
    game.start()
    pointBlock = pointBlock()
    pointBlock.pointBlock()


if __name__ == '__main__':
    main()
