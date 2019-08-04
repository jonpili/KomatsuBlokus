import pygame
import sys
import numpy as np
from enum import Enum
from copy import deepcopy
import random

import Player

class Color(Enum):
    GREEN  = 0
    YELLOW = 1
    RED    = 2
    BLUE   = 3

class Game():
    TILE_NUMBER = 20 # 3の倍数 - 1
    TILE_LENGTH = 30

    # タイルの設置はボード外エラー回避の為2マス広く
    SCREEN_WIDTH  = TILE_LENGTH * (TILE_NUMBER + 2)
    SCREEN_HEIGHT = TILE_LENGTH * (TILE_NUMBER + 2)
    TILE_LIMIT    = TILE_LENGTH * TILE_NUMBER

    # ビューの設定
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    surface.fill((0,0,0)) # 黒で塗りつぶし

    TILE_IMAGES = {
        'DEFAULT': pygame.image.load('image30/tile.bmp').convert(),
        'GREEN':   pygame.image.load('image30/green.bmp').convert(),
        'YELLOW':  pygame.image.load('image30/yellow.bmp').convert(),
        'RED':     pygame.image.load('image30/red.bmp').convert(),
        'BLUE':    pygame.image.load('image30/blue.bmp').convert()
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
    pygame.display.flip()
    pygame.mouse.set_visible(True) #マウスポインターの表示をオン

    def __init__(self):
        self.question_player_number()
        self.question_CP_number()
        self.set_player_and_CP_number()
        self.current_player = self.players[Color.GREEN.value]
        self.game_record = []

    def question_player_number(self):
        player_number = int(input('プレイ人数を入力してください：'))
        while not player_number in [2, 4]:
            print('入力が間違っています')
            player_number = int(input('プレイ人数を入力してください：'))
        self.player_number = player_number

    def question_CP_number(self):
        CP_number = int(input('コンピュータの人数を入力してください：'))
        while not CP_number in range(self.player_number + 1):
            print('入力が間違っています')
            CP_number = int(input('コンピュータの人数を入力してください：'))
        self.CP_number = CP_number

    def set_player_and_CP_number(self):
        if self.player_number == 2:
            if self.CP_number == 0:
                self.players = [Player.Player(Color.GREEN, False), Player.Player(Color.YELLOW, False)]
            elif self.CP_number == 1:
                self.players = [Player.Player(Color.GREEN, True), Player.Player(Color.YELLOW, False)]
            elif self.CP_number == 2:
                self.players = [Player.Player(Color.GREEN, True), Player.Player(Color.YELLOW, True)]
            self.COLOR_LIST  = [Color.GREEN, Color.YELLOW]
            self.players[Color.GREEN.value].next_player   = self.players[Color.YELLOW.value]
            self.players[Color.YELLOW.value].next_player  = self.players[Color.GREEN.value]
        elif self.player_number == 4:
            if self.CP_number == 0:
                self.players = [Player.Player(Color.GREEN, False), Player.Player(Color.YELLOW, False), Player.Player(Color.RED, False), Player.Player(Color.BLUE, False)]
            elif self.CP_number == 1:
                self.players = [Player.Player(Color.GREEN, True), Player.Player(Color.YELLOW, False), Player.Player(Color.RED, False), Player.Player(Color.BLUE, False)]
            elif self.CP_number == 2:
                self.players = [Player.Player(Color.GREEN, True), Player.Player(Color.YELLOW, True), Player.Player(Color.RED, False), Player.Player(Color.BLUE, False)]
            elif self.CP_number == 3:
                self.players = [Player.Player(Color.GREEN, True), Player.Player(Color.YELLOW, True), Player.Player(Color.RED, True), Player.Player(Color.BLUE, False)]
            elif self.CP_number == 4:
                self.players = [Player.Player(Color.GREEN, True), Player.Player(Color.YELLOW, True), Player.Player(Color.RED, True), Player.Player(Color.BLUE, True)]
            self.COLOR_LIST  = [Color.GREEN, Color.YELLOW, Color.RED, Color.BLUE]
            self.players[Color.GREEN.value].next_player   = self.players[Color.YELLOW.value]
            self.players[Color.YELLOW.value].next_player  = self.players[Color.RED.value]
            self.players[Color.RED.value].next_player     = self.players[Color.BLUE.value]
            self.players[Color.BLUE.value].next_player    = self.players[Color.GREEN.value]

    def start(self, board):
        while not all([player.passed for player in self.players]):
            if not board.any_block_settable_check(self.current_player):
                self.current_player.pass_my_turn(self)
            else:
                block = self.current_player.start_my_turn(self, board)
                self.play(board, block)

    def play(self, board, block):
        player = self.current_player
        while player == self.current_player:
            if self.current_player.computer:
                self.set_block_on_click_position(board, block)
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
        if self.current_player.computer:
            xpos = random.randint(1, self.TILE_NUMBER) # 右方向に正
            ypos = random.randint(1, self.TILE_NUMBER) # 下方向に正
            print([xpos, ypos], end=' ')
        else:
            xpos = int(pygame.mouse.get_pos()[0]/self.TILE_LENGTH) # 右方向に正
            ypos = int(pygame.mouse.get_pos()[1]/self.TILE_LENGTH) # 下方向に正

        if board.settable_check(self.current_player.color, block.selected['shape'], xpos, ypos):
            board.change_status(self.current_player.color, block.selected['shape'], block.selected['influence'], xpos, ypos)
            self.change_image(board, block.selected['shape'], xpos, ypos)
            self.current_player.used_blocks.append(self.current_player.selected_shape_index)
            self.current_player.score += block.selected['score']
            record = deepcopy([board.status[self.current_player.color.value], self.current_player.color, self.current_player.selected_shape_index, self.current_player.selected_direction_index, xpos, ypos])
            self.game_record.append(record)
            self.change_turn()
        else:
            if not self.current_player.computer:
                print('ここには置けません')

    def change_image(self, board, block_shape, x, y):
        image = self.TILE_IMAGES[self.current_player.color.name]
        for coord in np.argwhere(block_shape == board.CANTSET):
            to_x = self.TILE_LENGTH * (x + coord[1] - 2)
            to_y = self.TILE_LENGTH * (y + coord[0] - 2)
            self.surface.blit(image, image.get_rect().move(to_x, to_y))
        pygame.display.flip()

    def change_turn(self):
        self.current_player = self.current_player.next_player

    def score_check(self):
        print('\nGame Finished!\n')
        for player in self.players:
            print(player.color.name + '\'s score is ' + str(player.score) + '.')
        print('')

        winner_score = max([player.score for player in self.players])
        winners = [player for player in self.players if player.score == winner_score]
        if len(winners) == 1:
            print('Winner is \"' + winners[0].color.name + '\"!!')
        else:
            winner_used_block_number = min([len(player.used_blocks) for player in winners])
            winners = [player for player in self.players if len(player.used_blocks) == winner_used_block_number]
            if len(winners) == 1:
                print('Winner is \"' + winners[0].color.name + '\"!!')
            else:
                print('It\'s a draw.')

        print('\nCongratulations!')
        winner_message = input()
