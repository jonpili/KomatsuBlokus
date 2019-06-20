import numpy as np

array = [
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,1,1,0,0],
        [0,0,0,0,0]
        ]

array = np.asarray(array)

def test_0():
    print('わーい')

def test_1():
    print('いえーい')

def test_2():
    print('やっほー！')

name = 'test_'

for i in range(3):
    eval(name + str(i))()
