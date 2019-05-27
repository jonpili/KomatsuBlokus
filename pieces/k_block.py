BLANK   = 0
CANTSET = 1
ABLESET = 2

GREEN  = 1
YELLOW = 2

def changeTileStatus1(x, y, board1, board2):
    # ブロック自体を左上から時計回りに
    board1[y][x] = CANTSET
    board1[y-1][x] = CANTSET
    board1[y-2][x] = CANTSET
    board1[y+1][x] = CANTSET
    board1[y+1][x-1] = CANTSET

    # ブロックと辺で接する地点を左上から時計回りに
    board1[y-3][x] = CANTSET
    board1[y-2][x+1] = CANTSET
    board1[y-1][x+1] = CANTSET
    board1[y][x+1] = CANTSET
    board1[y+1][x+1] = CANTSET
    board1[y+2][x] = CANTSET
    board1[y+2][x-1] = CANTSET
    board1[y+1][x-2] = CANTSET
    board1[y][x-1] = CANTSET
    board1[y-1][x-1] = CANTSET
    board1[y-2][x-1] = CANTSET

    # ブロックと角で接する地点を左上から時計回りに
    if board1[y-3][x-1] != CANTSET:
        board1[y-3][x-1] = ABLESET

    if board1[y-3][x+1] != CANTSET:
        board1[y-3][x+1] = ABLESET

    if board1[y+2][x+1] != CANTSET:
        board1[y+2][x+1] = ABLESET

    if board1[y+2][x-2] != CANTSET:
        board1[y+2][x-2] = ABLESET

    if board1[y][x-2] != CANTSET:
        board1[y][x-2] = ABLESET

    # ブロック自体を左上から時計回りに
    board2[y][x] = CANTSET
    board2[y-1][x] = CANTSET
    board2[y-2][x] = CANTSET
    board2[y+1][x] = CANTSET
    board2[y+1][x-1] = CANTSET

def changeTileStatus2(x, y, board1, board2):
    pass

def setableCheck1

def main(color, colorImage, colorRect, selectedDirection, x, y, boardGreen, boardYellow, surface, tileLength):
    if color == GREEN:
        if selectedDirection == 1: # 初期向き
            if (boardGreen[y][x] != CANTSET
            and boardGreen[y-1][x] != CANTSET
            and boardGreen[y-2][x] != CANTSET
            and boardGreen[y+1][x] != CANTSET
            and boardGreen[y+1][x-1] != CANTSET):
                if boardGreen[y][x] != ABLESET\
                or boardGreen[y-1][x] != ABLESET\
                or boardGreen[y-2][x] != ABLESET\
                or boardGreen[y+1][x] != ABLESET\
                or boardGreen[y+1][x-1] != ABLESET:
                    surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * y))
                    surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * (y-1)))
                    surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * (y-2)))
                    surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * (y+1)))
                    surface.blit(colorImage, colorRect.move(tileLength * (x-1), tileLength * (y+1)))
                    changeTileStatus1(x, y, boardGreen, boardYellow)
                    return True

        elif selectedDirection == 2: # 初期向きから45°時計回りに
            if (boardGreen[y][x] != CANTSET
            and boardGreen[y][x+1] != CANTSET
            and boardGreen[y][x+2] != CANTSET
            and boardGreen[y][x-1] != CANTSET
            and boardGreen[y-1][x-1] != CANTSET):
                if boardGreen[y][x] != ABLESET\
                or boardGreen[y][x+1] != ABLESET\
                or boardGreen[y][x+2] != ABLESET\
                or boardGreen[y][x-1] != ABLESET\
                or boardGreen[y-1][x-1] != ABLESET:
                    surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * y))
                    surface.blit(colorImage, colorRect.move(tileLength * (x+1), tileLength * y))
                    surface.blit(colorImage, colorRect.move(tileLength * (x+2), tileLength * y))
                    surface.blit(colorImage, colorRect.move(tileLength * (x-1), tileLength * y))
                    surface.blit(colorImage, colorRect.move(tileLength * (x-1), tileLength * (y-1)))
                    changeTileStatus2(x, y, boardGreen, boardYellow)
                    return True

    elif color == YELLOW:
        pass

if __name__ == '__main__':
    main()
