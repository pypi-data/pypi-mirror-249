
def matrixFindColMax(a: list) -> list:
    if len(a) <= 0:
        return [0] * 10
    
    maxCol = a[0].copy()
    for row in a:
        for i in range(0, len(row)):
            maxCol[i] = max(maxCol[i], row[i])
    return maxCol

def matrixTranspos(matrix: list) -> list:
    return [list(row) for row in zip(*matrix)]

def listStrToInt(data: list) -> list:
    for i in range(0,len(data)):
        if type(data[i]) != list:
            data[i] = int(data[i])
        else:
            data[i] = listStrToInt(data[i])
    return data
