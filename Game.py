import pygame
import numpy as np

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
    pygame.display.set_caption('Mini Blokus')
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
