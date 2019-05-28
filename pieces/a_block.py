BLANK   = 0
CANTSET = 1
ABLESET = 2

GREEN  = 1
YELLOW = 2

def changeTileStatus(boardMine, boardOpponent, x, y):
    # ブロック自体を左上から時計回りに
    boardMine[y][x] = CANTSET

    # ブロックと辺で接する地点を左上から時計回りに
    boardMine[y][x-1] = CANTSET
    boardMine[y-1][x] = CANTSET
    boardMine[y][x+1] = CANTSET
    boardMine[y+1][x] = CANTSET

    # ブロックと角で接する地点を左上から時計回りに
    if boardMine[y-1][x-1] != CANTSET:
        boardMine[y-1][x-1] = ABLESET

    if boardMine[y-1][x+1] != CANTSET:
        boardMine[y-1][x+1] = ABLESET

    if boardMine[y+1][x+1] != CANTSET:
        boardMine[y+1][x+1] = ABLESET

    if boardMine[y+1][x-1] != CANTSET:
        boardMine[y+1][x-1] = ABLESET

    # ブロック自体を左上から時計回りに
    boardOpponent[y][x] = CANTSET

def changeTileImage(colorImage, colorRect, x, y, surface, tileLength):
    surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * y))

def main(colorImage, colorRect, boardMine, boardOpponent, x, y, surface, tileLength):
    if boardMine[y][x] == ABLESET:
        changeTileImage(colorImage, colorRect, x, y, surface, tileLength)
        changeTileStatus(boardMine, boardOpponent, x, y)
        return True

if __name__ == '__main__':
    main()
