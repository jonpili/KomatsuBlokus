import numpy as np

blockShape = [
             [0,0,1,0,0],
             [0,0,1,0,0],
             [0,0,1,0,0],
             [0,1,1,0,0],
             [0,0,0,0,0]
             ]

blockShape = np.asarray(blockShape)
print(blockShape)

blockCenter = round(len(blockShape)/2)

# 上の枠
print('　', end='')
for i in range(len(blockShape)):
    print('＿', end='')
print('　')

# 1を黒四角に、0を空白に置換
for lineIndex, line in enumerate(np.where(blockShape > 0, '䨻', '　')):
    print('｜', end='')
    for colIndex, col in enumerate(line):
        if lineIndex == blockCenter and colIndex == blockCenter:
            print('口', end='')
        else:
            print(col, end='')
    print('｜')
print('　', end='')

# 下の枠
for i in range(len(blockShape)):
    print('￣', end='')
print('　')
