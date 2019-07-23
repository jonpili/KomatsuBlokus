import pygame
#TODO　3つのメソッドを作る
class Game():
    TILE_NUMBER = 8
    TILE_LENGTH = 50

    GREEN  = 'green'
    YELLOW = 'yellow'
    RED    = 'red' # 将来的に実装
    BLUE   = 'blue' # 将来的に実装

    # タイルの設置はボード外エラー回避の為2マス広く
    SCREEN_WIDTH  = TILE_LENGTH * (TILE_NUMBER + 2)
    SCREEN_HEIGHT = TILE_LENGTH * (TILE_NUMBER + 2)
    TILE_LIMIT    = TILE_LENGTH * TILE_NUMBER

    # ビューの設定
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    surface.fill((0,0,0)) # 黒で塗りつぶし

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

    # pygameの初期設定
    pygame.init()
    pygame.display.set_caption('Komatsu Blokus')
    pygame.mouse.set_visible(True) #マウスポインターの表示をオン

    def __init__(self, color):
        self.who_turn = color
