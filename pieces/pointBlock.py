BLANK   = 0
CANTSET = 1
ABLESET = 2

GREEN  = 1
YELLOW = 2

def changeTileStatus(x, y, board1, board2):
    # ブロック自体を左上から時計回りに
    board1[y][x] = CANTSET

    # ブロックと辺で接する地点を左上から時計回りに
    board1[y][x-1] = CANTSET
    board1[y-1][x] = CANTSET
    board1[y][x+1] = CANTSET
    board1[y+1][x] = CANTSET

    # ブロックと角で接する地点を左上から時計回りに
    if board1[y-1][x-1] != CANTSET:
        board1[y-1][x-1] = ABLESET

    if board1[y-1][x+1] != CANTSET:
        board1[y-1][x+1] = ABLESET

    if board1[y+1][x+1] != CANTSET:
        board1[y+1][x+1] = ABLESET

    if board1[y+1][x-1] != CANTSET:
        board1[y+1][x-1] = ABLESET

    # ブロック自体を左上から時計回りに
    board2[y][x] = CANTSET

def main(color, colorImage, colorRect, x, y, boardGreen, boardYellow, surface, tileLength):
    if color == GREEN:
        if boardGreen[y][x] == ABLESET:
            surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * y))
            changeTileStatus(x, y, boardGreen, boardYellow)
            return True

    elif color == YELLOW:
        if boardYellow[y][x] == ABLESET:
            surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * y))
            changeTileStatus(x, y, boardYellow, boardGreen)
            return True

if __name__ == '__main__':
    main()
