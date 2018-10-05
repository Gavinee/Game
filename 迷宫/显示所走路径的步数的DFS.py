"""
     走迷宫
     蓝色的边界 :blue                    -1
     每个格子之间的线：purple
     障碍物:yellow                        0
     可以行走的格子:white                  1
     起始点       ：red                   2
     终止点       ：red                   3
     通过DFS所经过的路径:black             4

     若起始地与终止点有路径可以到达，则将用黑色的路径找出所要经过的点
     若起始点与终止点无路径，直接弹出界面，显示是绝路。

     DFS的缺点：每次递归都按照方向顺序选择路径，而当迷宫是死路时，只有将迷宫全部可走路径完全遍历一遍才会结束搜索。
               算法的难易程度由算法所确定的行走的方向顺序决定。
               
     此程序能实时显示所走的路径的步数位置。
     程序源码地址:https://github.com/Gavinee/Game/blob/master/%E8%BF%B7%E5%AE%AB/%E6%98%BE%E7%A4%BA%E6%89%80%E8%B5%B0%E8%B7%AF%E5%BE%84%E7%9A%84%E6%AD%A5%E6%95%B0%E7%9A%84DFS.py
"""
__author__ = 'Qiufeng'
# 深度优先搜索，走迷宫

# -*- coding: utf-8 -*-
import turtle
import random
import sys


def title(chr, size):  # 标题
    turtle.penup()
    turtle.goto(-380, 370)
    turtle.write(chr, font=("Times", size, "bold"))
    turtle.pendown()


def GameOver(chr1, size1):
    turtle.reset()
    turtle.pensize(7)
    turtle.penup()
    turtle.goto(0, 0)
    turtle.write(chr1, font =("Times", size1, "bold"))
    turtle.pendown()

def Coordinate(chr,size,x,y):
    turtle.penup()
    turtle.pensize(5)
    turtle.color('white')
    turtle.goto(x, y)
    turtle.write(chr, font =("Times", size, "bold"))
    turtle.pendown()

def drawRectangle(color, fillingColor, pensize, speed, begin, length):  # 画正方形
    turtle.color(color, fillingColor)
    turtle.begin_fill()
    turtle.pensize(pensize)
    turtle.speed(speed)
    turtle.penup()
    turtle.goto(begin[0], begin[1])
    turtle.pendown()
    for i in range(4):
        turtle.forward(length)
        turtle.right(90)
    turtle.end_fill()


def draw(x, y, distance, chr, size, logicList):  # 画迷宫
    title(chr, size)
    seq = [0, 1, 2, 3,4]
    color = 'purple'
    fillingColor = 'blue'
    pensize = 5
    speed = 50
    length = distance
    # 迷宫墙

    for i in range(-x, x, distance):  # 上边界
        begin = [i, y]
        drawRectangle(color, fillingColor, pensize, speed, begin, length)

    for i in range(-x, x, distance):  # 下边界
        begin = [i, -y + distance]
        drawRectangle(color, fillingColor, pensize, speed, begin, length)

    for i in range(-y + distance, y, distance):  # 左边界
        begin = [-x, i]
        drawRectangle(color, fillingColor, pensize, speed, begin, length)

    for i in range(-y + distance, y, distance):  # 右边界
        begin = [x - distance, i]
        drawRectangle(color, fillingColor, pensize, speed, begin, length)

    # 迷宫内侧
    for i in range(-x + distance, x - distance, distance):  # 纵
        for j in range(y - distance, -y + distance, -distance):  # 横
            begin = [i, j]
            logicX = int((i + x) / distance)
            logicY = int((y - j) / distance)

            selectColor = random.choice(seq)
            # print(selectColor)
            if selectColor == 0:
                fillingColor = 'yellow'
                logicList[logicX][logicY] = 0  # 障碍物是0
            elif selectColor == 1:
                fillingColor = 'white'
                logicList[logicX][logicY] = 1  # 可走的路径是1
            else:
                fillingColor = 'white'
                logicList[logicX][logicY] = 1

            if i == -x + distance and j == y - distance:
                fillingColor = 'red'
                logicList[1][1] = 2
            if i == x - 2 * distance and j == -y + 2 * distance:
                fillingColor = 'red'
                logicList[len(logicList) - 2][len(logicList[0]) - 2] = 3
            drawRectangle(color, fillingColor, pensize, speed, begin, length)


