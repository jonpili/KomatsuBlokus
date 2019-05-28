BLANK   = 0
CANTSET = 1
ABLESET = 2

GREEN  = 1
YELLOW = 2

def changeTileStatus1(colorImage, colorRect, x, y, boardMine, boardOpponent, surface, tileLength):
    surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * y))
    surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * (y-1)))
    surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * (y-2)))
    surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * (y+1)))
    surface.blit(colorImage, colorRect.move(tileLength * (x-1), tileLength * (y+1)))

    # ブロック自体を左上から時計回りに
    boardMine[y][x] = CANTSET
    boardMine[y-1][x] = CANTSET
    boardMine[y-2][x] = CANTSET
    boardMine[y+1][x] = CANTSET
    boardMine[y+1][x-1] = CANTSET

    # ブロックと辺で接する地点を左上から時計回りに
    boardMine[y-3][x] = CANTSET
    boardMine[y-2][x+1] = CANTSET
    boardMine[y-1][x+1] = CANTSET
    boardMine[y][x+1] = CANTSET
    boardMine[y+1][x+1] = CANTSET
    boardMine[y+2][x] = CANTSET
    boardMine[y+2][x-1] = CANTSET
    boardMine[y+1][x-2] = CANTSET
    boardMine[y][x-1] = CANTSET
    boardMine[y-1][x-1] = CANTSET
    boardMine[y-2][x-1] = CANTSET

    # ブロックと角で接する地点を左上から時計回りに
    if boardMine[y-3][x-1] != CANTSET:
        boardMine[y-3][x-1] = ABLESET

    if boardMine[y-3][x+1] != CANTSET:
        boardMine[y-3][x+1] = ABLESET

    if boardMine[y+2][x+1] != CANTSET:
        boardMine[y+2][x+1] = ABLESET

    if boardMine[y+2][x-2] != CANTSET:
        boardMine[y+2][x-2] = ABLESET

    if boardMine[y][x-2] != CANTSET:
        boardMine[y][x-2] = ABLESET

    # ブロック自体を左上から時計回りに
    boardOpponent[y][x] = CANTSET
    boardOpponent[y-1][x] = CANTSET
    boardOpponent[y-2][x] = CANTSET
    boardOpponent[y+1][x] = CANTSET
    boardOpponent[y+1][x-1] = CANTSET

def changeTileStatus2(colorImage, colorRect, x, y, boardMine, boardOpponent, surface, tileLength):
    pass

def setableCheck1(x, y, boardMine):
    if (boardMine[y][x] != CANTSET
    and boardMine[y-1][x] != CANTSET
    and boardMine[y-2][x] != CANTSET
    and boardMine[y+1][x] != CANTSET
    and boardMine[y+1][x-1] != CANTSET):
        if boardMine[y][x] != ABLESET\
        or boardMine[y-1][x] != ABLESET\
        or boardMine[y-2][x] != ABLESET\
        or boardMine[y+1][x] != ABLESET\
        or boardMine[y+1][x-1] != ABLESET:
            return True

def setableCheck2(x, y, boardMine):
    if (boardMine[y][x] != CANTSET
    and boardMine[y][x+1] != CANTSET
    and boardMine[y][x+2] != CANTSET
    and boardMine[y][x-1] != CANTSET
    and boardMine[y-1][x-1] != CANTSET):
        if boardMine[y][x] != ABLESET\
        or boardMine[y][x+1] != ABLESET\
        or boardMine[y][x+2] != ABLESET\
        or boardMine[y][x-1] != ABLESET\
        or boardMine[y-1][x-1] != ABLESET:
            return True

def main(color, colorImage, colorRect, boardMine, boardOpponent, selectedDirection, x, y, surface, tileLength):
    if color == GREEN:
        if selectedDirection == 1: # 初期向き
            if setableCheck1(x, y, boardMine):
                changeTileStatus1(colorImage, colorRect, x, y, boardMine, boardOpponent, surface, tileLength)
                return True

        elif selectedDirection == 2: # 初期向きから90°時計回りに
            if setableCheck2(x, y, boardMine):
                surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * y))
                surface.blit(colorImage, colorRect.move(tileLength * (x+1), tileLength * y))
                surface.blit(colorImage, colorRect.move(tileLength * (x+2), tileLength * y))
                surface.blit(colorImage, colorRect.move(tileLength * (x-1), tileLength * y))
                surface.blit(colorImage, colorRect.move(tileLength * (x-1), tileLength * (y-1)))
                changeTileStatus2(x, y, boardMine, boardOpponent)
                return True

    elif color == YELLOW:
        pass

if __name__ == '__main__':
    main()
