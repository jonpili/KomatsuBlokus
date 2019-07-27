import Block

class Player():
    block_shape_index_list     = [chr(ord('a') + i) for i in range(21)] # aからuの配列
    block_direction_index_list = [str(n) for n in range(8)] # 0から7の配列

    def __init__(self, color):
        self.color = color
        self.passed = False
        self.used_blocks = []
        self.selected_shape_index = ''
        self.selected_direction_index = ''
        self.score = 0

    def pass_my_turn(self, game):
        print('＝＝＝＝＝＝＝＝＝＝' + game.current_player.color + '\'s Turn＝＝＝＝＝＝＝＝＝＝')
        print('置けるブロックが存在しないためパスとなります')
        game.change_turn()

    def start_my_turn(self, game, board):
        board.check_status(game)
        block = self.select_block(board)
        while not board.settable_area_exist_check(self.color, block.selected['shape']):
            print('そのブロックを置く場所がありません\n')
            block = self.select_block(board)
        return block

    def select_block(self, board):
        print('手持ちのブロックリスト')
        print([i for i in self.block_shape_index_list if i not in self.used_blocks])
        print('')
        self.selected_shape_index = input('ブロックを選択してください：')
        while True:
            if self.check_input(board):
                break

        if not self.passed:
            self.selected_direction_index = input('向きを選択してください：')
            while not self.selected_direction_index in self.block_direction_index_list:
                print('入力が間違っています')
                self.selected_direction_index = input('向きを選択してください：')
            self.selected_direction_index = int(self.selected_direction_index)

        block = Block.Block(self.selected_shape_index, self.selected_direction_index, True)

        return block

    def check_input(self, board):
        if self.selected_shape_index in self.used_blocks or not self.selected_shape_index in self.block_shape_index_list:
            if self.selected_shape_index in self.used_blocks:
                print('そのブロックは既に使っています\n')
                self.selected_shape_index = input('ブロックを選択してください：')
            else:
                print('入力が間違っています\n')
                self.selected_shape_index = input('ブロックを選択してください：')
            return False
        else:
            return True

    def cancel_selected(self, game, board):
        print('\n選択がキャンセルされました\n')
        block = self.start_my_turn(game, board)
        return block

    def score_check(self, player_green, player_yellow):
        #スコアチェック
        greenScore = 89 - player_green.score
        yellowScore = 89 - player_yellow.score
        #結果発表
        print('ゲームは終了です')
        print('緑色の点数は' + str(greenScore) + '点です')
        print('黄色の点数は' + str(yellowScore) + '点です')

        if greenScore < yellowScore:
            print('勝者は「緑色」です')
        elif greenScore > yellowScore:
            print('勝者は「黄色」です')
        else:
            if len(player_green.used_blocks) < len(player_yellow.used_blocks):
                print('勝者は「緑色」です')
            elif len(player_green.used_blocks) > len(player_yellow.used_blocks):
                print('勝者は「黄色」です')
            else:
                print('引き分けです')