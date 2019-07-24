import pygame
import sys

import Player

class Game():
    TILE_NUMBER = 8
    TILE_LENGTH = 50

    GREEN  = 'green'
    YELLOW = 'yellow'
    RED    = 'red' # 将来的に実装
    BLUE   = 'blue' # 将来的に実装

    COLOR_LIST  = [GREEN, YELLOW]

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

    def start(self, board):
        player_green = Player.Player(self.GREEN)
        player_yellow = Player.Player(self.YELLOW)
        # ゲームスタート処理
        board.check_status(self)
        block = player_green.select_block(board)
        block = player_green.block_usable_check(board, block, self.who_turn)

        while True:
            for event in pygame.event.get():
                player_green, player_yellow, board, block = self.play(player_green, player_yellow, board, block, event)

    def play(self, player_green, player_yellow, board, block, event):
        # ESCAPEキーが押されたらゲーム終了
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        # Zキーが押されたらブロック選択キャンセル
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            if self.who_turn == self.GREEN:
                block = player_green.cancel_selected(board, block, self.who_turn)
            elif self.who_turn == self.YELLOW:
                block = player_yellow.cancel_selected(board, block, self.who_turn)
        # クリックしたらブロックを配置
        elif event.type == pygame.MOUSEBUTTONDOWN:
            xpos = int(pygame.mouse.get_pos()[0]/self.TILE_LENGTH) # 右方向に正
            ypos = int(pygame.mouse.get_pos()[1]/self.TILE_LENGTH) # 下方向に正
            if board.settable_check(self.who_turn, block.selected['shape'], xpos, ypos):
                board.change_status(self.who_turn, block.selected['shape'], block.selected['influence'], xpos, ypos)
                board.change_image(block.selected['shape'], eval('self.' + self.who_turn.upper() + '_IMAGE'), eval('self.' + self.who_turn.upper() + '_RECT'), xpos, ypos, self.surface, self.TILE_LENGTH)

                self.change_turn()
                board.check_status(self)
                block = eval('player_' + self.who_turn).select_block(board)
                block = eval('player_' + self.who_turn).block_usable_check(board, block, self.who_turn)
            else: print('ここには置けません')
        return player_green, player_yellow, board, block

    def change_turn(self):
        color_number = self.COLOR_LIST.index(self.who_turn)
        color_number += 1
        if color_number == len(self.COLOR_LIST):
            color_number -= len(self.COLOR_LIST)

        self.who_turn = self.COLOR_LIST[color_number]
        print(self.who_turn)
