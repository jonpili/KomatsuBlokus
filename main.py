import Game
import Board

def main():
    game  = Game.Game()
    board = Board.Board(game)
    game.start(board)
    game.score_check()
    return game.game_record

if __name__ == '__main__':
    main()
