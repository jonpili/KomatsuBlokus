import Game
import Board

def main():
    game  = Game.Game('green')
    board = Board.Board(game.TILE_NUMBER)
    game.start(board)

if __name__ == '__main__':
    main()
