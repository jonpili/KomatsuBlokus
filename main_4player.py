import Game_4player
import Board_4player

def main():
    game  = Game_4player.Game()
    board = Board_4player.Board(game)
    game.start(board)
    game.score_check()

if __name__ == '__main__':
    main()
