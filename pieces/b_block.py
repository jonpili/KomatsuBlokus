import numpy as np

BLANK   = 0
CANTSET = 1
ABLESET = 2

GREEN  = 1
YELLOW = 2

def settableCheck1(boardMine, x, y):
    # for i in range(len(blockShape)):
    #     for j in range(len(blockShape)):
    #         tileStatus = blockShape[i][j]
    #         if tileStatus == CANTSET:
    if boardMine[y][x] != CANTSET and boardMine[y+1][x] != CANTSET:
        if boardMine[y][x] == ABLESET or boardMine[y+1][x] == ABLESET:
            return True

def changeTileImage1(colorImage, colorRect, x, y, surface, tileLength):
    surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * y))
    surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * (y+1)))

def changeBoardStatus(blockShape, blockInfluences, boardMine, boardOpponent, x, y):
    # ブロックの影響を自分のボードに適用
    for coord in np.argwhere(blockInfluences == CANTSET):
        boardMine[y + coord[0] - 2][x + coord[1] - 2] = CANTSET
    for coord in np.argwhere(blockInfluences == ABLESET):
        if boardMine[y + coord[0] - 2][x + coord[1] - 2] != CANTSET:
            boardMine[y + coord[0] - 2][x + coord[1] - 2] = ABLESET

    # for i in range(len(blockInfluences)):
    #     for j in range(len(blockInfluences)):
    #         tileStatus = blockInfluences[i][j]
    #         if tileStatus == CANTSET:
    #             boardMine[y+i-2][x+j-2] = CANTSET
    #         elif tileStatus == ABLESET:
    #             if boardMine[y+i-2][x+j-2] != CANTSET:
    #                 boardMine[y+i-2][x+j-2] = ABLESET

    # ブロックの形を自分以外のボードに適用
    for i in range(len(blockShape)):
        for j in range(len(blockShape)):
            tileStatus = blockShape[i][j]
            if tileStatus == CANTSET:
                boardOpponent[y+i-1][x+j-1] = CANTSET

def settableCheck2(boardMine, x, y):
    if boardMine[y][x] != CANTSET and boardMine[y][x-1] != CANTSET:
        if boardMine[y][x] == ABLESET or boardMine[y][x-1] == ABLESET:
            return True

def changeTileImage2(colorImage, colorRect, x, y, surface, tileLength):
    surface.blit(colorImage, colorRect.move(tileLength * x, tileLength * y))
    surface.blit(colorImage, colorRect.move(tileLength * (x-1), tileLength * y))

def changeTileStatus2(boardMine, boardOpponent, x, y):
    # ブロック自体を左上から時計回りに
    boardMine[y][x] = CANTSET
    boardMine[y][x-1] = CANTSET

    # ブロックと辺で接する地点を左上から時計回りに
    boardMine[y-1][x-1] = CANTSET
    boardMine[y-1][x] = CANTSET
    boardMine[y][x+1] = CANTSET
    boardMine[y+1][x] = CANTSET
    boardMine[y+1][x-1] = CANTSET
    boardMine[y][x-2] = CANTSET

    # ブロックと角で接する地点を左上から時計回りに
    if boardMine[y-1][x-2] != CANTSET:
        boardMine[y-1][x-2] = ABLESET

    if boardMine[y-1][x+1] != CANTSET:
        boardMine[y-1][x+1] = ABLESET

    if boardMine[y+1][x+1] != CANTSET:
        boardMine[y+1][x+1] = ABLESET

    if boardMine[y+1][x-2] != CANTSET:
        boardMine[y+1][x-2] = ABLESET

    # ブロック自体を左上から時計回りに
    boardOpponent[y][x] = CANTSET
    boardOpponent[y][x-1] = CANTSET

def main(colorImage, colorRect, boardMine, boardOpponent, selectedDirection, x, y, surface, tileLength):
    blockShape = np.asarray([
    [0,0,0],
    [0,1,0],
    [0,1,0]
    ])

    blockInfluences = np.asarray([
    [0,0,0,0,0],
    [0,2,1,2,0],
    [0,1,1,1,0],
    [0,1,1,1,0],
    [0,2,1,2,0]
    ])

    print(np.argwhere(blockInfluences == ABLESET)[0][0])

    if selectedDirection == 1: # 初期向き
        if settableCheck1(boardMine, x, y):
            changeTileImage1(colorImage, colorRect, x, y, surface, tileLength)
            changeBoardStatus(blockShape, blockInfluences, boardMine, boardOpponent, x, y)
            return True

    elif selectedDirection == 2: # 初期向きから90°時計回りに
        if settableCheck2(boardMine, x, y):
            changeTileImage2(colorImage, colorRect, x, y, surface, tileLength)
            changeTileStatus2(boardMine, boardOpponent, x, y)
            return True

if __name__ == '__main__':
    main()
