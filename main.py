import Game
import Board

def main():
    game  = Game.Game('green')
    board = Board.Board(game)
    game.start(board)

if __name__ == '__main__':
    main()
