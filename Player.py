import Block
import random

class Player():
    block_shape_index_list     = [chr(ord('a') + i) for i in range(21)] # aからuの配列
    block_direction_index_list = [str(n) for n in range(8)] # 0から7の配列

    def __init__(self, enum, boolean):
        self.color = enum
        self.computer = boolean
        self.passed = False
        self.used_blocks = []
        self.usable_blocks = []
        self.selected_shape_index = ''
        self.selected_direction_index = ''
        self.score = 0

    def pass_my_turn(self, game):
        print('＝＝＝＝＝＝＝＝＝＝' + game.current_player.color.name + '\'s Turn＝＝＝＝＝＝＝＝＝＝')
        print('置けるブロックが存在しないためパスとなります\n')
        game.change_turn()

    def start_my_turn(self, game, board):
        board.check_status(game)
        if self.computer: block = self.select_block_by_CP(board)
        else:             block = self.select_block(board)

        while not board.settable_area_exist_check(self.color, block.selected['shape']):
            print('そのブロックを置く場所がありません\n')
            if self.computer: block = self.select_block_by_CP(board)
            else:             block = self.select_block(board)
        return block

    def select_block(self, board):
        print('手持ちのブロックリスト')
        print([i for i in self.block_shape_index_list if i not in self.used_blocks])
        self.selected_shape_index = input('\nブロックを選択してください：')
        while True:
            if self.check_input(board):
                break

        self.selected_direction_index = input('向きを選択してください：')
        while not self.selected_direction_index in self.block_direction_index_list:
            print('入力が間違っています')
            self.selected_direction_index = input('向きを選択してください：')
        self.selected_direction_index = int(self.selected_direction_index)

        block = Block.Block(self.selected_shape_index, self.selected_direction_index, True)
        return block

    def select_block_by_CP(self, board):
        self.selected_shape_index = random.choice(self.usable_blocks)
        self.selected_direction_index = random.choice(range(8))

        block = Block.Block(self.selected_shape_index, self.selected_direction_index, True)
        return block

    def check_input(self, board):
        if self.selected_shape_index in self.used_blocks:
            print('そのブロックは既に使っています\n')
            self.selected_shape_index = input('ブロックを選択してください：')
            return False
        elif not self.selected_shape_index in self.block_shape_index_list:
            print('入力が間違っています\n')
            self.selected_shape_index = input('ブロックを選択してください：')
            return False
        else:
            return True

    def cancel_selected(self, game, board):
        print('\n選択がキャンセルされました\n')
        block = self.start_my_turn(game, board)
        return block
