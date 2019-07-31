import Game
import Board

def main():
    player_number = question_player_number()

    game  = Game.Game(player_number)
    board = Board.Board(game)
    game.start(board)
    game.score_check()

def question_player_number():
    player_number = int(input('プレイ人数を入力してください：'))
    while not player_number in [2, 4]:
        print('入力が間違っています')
        player_number = int(input('プレイ人数を入力してください：'))
    return player_number

if __name__ == '__main__':
    main()
