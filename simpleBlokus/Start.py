import pygame
import PointBlock

class Start():
    def main(self, game):
        whoTurn = self.checkBoard(game, game.GREEN)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit() # ESCAPEキーが押されたら終了
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # ボード外エラー回避の為1マス右下に
                    xpos = int(pygame.mouse.get_pos()[0]/game.tileLength) # 右方向に正
                    ypos = int(pygame.mouse.get_pos()[1]/game.tileLength) # 下方向に正

                    block = PointBlock.PointBlock()

                    if whoTurn == game.GREEN:
                        if game.boardGREEN[ypos][xpos] != game.CANTSET:
                            if block.pointBlock(game, xpos, ypos, game.GREEN):
                                whoTurn = self.checkBoard(game, game.YELLOW)

                    elif whoTurn == game.YELLOW:
                        if game.boardYELLOW[ypos][xpos] != game.CANTSET:
                            if block.pointBlock(game, xpos, ypos, game.YELLOW):
                                whoTurn = self.checkBoard(game, game.GREEN)

    def checkBoard(self, game, color):
        print('')
        print('ーーーー緑の盤面ーーーー')
        for width in game.boardGREEN:
            print(width)
        print('ーーーー黄の盤面ーーーー')
        for width in game.boardYELLOW:
            print(width)

        if color == game.GREEN:
            print('＝＝＝緑色のターン＝＝＝')
        elif color == game.YELLOW:
            print('＝＝＝黄色のターン＝＝＝')

        pygame.display.flip()
        return color
