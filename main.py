import pygame
import sys
import re
import numpy as np

import Game
import Player
import Board

# TODO: Playerクラスのプロパティから引っ張ってくる
turn_passed_list = [False, False] # GREEN, YELLOWの順番

# TODO: Gameクラスのプロパティから引っ張ってくる
GREEN  = 'green'
YELLOW = 'yellow'
RED    = 'red' # 将来的に実装
BLUE   = 'blue' # 将来的に実装

# TODO: Gameクラスのプロパティから引っ張ってくる
TILE_NUMBER = 8

def start(game, board):
    player1 = Player.Player(GREEN)
    player2 = Player.Player(YELLOW)
    # ゲームスタート処理
    board.check_status(game, turn_passed_list)
    block = player1.select_block(board)
    block = player1.block_usable_check(board, block)

    while True:
        for event in pygame.event.get():
            # ESCAPEキーが押されたらゲーム終了
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # Zキーが押されたらブロック選択キャンセル
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                if game.who_turn == GREEN:
                    block = player1.cancel_selected(board, block)
                elif game.who_turn == YELLOW:
                    block = player2.cancel_selected(board, block)
            # クリックしたらブロックを配置
            elif event.type == pygame.MOUSEBUTTONDOWN:
                xpos = int(pygame.mouse.get_pos()[0]/game.TILE_LENGTH) # 右方向に正
                ypos = int(pygame.mouse.get_pos()[1]/game.TILE_LENGTH) # 下方向に正
                if game.who_turn == GREEN:
                    if board.settable_check(block.selected['shape'], board.green_board, xpos, ypos):
                        board.change_status(block.selected['shape'], block.selected['influence'], board.green_board, board.yellow_board, xpos, ypos)
                        board.change_image(block.selected['shape'], game.GREEN_IMAGE, game.GREEN_RECT, xpos, ypos, game.surface, game.TILE_LENGTH)
                        game.who_turn = YELLOW
                        board.check_status(game, turn_passed_list)
                        block = player2.select_block(board)
                        block = player2.block_usable_check(board, block)
                    else: print('ここには置けません')

                elif game.who_turn == YELLOW:
                    if board.settable_check(block.selected['shape'], board.yellow_board, xpos, ypos):
                        board.change_status(block.selected['shape'], block.selected['influence'], board.yellow_board, board.green_board, xpos, ypos)
                        board.change_image(block.selected['shape'], game.YELLOW_IMAGE, game.YELLOW_RECT, xpos, ypos, game.surface, game.TILE_LENGTH)
                        game.who_turn = GREEN
                        board.check_status(game, turn_passed_list)
                        block = player1.select_block(board)
                        block = player1.block_usable_check(board, block)
                    else: print('ここには置けません')

def main():
    game  = Game.Game(GREEN)
    board = Board.Board(game.TILE_NUMBER)
    start(game, board)

if __name__ == '__main__':
    main()
