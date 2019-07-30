# import numpy as np
#
# array = [
#         [1,2,3,4,5],
#         [1,2,3,4,5],
#         [1,2,3,4,5],
#         [1,2,3,4,5],
#         [1,2,3,4,5]
#         ]
#
# array = np.asarray(array)

from enum import Enum

class Color(Enum):
    GREEN  = 'green'
    YELLOW = 'yellow'
    RED    = 'red' # 将来的に実装
    BLUE   = 'blue' # 将来的に実装

if __name__ == '__main__':
    print(Color)  # <enum 'Color'>
    print(Color('green').value)  # Color.RED
    print(Color.RED == Color.RED)  # True
    print(Color.RED == Color.GREEN)  # False
    for color in Color:
        print(color)  # Color.RED\nColor.GREEN\nColor.BLUE
