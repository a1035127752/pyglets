import pyglet
import elements
from pyglet.window import mouse

class T3(pyglet.window.Window):

    WIDTH = 452
    HEIGHT = 452
    CAPTION = "T3"
    P = ["","叉","圈"]

    # 棋子区域边长
    PIECE_SIZE = 150
    # 间隙偏移值
    GAP_OFFSET = 151
    # 边界
    OUTSIDE = 452
    # 最大步数
    MAX_STEP = 9
    # 当前步数
    STEP = 1
    # 存放结果
    RESULT = [[0]*3 for i in range(3)]

    def __init__(self):
        self.win = pyglet.window.Window.__init__(self,width=self.WIDTH,height=self.HEIGHT,caption=self.CAPTION)
        self.scene()

        pass

    def scene(self):
        """
        场景设置
        :return:
        """
        self.imgs = elements.Image()
        cells = []
        for i in range(3):
            for j in range(3):
                cells.append(pyglet.sprite.Sprite(img=self.imgs.bg, x=j * self.PIECE_SIZE + j, y=i * self.PIECE_SIZE + i))
        self.cells = cells
        self.txt = label = pyglet.text.Label('', font_size=36,
                          x=self.WIDTH//2, y=self.HEIGHT//2,
                          color=(255, 0, 0, 255),
                          anchor_x='center', anchor_y='center')

    def area_no(self,x,y):
        """
        通过坐标计算鼠标所属区域
        6 7 8
        3 4 5
        0 1 2
        :param x:
        :param y:
        :return:
        """
        # 如果鼠标点击的是间隙或者不在棋盘区域返回 -1
        if x < 0 or x > self.OUTSIDE or y < 0 \
                or y > self.OUTSIDE or x == self.GAP_OFFSET \
                or x == 2 * self.GAP_OFFSET \
                or y == self.GAP_OFFSET or y == self.GAP_OFFSET:
            return -1
        px = x // self.PIECE_SIZE
        py = y // self.PIECE_SIZE
        return elements.areas[px][py],px,py

    def referee(self,step):
        """
        判定胜负
        步数 <= 4 不用判定
        :return:
        """
        if step <= 4:
            return 0
        # 返回值 1 = x     2 = o
        # 计算每列相加
        for x in range(3):
            r =  self.RESULT[x][0] & self.RESULT[x][1] & self.RESULT[x][2]
            if r > 0:
                return r
        #计算每行
        for y in range(3):
            r = self.RESULT[0][y] & self.RESULT[1][y] & self.RESULT[2][y]
            if r > 0:
                return r
        # 计算对角线
        diag1 = self.RESULT[0][0] & self.RESULT[1][1] & self.RESULT[2][2]
        if diag1 > 0:
            return diag1
        # 第二条对角线
        diag2 = self.RESULT[0][2] & self.RESULT[1][1] & self.RESULT[2][0]
        if diag2 > 0:
            return diag2
        return 0


    def on_draw(self):
        self.clear()
        for cell in self.cells:
            cell.draw()
        self.txt.draw()

    def on_mouse_press(self,x, y, button, modifiers):
        if button == mouse.LEFT:
            if self.STEP > self.MAX_STEP:
                return
            no,px,py = self.area_no(x,y)
            self.cells[no].x = px * self.PIECE_SIZE + px
            self.cells[no].y = py * self.PIECE_SIZE + py
            if self.STEP % 2 == 0:
                self.cells[no].image = self.imgs.o
                self.RESULT[px][py] = 2
            else:
                self.cells[no].image = self.imgs.x
                self.RESULT[px][py] = 1
            r = self.referee(self.STEP)
            if r > 0:
                self.STEP = self.MAX_STEP
                self.txt.text = "当前获胜是:{}".format(self.P[r])
            self.STEP += 1


if __name__ == '__main__':
    t3 = T3()
    pyglet.app.run()