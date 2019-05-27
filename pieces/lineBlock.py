BLANK   = 0
CANTSET = 1
ABLESET = 2

GREEN  = 1
YELLOW = 2

def changeTileStatus1(x, y, board1, board2):
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

def changeTileStatus2(x, y, board1, board2):
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
        if selectedDirection == 1: # 下向き（図における初期向き）
            if ((boardGreen[y][x] != CANTSET and boardGreen[y+1][x] != CANTSET)
            and (boardGreen[y][x] == ABLESET or boardGreen[y+1][x] == ABLESET)):
                surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * y))
                surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * (y+1)))
                changeTileStatus1(x, y, boardGreen, boardYellow)
                return True

        elif selectedDirection == 2: # 左向き（図における初期向きから時計回りに）
            if ((boardGreen[y][x] != CANTSET and boardGreen[y][x-1] != CANTSET)
            and (boardGreen[y][x] == ABLESET or boardGreen[y][x-1] == ABLESET)):
                surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * y))
                surface.blit(colorImage, colorRect.move(tileLength * (x-1), tileLength * y))
                changeTileStatus2(x, y, boardGreen, boardYellow)
                return True

    elif color == YELLOW:
        if selectedDirection == 1: # 下向き（図における初期向き）
            if ((boardYellow[y][x] != CANTSET and boardYellow[y+1][x] != CANTSET)
            and (boardYellow[y][x] == ABLESET or boardYellow[y+1][x] == ABLESET)):
                surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * y))
                surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * (y+1)))
                changeTileStatus1(x, y, boardYellow, boardGreen)
                return True

        elif selectedDirection == 2: # 左向き（図における初期向きから時計回りに）
            if ((boardYellow[y][x] != CANTSET and boardYellow[y][x-1] != CANTSET)
            and (boardYellow[y][x] == ABLESET or boardYellow[y][x-1] == ABLESET)):
                surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * y))
                surface.blit(colorImage, colorRect.move(tileLength * (x-1), tileLength * y))
                changeTileStatus2(x, y, boardGreen, boardYellow)
                return True

if __name__ == '__main__':
    main()
