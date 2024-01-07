from PIL import Image
import numpy as np 
import matplotlib.pyplot as plt

from ..helpers import listhelper


def draw2DPoint(pts: list) -> None:
    """
    draw 2D Point Plot

    绘制2维散点图

    Usage
    ----------
    pts = [
        [1, 1], [1, 2], [1, 3], [3, 2] ...
    ]
    """
    pts = listhelper.listStrToInt(pts)
    pts_trans = listhelper.matrixTranspos(pts)
    pts_max = listhelper.matrixFindColMax(pts)

    plt.figure(figsize=(pts_max[0] + 1, pts_max[1] + 1))
    plt.scatter(np.array(pts_trans[0]), np.array(pts_trans[1]), c='r')
    plt.show()

def draw3DPoint(pts: list) -> None:
    """
    draw 3D Point Plot

    绘制3维散点图

    Usage
    ----------
    pts = [
        [1, 1, 1], [1, 1, 2], [1, 2, 1], [1, 3, 1] ...
    ]
    """
    pts = listhelper.listStrToInt(pts)
    pts_trans = listhelper.matrixTranspos(pts)

    ax: plt.Axes = plt.subplot(projection = '3d')
    ax.set_title('3DPointPlot')
    ax.scatter(np.array(pts_trans[0]), np.array(pts_trans[1]), np.array(pts_trans[2]), c = 'r')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
        
def draw2DPixel(pts: list, reverse: bool = False) -> None:
    """
    draw 2D Pixel Plot

    绘制2维像素图

    automatically calculate length and width, display images in a format similar to a QR code
    
    自动计算图的长宽，生成一个类似于二维码的图片

    Usage
    ----------
    pts = [
        [1, 1], [1, 2], [1, 3], [3, 2] ...
    ]

    reverse = True || False
    """
    
    if reverse: 
        bgc, sfc = (255, 255, 255), (0, 0, 0)
    else: 
        bgc, sfc = (0, 0, 0), (255, 255, 255)

    pts = listhelper.listStrToInt(pts)
    pts_max = listhelper.matrixFindColMax(pts)

    pic: Image = Image.new("RGB", (pts_max[0] + 1, pts_max[1] + 1), bgc)
    for pt in pts:
        pic.putpixel([pt[0], pt[1]], sfc)
    pic.show()
