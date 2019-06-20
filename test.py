import numpy as np

array = [
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,1,1,0,0],
        [0,0,0,0,0]
        ]

array = np.asarray(array)
#print(array)

import math

center = math.floor(len(array)/2)
array = np.where(array > 0, '□', '　')
for indexLine, line in enumerate(array):
    print('｜', end='')
    for indexCol, col in enumerate(line):
        if indexLine == center and indexCol == center:
            print('■', end='')
        else:
            print(col, end='')
    print('｜')
print('　', end='')
       #np.where(blockShape > 0 , '□', '　'):
    #print('｜', end='')
    #line(np.where(blockShape[1,1] == 1, '■', '  '))
