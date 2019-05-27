BLANK   = 0
CANTSET = 1
ABLESET = 2

GREEN  = 1
YELLOW = 2

def changeTileStatus1(colorImage, colorRect, x, y, board1, board2, surface, tileLength):
    surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * y))
    surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * (y+1)))

    # ブロック自体を左上から時計回りに
    board1[y][x] = CANTSET
    board1[y+1][x] = CANTSET

    # ブロックと辺で接する地点を左上から時計回りに
    board1[y-1][x] = CANTSET
    board1[y][x+1] = CANTSET
    board1[y+1][x+1] = CANTSET
    board1[y+2][x] = CANTSET
    board1[y+1][x-1] = CANTSET
    board1[y][x-1] = CANTSET

    # ブロックと角で接する地点を左上から時計回りに
    if board1[y-1][x-1] != CANTSET:
        board1[y-1][x-1] = ABLESET

    if board1[y-1][x+1] != CANTSET:
        board1[y-1][x+1] = ABLESET

    if board1[y+2][x+1] != CANTSET:
        board1[y+2][x+1] = ABLESET

    if board1[y+2][x-1] != CANTSET:
        board1[y+2][x-1] = ABLESET

    # ブロック自体を左上から時計回りに
    board2[y][x] = CANTSET
    board2[y+1][x] = CANTSET

def changeTileStatus2(colorImage, colorRect, x, y, board1, board2, surface, tileLength):
    surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * y))
    surface.blit(colorImage, colorRect.move(tileLength * (x-1), tileLength * y))

    # ブロック自体を左上から時計回りに
    board1[y][x] = CANTSET
    board1[y][x-1] = CANTSET

    # ブロックと辺で接する地点を左上から時計回りに
    board1[y-1][x-1] = CANTSET
    board1[y-1][x] = CANTSET
    board1[y][x+1] = CANTSET
    board1[y+1][x] = CANTSET
    board1[y+1][x-1] = CANTSET
    board1[y][x-2] = CANTSET

    # ブロックと角で接する地点を左上から時計回りに
    if board1[y-1][x-2] != CANTSET:
        board1[y-1][x-2] = ABLESET

    if board1[y-1][x+1] != CANTSET:
        board1[y-1][x+1] = ABLESET

    if board1[y+1][x+1] != CANTSET:
        board1[y+1][x+1] = ABLESET

    if board1[y+1][x-2] != CANTSET:
        board1[y+1][x-2] = ABLESET

    # ブロック自体を左上から時計回りに
    board2[y][x] = CANTSET
    board2[y][x-1] = CANTSET

def main(color, colorImage, colorRect, selectedDirection, x, y, boardGreen, boardYellow, surface, tileLength):
    if color == GREEN:
        if selectedDirection == 1: # 初期向き（下）
            if ((boardGreen[y][x] != CANTSET and boardGreen[y+1][x] != CANTSET)
            and (boardGreen[y][x] == ABLESET or boardGreen[y+1][x] == ABLESET)):
                changeTileStatus1(colorImage, colorRect, x, y, boardGreen, boardYellow, surface, tileLength)
                return True

        elif selectedDirection == 2: # 初期向きから90°時計回りに（左）
            if ((boardGreen[y][x] != CANTSET and boardGreen[y][x-1] != CANTSET)
            and (boardGreen[y][x] == ABLESET or boardGreen[y][x-1] == ABLESET)):

                changeTileStatus2(colorImage, colorRect, x, y, boardGreen, boardYellow, surface, tileLength)
                return True

    elif color == YELLOW:
        if selectedDirection == 1: # 初期向き（下）
            if ((boardYellow[y][x] != CANTSET and boardYellow[y+1][x] != CANTSET)
            and (boardYellow[y][x] == ABLESET or boardYellow[y+1][x] == ABLESET)):
                changeTileStatus1(colorImage, colorRect, x, y, boardYellow, boardGreen, surface, tileLength)
                return True

        elif selectedDirection == 2: # 初期向きから90°時計回りに（左）
            if ((boardYellow[y][x] != CANTSET and boardYellow[y][x-1] != CANTSET)
            and (boardYellow[y][x] == ABLESET or boardYellow[y][x-1] == ABLESET)):
                changeTileStatus2(colorImage, colorRect, x, y, boardYellow, boardGreen, surface, tileLength)
                return True

if __name__ == '__main__':
    main()
