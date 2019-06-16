# import numpy as np
#
# array = [
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#         [1, 0, 2, 1, 2, 0, 0, 0, 0, 1],
#         [1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
#         [1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
#         [1, 2, 1, 1, 1, 1, 0, 0, 0, 1],
#         [1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
#         [1, 2, 1, 1, 2, 1, 2, 0, 0, 1],
#         [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
#         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
#         ]
#
# array = np.asarray(array).T
# print(array[2][1])

import re

while True:
    selectedBlock = input('ブロックを選択してください：')
    while re.search('[^a-u]', selectedBlock) or re.search('[a-u]{2,}', selectedBlock) or selectedBlock == '':
        print('入力が間違っています')
        selectedBlock = input('ブロックを選択してください：')

    selectedDirection = input('向きを選択してください：')
    while re.search('[^0-7]', selectedDirection) or re.search('[0-7]{2,}', selectedDirection) or selectedDirection == '':
        print('入力が間違っています')
        selectedDirection = input('向きを選択してください：')
    selectedDirection = int(selectedDirection)

    print(selectedBlock)
    print(selectedDirection)
