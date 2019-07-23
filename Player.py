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

        block = Block.Block(self.selected_shape_index, self.selected_direction_index)
        self.used_blocks.append(self.selected_shape_index)

        return block

    def check_input(self, board):
        if self.selected_shape_index in self.used_blocks or not self.selected_shape_index in self.block_shape_index_list:
            if self.selected_shape_index in self.used_blocks:
                print('そのブロックは既に使っています\n')
                self.selected_shape_index = input('ブロックを選択してください：')
            else:
                # # Xキーが入力されたらターンスキップ
                # if self.selected_shape_index == 'x':
                #     if self.color == GREEN:
                #         turn_passed_list[0] = True
                #     elif self.color == YELLOW:
                #         turn_passed_list[1] = True
                #
                #     if self.score_check():
                #         sys.exit()
                #     else:
                #         block = self.pass_my_turn(board)
                #         self.passed = True
                # else:
                #     print('入力が間違っています\n')
                #     self.selected_shape_index = input('ブロックを選択してください：')
                print('入力が間違っています\n')
                self.selected_shape_index = input('ブロックを選択してください：')
            return False
        else:
            return True

    def cancel_selected(self, board, block):
        print('\n選択がキャンセルされました\n')
        self.used_blocks.pop()
        block = self.select_block(board)
        block = self.block_usable_check(board, block)
        return block

    # def pass_my_turn(self, board):
    #     if self.color == GREEN:
    #         game.who_turn = YELLOW
    #     elif self.color == YELLOW:
    #         game.who_turn = GREEN
    #
    #     print('\n＝＝＝＝＝' + game.who_turn + '\'s Turn＝＝＝＝＝')
    #     print('相手がパスしました\n')
    #
    #     if self.select_block(board)
    #     block = self.select_block(board)
    #     block = self.block_usable_check(board, block)
    #
    #     return block

    def block_usable_check(self, board, block):
        while not board.settable_area_exist_check(block.selected['shape'], eval('board.' + self.color + '_board')):
            print('そのブロックを置く場所がありません\n')
            self.used_blocks.pop()
            block = self.select_block(board)
        return block

    # def score_check(self):
    #     if all(turn_passed_list):
    #         #スコアチェック
    #         greenRemainingBlock = list(set(self.block_shape_index_list) - set(greenUsedBlocks))
    #         yellowRemainingBlock = list(set(self.block_shape_index_list) - set(yellowUsedBlocks))
    #         greenScore = sum(list(map(lambda alphabet: scoreTable[alphabet], greenRemainingBlock)))
    #         yellowScore = sum(list(map(lambda alphabet: scoreTable[alphabet], yellowRemainingBlock)))
    #         #結果発表
    #         print('ゲームは終了です')
    #         print('緑色の点数は' + str(greenScore) + '点です')
    #         print('黄色の点数は' + str(yellowScore) + '点です')
    #
    #         if greenScore < yellowScore:
    #             print('勝者は「緑色」です')
    #         elif greenScore > yellowScore:
    #             print('勝者は「黄色」です')
    #         else:
    #             if len(greenRemainingBlock) < len(yellowRemainingBlock):
    #                 print('勝者は「緑色」です')
    #             elif len(greenRemainingBlock) > len(yellowRemainingBlock):
    #                 print('勝者は「黄色」です')
    #             else:
    #                 print('引き分けです')
    #
    #         turn_passed_list[0] = False
    #         return True
    #     else:
    #         return False
