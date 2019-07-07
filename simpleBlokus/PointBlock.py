class PointBlock():
    def pointBlock(self, game, x, y, color):
        if color == game.GREEN:
            if game.boardGREEN[y][x] == game.ABLESET:
                game.surface.blit(game.GREENImage, game.GREENRect.move(game.tileLength * x, game.tileLength * y))
                self.changeTileStatus(game, x, y, game.boardGREEN, game.boardYELLOW)
                return True

        elif color == game.YELLOW:
            if game.boardYELLOW[y][x] == game.ABLESET:
                game.surface.blit(game.YELLOWImage, game.YELLOWRect.move(game.tileLength * x, game.tileLength * y))
                self.changeTileStatus(game, x, y, game.boardYELLOW, game.boardGREEN)
                return True

    def changeTileStatus(self, game, x, y, board1, board2):
        # ブロック自体を左上から時計回りに
        board1[y][x] = game.CANTSET

        # ブロックと辺で接する地点を左上から時計回りに
        board1[y][x-1] = game.CANTSET
        board1[y-1][x] = game.CANTSET
        board1[y][x+1] = game.CANTSET
        board1[y+1][x] = game.CANTSET

        # ブロックと角で接する地点を左上から時計回りに
        if board1[y-1][x-1] != game.CANTSET:
            board1[y-1][x-1] = game.ABLESET

        if board1[y-1][x+1] != game.CANTSET:
            board1[y-1][x+1] = game.ABLESET

        if board1[y+1][x+1] != game.CANTSET:
            board1[y+1][x+1] = game.ABLESET

        if board1[y+1][x-1] != game.CANTSET:
            board1[y+1][x-1] = game.ABLESET

        # ブロック自体を左上から時計回りに
        board2[y][x] = game.CANTSET
