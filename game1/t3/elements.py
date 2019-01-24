import pyglet

# 初始化棋子区域坐标序号
areas = [[0]*3 for i in range(3)]
areas[0][0] = 0
areas[1][0] = 1
areas[2][0] = 2
areas[0][1] = 3
areas[1][1] = 4
areas[2][1] = 5
areas[0][2] = 6
areas[1][2] = 7
areas[2][2] = 8

class Image():
    """
    图片资源
    """
    def __init__(self):
        pyglet.resource.path = ['../resources']
        pyglet.resource.reindex()
        self.bg = pyglet.resource.image("bg1.png")
        self.o = pyglet.resource.image("o_bg1.png")
        self.x = pyglet.resource.image("x_bg1.png")
        pass


