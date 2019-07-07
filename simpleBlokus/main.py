import pygame
import sys
import Start

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

def main():
    game = Game()
    start = Start.Start()
    print('＝＝＝＝＝ゲーム開始＝＝＝＝＝')
    start.main(game)

if __name__ == '__main__':
    main()
