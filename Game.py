import pygame
import sys
import numpy as np

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

    TILE_IMAGES = {
        'default': pygame.image.load('image/tile.bmp').convert(),
        'green': pygame.image.load('image/green.bmp').convert(),
        'yellow': pygame.image.load('image/yellow.bmp').convert()
    }

    # タイルで画面を埋める
    image = TILE_IMAGES['default']
    for i in range(0, TILE_LIMIT, TILE_LENGTH):
        for j in range(0, TILE_LIMIT, TILE_LENGTH):
            # 枠の分はスキップ
            surface.blit(image, image.get_rect().move((i + TILE_LENGTH), (j + TILE_LENGTH)))

    # pygameの初期設定
    pygame.init()
    pygame.display.set_caption('Komatsu Blokus')
    pygame.mouse.set_visible(True) #マウスポインターの表示をオン

    def start(self, board):
        player_green  = Player.Player(self.GREEN)
        player_yellow = Player.Player(self.YELLOW)
        player_green.next_player  = player_yellow
        player_yellow.next_player = player_green
        # ゲームスタート処理
        self.current_player = player_green
        board.check_status(self)

        while True:
            if board.any_block_settable_check():
                self.current_player.pass_my_turn(self)
            else:
                block = self.current_player.start_my_turn(self, board)
                self.play(board, block)

    def play(self, board, block):
        player = self.current_player
        while player == self.current_player:
            for event in pygame.event.get():
                # ESCAPEキーが押されたらゲーム終了
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # Zキーが押されたらブロック選択キャンセル
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                    block = self.current_player.cancel_selected(self, board)
                # クリックしたらブロックを配置
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    xpos = int(pygame.mouse.get_pos()[0]/self.TILE_LENGTH) # 右方向に正
                    ypos = int(pygame.mouse.get_pos()[1]/self.TILE_LENGTH) # 下方向に正
                    if board.settable_check(self.current_player.color, block.selected['shape'], xpos, ypos):
                        board.change_status(self.current_player.color, block.selected['shape'], block.selected['influence'], xpos, ypos)
                        self.current_player.used_blocks.append(self.current_player.selected_shape_index)
                        self.current_player.score += block.score['score']
                        self.change_image(board, block.selected['shape'], xpos, ypos)
                        self.change_turn()
                    else: print('ここには置けません')

    def change_turn(self):
        self.current_player = self.current_player.next_player
        print(self.current_player.color)

    def change_image(self, board, block_shape, x, y):
        image = self.TILE_IMAGES[self.current_player.color]
        for coord in np.argwhere(block_shape == board.CANTSET):
            to_x = self.TILE_LENGTH * (x + coord[1] - 2)
            to_y = self.TILE_LENGTH * (y + coord[0] - 2)
            self.surface.blit(image, image.get_rect().move(to_x, to_y))
