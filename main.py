import Game
import Board

def main():
    player_number = question_player_number()
    CP_number     = question_CP_number(player_number)

    game  = Game.Game(player_number, CP_number)
    board = Board.Board(game)
    game.start(board)
    game.score_check()

def question_player_number():
    player_number = int(input('プレイ人数を入力してください：'))
    while not player_number in [2, 4]:
        print('入力が間違っています')
        player_number = int(input('プレイ人数を入力してください：'))
    return player_number

def question_CP_number(player_number):
    CP_number = int(input('コンピュータの人数を入力してください：'))
    while not CP_number in range(player_number + 1):
        print('入力が間違っています')
        CP_number = int(input('コンピュータの人数を入力してください：'))
    return CP_number

if __name__ == '__main__':
    main()