def DFS(logicList, xpath, ypath, dst, path, count):  # DFS算法
    if (logicList[xpath][ypath] == 3):
        print(logicList)
        """
        if count[0] == 0:
            for jj in range(len(logicList[0])):
                for tt in range(len(logicList)):
                    if (logicList[tt][jj]==4):
                        path.append([tt,jj])
        """
        logicList[xpath][ypath] = 4
        path.append([xpath, ypath])
        count[0] = 1
        return

    for i in range(4):
        nextx = xpath + dst[i][0]
        nexty = ypath + dst[i][1]
        if (nextx >= 1
                and nexty >= 1
                and nextx <= len(logicList) - 2
                and nexty <= len(logicList[0]) - 2
                and logicList[nextx][nexty] != 0
                and logicList[nextx][nexty] != 4):
            logicList[xpath][ypath] = 4
            if (xpath, ypath) not in path:
                path.append([xpath, ypath])
            else:
                return
            DFS(logicList, nextx, nexty, dst, path, count)
            if count[0] == 1:
                return
            logicList[xpath][ypath] = 1

    return


def route(path, deviceDistance, deviceX, deviceY):  # 需要走过的路径
    color = 'black'
    fillingColor = 'black'
    pensize = 5
    speed = 50
    chr1 = "没有到达的路径，是绝路!!!"
    size1 = 24
    if len(path) == 1:
        GameOver(chr1, size1)
        return
    steps = 0
    for i in path:
        i[0] = i[0] * deviceDistance - deviceX
        i[1] = deviceY - i[1] * deviceDistance
        drawRectangle(color, fillingColor, pensize, speed, i, deviceDistance)               #填充方格
        Coordinate(str(steps), 15, i[0]+int(deviceDistance/2), i[1]-int(deviceDistance/2))   #所走的步数
        steps = steps + 1



def main():
    print("请输入方格的长:")
    distance = input()
    print("请输入画图区域的长(必须是方格长度的n倍,n=2,3,4,....):")
    width = input()
    deviceX = int(width)  # 屏幕上X轴正半轴的边界
    deviceY = int(width)  # 屏幕上Y轴正半轴的边界
    deviceDistance = int(distance ) # 每个迷宫方格的间距
    chr = "深度优先搜索(DFS)"  # 在屏幕上显示文字
    size = 20  # 字体大小

    x = deviceX * 2 / deviceDistance  # x轴方向方格的个数
    y = deviceY * 2 / deviceDistance  # y轴方向方格的个数

    logicList = []  # 逻辑坐标
    """
    这里逻辑坐标，将左上角定为[1,1],为起点，
    将右下角定为[x-2,y-2],为终点
    """
    for j in range(int(x)):  # j为纵轴
        list1 = []
        for i in range(int(y)):  # i为横轴
            list1.append(-1)  # 边界为-1
        logicList.append(list1)
    draw(deviceX, deviceY, deviceDistance, chr, size, logicList)

    path = []

    xpath = 1
    ypath = 1

    left = [-1, 0]
    right = [1, 0]
    under = [0, -1]
    on = [0, 1]
    dst = []  # 当前节点运动的方向  右上左下
    dst.append(right)
    dst.append(on)
    dst.append(left)
    dst.append(under)

    path.append([1, 1])  # 将起始点加入路径中,若数组中无元素，传到函数中只能是传值，而数组中有元素，
    # 传到函数中则是引用传递，而这里需要用到的就是引用传递
    count = [0]
    DFS(logicList, xpath, ypath, dst, path, count)

    route(path, deviceDistance, deviceX, deviceY)

main()
