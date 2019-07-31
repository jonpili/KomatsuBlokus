import Game
import Board

def main():
    game  = Game.Game()
    board = Board.Board(game)
    # game.check_player_number()
    game.start(board)
    game.score_check()

if __name__ == '__main__':
    main()
