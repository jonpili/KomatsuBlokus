import numpy as np
import math

BLANK   = 0
CANTSET = 1
ABLESET = 2

GREEN  = 1
YELLOW = 2

def setBlockInfo():
    blockShape = np.asarray([
    [0,1,0],
    [1,1,0],
    [1,1,0]
    ])

    blockInfluences = np.asarray([
    [0,2,1,2,0],
    [2,1,1,1,0],
    [1,1,1,1,0],
    [1,1,1,1,0],
    [2,1,1,2,0]
    ])

    return blockShape, blockInfluences

def display(selectedDirection):
    blockShape, blockInfluences = setBlockInfo()

    if selectedDirection == 0: # 初期向き
        pass
    elif selectedDirection == 1: # 裏向き
        blockShape = np.rot90(blockShape.T, -1)
    elif selectedDirection == 2: # 初期向きから90°時計回りに
        blockShape = np.rot90(blockShape, -1)
    elif selectedDirection == 3: # 裏向きから90°反時計回りに
        blockShape = blockShape.T
    elif selectedDirection == 4: # 初期向きから180°時計回りに
        blockShape = np.rot90(blockShape, -2)
    elif selectedDirection == 5: # 裏向きから180°反時計回りに
        blockShape = np.rot90(blockShape.T, -3)
    elif selectedDirection == 6: # 初期向きから270°時計回りに
        blockShape = np.rot90(blockShape, -3)
    elif selectedDirection == 7: # 裏向きから270°反時計回りに
        blockShape = np.rot90(blockShape.T, -2)

    print('')
    print('【選択中のブロック】')

    # 上の枠
    print('　', end='')
    for i in range(len(blockShape)):
        print('＿', end='')
    print('　')

    # 1を黒四角に、0を空白に置換
    center = math.floor(len(blockShape)/2)

    for indexLine, line in enumerate(np.where(blockShape > 0, '□', '　')):
        print('｜', end='')
        for indexCol, col in enumerate(line):
            if indexLine == center and indexCol == center:
                print('■', end='')
            else:
                print(col, end='')
        print('｜')
    print('　', end='')

    # 下の枠
    for i in range(len(blockShape)):
        print('￣', end='')
    print('　')

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
    blockShape, blockInfluences = setBlockInfo()

    if selectedDirection == 0: # 初期向き
        if settableCheck(blockShape, boardMine, x, y):
            changeBoardImage(blockShape, colorImage, colorRect, x, y, surface, tileLength)
            changeBoardStatus(blockShape, blockInfluences, boardMine, boardOpponent, x, y)
            return True

    elif selectedDirection == 1: # 裏向き
        blockShape = np.rot90(blockShape.T, -1)
        blockInfluences = np.rot90(blockInfluences.T, -1)
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

    elif selectedDirection == 3: # 裏向きから90°反時計回りに
        blockShape = blockShape.T
        blockInfluences = blockInfluences.T
        if settableCheck(blockShape, boardMine, x, y):
            changeBoardImage(blockShape, colorImage, colorRect, x, y, surface, tileLength)
            changeBoardStatus(blockShape, blockInfluences, boardMine, boardOpponent, x, y)
            return True

    elif selectedDirection == 4: # 初期向きから180°時計回りに
        blockShape = np.rot90(blockShape, -2)
        blockInfluences = np.rot90(blockInfluences, -2)
        if settableCheck(blockShape, boardMine, x, y):
            changeBoardImage(blockShape, colorImage, colorRect, x, y, surface, tileLength)
            changeBoardStatus(blockShape, blockInfluences, boardMine, boardOpponent, x, y)
            return True

    elif selectedDirection == 5: # 裏向きから180°反時計回りに
        blockShape = np.rot90(blockShape.T, -3)
        blockInfluences = np.rot90(blockInfluences.T, -3)
        if settableCheck(blockShape, boardMine, x, y):
            changeBoardImage(blockShape, colorImage, colorRect, x, y, surface, tileLength)
            changeBoardStatus(blockShape, blockInfluences, boardMine, boardOpponent, x, y)
            return True

    elif selectedDirection == 6: # 初期向きから270°時計回りに
        blockShape = np.rot90(blockShape, -3)
        blockInfluences = np.rot90(blockInfluences, -3)
        if settableCheck(blockShape, boardMine, x, y):
            changeBoardImage(blockShape, colorImage, colorRect, x, y, surface, tileLength)
            changeBoardStatus(blockShape, blockInfluences, boardMine, boardOpponent, x, y)
            return True

    elif selectedDirection == 7: # 裏向きから270°反時計回りに
        blockShape = np.rot90(blockShape.T, -2)
        blockInfluences = np.rot90(blockInfluences.T, -2)
        if settableCheck(blockShape, boardMine, x, y):
            changeBoardImage(blockShape, colorImage, colorRect, x, y, surface, tileLength)
            changeBoardStatus(blockShape, blockInfluences, boardMine, boardOpponent, x, y)
            return True

if __name__ == '__main__':
    main()
