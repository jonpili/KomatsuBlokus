import numpy as np

BLANK   = 0
CANTSET = 1
ABLESET = 2

GREEN  = 1
YELLOW = 2

def settableCheck(blockShape, boardMine, x, y):
    # 1つでもCANTSETがあれば置けない
    for coord in np.argwhere(blockShape == CANTSET):
        if boardMine[y + coord[0] - 1][x + coord[1] - 1] == CANTSET:
            return False
    # 1つでもABLESETがあれば置ける
    for coord in np.argwhere(blockShape == CANTSET):
        if boardMine[y + coord[0] - 1][x + coord[1] - 1] == ABLESET:
            return True

def changeBoardImage(blockShape, colorImage, colorRect, x, y, surface, tileLength):
    for coord in np.argwhere(blockShape == CANTSET):
        surface.blit(colorImage, colorRect.move(tileLength * (x + coord[1] - 1), tileLength * (y + coord[0] - 1)))

def changeBoardStatus(blockShape, blockInfluences, boardMine, boardOpponent, x, y):
    # ブロックの影響を自分のボードに適用
    for coord in np.argwhere(blockInfluences == CANTSET):
        boardMine[y + coord[0] - 2][x + coord[1] - 2] = CANTSET
    for coord in np.argwhere(blockInfluences == ABLESET):
        if boardMine[y + coord[0] - 2][x + coord[1] - 2] == BLANK:
            boardMine[y + coord[0] - 2][x + coord[1] - 2] = ABLESET

    # ブロックの影響を自分以外のボードに適用
    for coord in np.argwhere(blockShape == CANTSET):
        boardOpponent[y + coord[0] - 1][x + coord[1] - 1] = CANTSET

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

    if selectedDirection == 1: # 初期向き
        if settableCheck(blockShape, boardMine, x, y):
            changeBoardImage(blockShape, colorImage, colorRect, x, y, surface, tileLength)
            changeBoardStatus(blockShape, blockInfluences, boardMine, boardOpponent, x, y)
            return True

    elif selectedDirection == 2: # 初期向きから90°時計回りに
        blockShape = np.rot90(blockShape, -1)
        blockInfluences = np.rot90(blockInfluences, -1)
        if settableCheck(blockShape, boardMine, x, y):
            changeBoardImage(blockShape, colorImage, colorRect, x, y, surface, tileLength)
            changeBoardStatus(blockShape, blockInfluences, boardMine, boardOpponent, x, y)
            return True

if __name__ == '__main__':
    main()
