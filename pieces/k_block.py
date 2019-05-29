BLANK   = 0
CANTSET = 1
ABLESET = 2

GREEN  = 1
YELLOW = 2

def settableCheck1(boardMine, x, y):
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

def changeTileImage1(colorImage, colorRect, x, y, surface, tileLength):
    surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * y))
    surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * (y-1)))
    surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * (y-2)))
    surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * (y+1)))
    surface.blit(colorImage, colorRect.move(tileLength * (x-1), tileLength * (y+1)))

def changeTileStatus1(boardMine, boardOpponent, x, y):
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

def settableCheck2(boardMine, x, y):
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

def changeTileImage2(colorImage, colorRect, x, y, surface, tileLength):
    surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * y))
    surface.blit(colorImage, colorRect.move(tileLength * (x+1), tileLength * y))
    surface.blit(colorImage, colorRect.move(tileLength * (x+2), tileLength * y))
    surface.blit(colorImage, colorRect.move(tileLength * (x-1), tileLength * y))
    surface.blit(colorImage, colorRect.move(tileLength * (x-1), tileLength * (y-1)))

def changeTileStatus2(boardMine, boardOpponent, x, y):
    # ブロック自体を左上から時計回りに
    boardMine[y][x] = CANTSET
    boardMine[y][x+1] = CANTSET
    boardMine[y][x+2] = CANTSET
    boardMine[y][x-1] = CANTSET
    boardMine[y-1][x-1] = CANTSET

    # ブロックと辺で接する地点を左上から時計回りに
    boardMine[y-2][x-1] = CANTSET
    boardMine[y-1][x] = CANTSET
    boardMine[y-1][x+1] = CANTSET
    boardMine[y-1][x+2] = CANTSET
    boardMine[y][x+3] = CANTSET
    boardMine[y+1][x+2] = CANTSET
    boardMine[y+1][x+1] = CANTSET
    boardMine[y+1][x] = CANTSET
    boardMine[y+1][x-1] = CANTSET
    boardMine[y][x-1] = CANTSET
    boardMine[y-1][x-2] = CANTSET

    # ブロックと角で接する地点を左上から時計回りに
    if boardMine[y-2][x-2] != CANTSET:
        boardMine[y-2][x-2] = ABLESET

    if boardMine[y-2][x] != CANTSET:
        boardMine[y-2][x] = ABLESET

    if boardMine[y-1][x+3] != CANTSET:
        boardMine[y-1][x+3] = ABLESET

    if boardMine[y+1][x+3] != CANTSET:
        boardMine[y+1][x+3] = ABLESET

    if boardMine[y+1][x-2] != CANTSET:
        boardMine[y+1][x-2] = ABLESET

    # ブロック自体を左上から時計回りに
    boardOpponent[y][x] = CANTSET
    boardOpponent[y][x+1] = CANTSET
    boardOpponent[y][x+2] = CANTSET
    boardOpponent[y][x-1] = CANTSET
    boardOpponent[y-1][x-1] = CANTSET

def main(colorImage, colorRect, boardMine, boardOpponent, selectedDirection, x, y, surface, tileLength):
    if selectedDirection == 1: # 初期向き
        if settableCheck1(boardMine, x, y):
            changeTileImage1(colorImage, colorRect, x, y, surface, tileLength)
            changeTileStatus1(boardMine, boardOpponent, x, y)
            return True

    elif selectedDirection == 2: # 初期向きから90°時計回りに
        if settableCheck2(boardMine, x, y):
            changeTileImage2(colorImage, colorRect, x, y, surface, tileLength)
            changeTileStatus2(boardMine, boardOpponent, x, y)
            return True

    # elif selectedDirection == 3: # 初期向きから180°時計回りに
    #     if settableCheck3(boardMine, x, y):
    #         changeTileImage3(colorImage, colorRect, x, y, surface, tileLength)
    #         changeTileStatus3(boardMine, boardOpponent, x, y)
    #         return True

if __name__ == '__main__':
    main()
