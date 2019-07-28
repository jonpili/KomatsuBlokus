import pygame
import sys
import numpy as np
from enum import Enum
import random

import Player

class Color(Enum):
    GREEN  = 0
    YELLOW = 1
    RED    = 2
    BLUE   = 3

class Game():
    TILE_NUMBER = 8
    TILE_LENGTH = 50

    COLOR_LIST  = [Color.GREEN, Color.YELLOW]

    # タイルの設置はボード外エラー回避の為2マス広く
    SCREEN_WIDTH  = TILE_LENGTH * (TILE_NUMBER + 2)
    SCREEN_HEIGHT = TILE_LENGTH * (TILE_NUMBER + 2)
    TILE_LIMIT    = TILE_LENGTH * TILE_NUMBER

    # ビューの設定
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    surface.fill((0,0,0)) # 黒で塗りつぶし

    TILE_IMAGES = {
        'DEFAULT': pygame.image.load('image/tile.bmp').convert(),
        'GREEN': pygame.image.load('image/green.bmp').convert(),
        'YELLOW': pygame.image.load('image/yellow.bmp').convert()
    }

    # タイルで画面を埋める
    image = TILE_IMAGES['DEFAULT']
    for i in range(0, TILE_LIMIT, TILE_LENGTH):
        for j in range(0, TILE_LIMIT, TILE_LENGTH):
            # 枠の分はスキップ
            surface.blit(image, image.get_rect().move((i + TILE_LENGTH), (j + TILE_LENGTH)))

    # pygameの初期設定
    pygame.init()
    pygame.display.set_caption('Komatsu Blokus')
    pygame.mouse.set_visible(True) #マウスポインターの表示をオン

    def __init__(self):
        self.player_green  = Player.Player(Color.GREEN, False)
        self.player_yellow = Player.Player(Color.YELLOW, True)
        self.player_green.next_player  = self.player_yellow
        self.player_yellow.next_player = self.player_green
        self.current_player = self.player_green

    def start(self, board):
        while True:
            if all([player.passed for player in [self.player_green, self.player_yellow]]):
                self.score_check(self.player_green, self.player_yellow)
                break
            elif not board.any_block_settable_check(self.current_player):
                self.current_player.pass_my_turn(self)
            else:
                block = self.current_player.start_my_turn(self, board)
                self.play(board, block)

    def play(self, board, block):
        player = self.current_player
        while player == self.current_player:
            if self.current_player.computer:
                self.set_block_on_click_position_by_CP(board, block)
                break
            else:
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
                        self.set_block_on_click_position(board, block)

    def set_block_on_click_position(self, board, block):
        xpos = int(pygame.mouse.get_pos()[0]/self.TILE_LENGTH) # 右方向に正
        ypos = int(pygame.mouse.get_pos()[1]/self.TILE_LENGTH) # 下方向に正
        if board.settable_check(self.current_player.color, block.selected['shape'], xpos, ypos):
            board.change_status(self.current_player.color, block.selected['shape'], block.selected['influence'], xpos, ypos)
            self.change_image(board, block.selected['shape'], xpos, ypos)
            self.current_player.used_blocks.append(self.current_player.selected_shape_index)
            self.current_player.score += block.selected['score']
            self.change_turn()
        else: print('ここには置けません')

    def set_block_on_click_position_by_CP(self, board, block):
        xpos = random.randint(0, 7) # 右方向に正
        ypos = random.randint(0, 7) # 下方向に正
        print([xpos, ypos])
        if board.settable_check(self.current_player.color, block.selected['shape'], xpos, ypos):
            board.change_status(self.current_player.color, block.selected['shape'], block.selected['influence'], xpos, ypos)
            self.change_image(board, block.selected['shape'], xpos, ypos)
            self.current_player.used_blocks.append(self.current_player.selected_shape_index)
            self.current_player.score += block.selected['score']
            self.change_turn()
        else:
            print('ここには置けません')

    def change_image(self, board, block_shape, x, y):
        image = self.TILE_IMAGES[self.current_player.color.name]
        for coord in np.argwhere(block_shape == board.CANTSET):
            to_x = self.TILE_LENGTH * (x + coord[1] - 2)
            to_y = self.TILE_LENGTH * (y + coord[0] - 2)
            self.surface.blit(image, image.get_rect().move(to_x, to_y))

    def change_turn(self):
        self.current_player = self.current_player.next_player

    def score_check(self, player_green, player_yellow):
        print('ゲームは終了です')
        print('緑色の点数は ' + str(player_green.score) + ' 点です')
        print('黄色の点数は ' + str(player_yellow.score) + ' 点です')

        if player_green.score > player_yellow.score:
            print('勝者は「緑色」です')
        elif player_green.score < player_yellow.score:
            print('勝者は「黄色」です')
        else:
            if len(player_green.used_blocks) < len(player_yellow.used_blocks):
                print('勝者は「緑色」です')
            elif len(player_green.used_blocks) > len(player_yellow.used_blocks):
                print('勝者は「黄色」です')
            else:
                print('引き分けです')
