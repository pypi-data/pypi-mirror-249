

#求256*256矩形方格的希尔伯特路径坐标点
#通用代码

def _hilbert(direction, rotation, order):
    if order == 0:
        return

    direction += rotation
    _hilbert(direction, -rotation, order - 1)
    step1(direction)

    direction -= rotation
    _hilbert(direction, rotation, order - 1)
    step1(direction)
    _hilbert(direction, rotation, order - 1)

    direction -= rotation
    step1(direction)
    _hilbert(direction, -rotation, order - 1)

def step1(direction):
    next = {0: (1, 0), 1: (0, 1), 2: (-1, 0), 3: (0, -1)}[direction & 0x3]

    global x, y
    x.append(x[-1] + next[0])
    y.append(y[-1] + next[1])

def hilbert_(order):
    global x, y
    x = [0,]
    y = [0,]
    _hilbert(0, 1, order)
    return (x, y)

def hilbert(o: int) -> list:
    """
    generate o order hilbert curve, side length is 2 ^ o

    生成o阶希尔伯特曲线，边长为2的o次方

    Usage
    ----------
    o = 0, 1, 2 ....

    Explanation
    ----------
    before: 
        0 1 2 3 4 5 6 7 8 9 a b c d e f
    after: 
        0 1 e f

        3 2 d c

        4 7 8 b

        5 6 9 a
    """
    x, y = hilbert_(o)
    res = list()
    for i in range(0, len(x)):
        res.append((x[i], y[i]))
    return res