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

def print_color(color):
    if color == Color.RED:
        print('Color is red')
    elif color == Color.GREEN:
        print('Color is green')
    elif color == Color.BLUE:
        print('Color is blue')
    else:
        print('not Color enum')

if __name__ == '__main__':
    print_color(Color.BLUE)  # Color is blue
    print_color('green')  # not Color enum
    print(Color)  # <enum 'Color'>
    print(Color('green'))  # Color.RED
    print(Color.RED == Color.RED)  # True
    print(Color.RED == Color.GREEN)  # False
    for color in Color:
        print(color)  # Color.RED\nColor.GREEN\nColor.BLUE
