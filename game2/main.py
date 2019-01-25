import pyglet
import random

class Snake(pyglet.window.Window):
    """
    贪吃蛇设计思路
    1. 贪吃蛇是一个队列，蛇头是队列第一个元素
    2. 贪吃蛇蛇头初始位置在屏幕中间，初始行动方向是向右，移速是蛇头的长度
    3. 贪吃蛇移动时，减去一个蛇尾单位，加上一个蛇头单位
    4. 贪吃蛇吃食物事，加上一个蛇头单位
    5. 贪吃蛇碰到边界时     失败
    6. 贪吃蛇碰到自己身体时 失败
    """

    WIDTH = 600
    HEIGHT = 600
    CAPTION = "Snake"

    # 一个单位的尺寸
    SIZE = 20

    # 初始位置(x,y)
    OFFSET = SIZE//2 #修正值
    position = [WIDTH//2 + OFFSET,HEIGHT//2 + OFFSET]

    #蛇头方向
    LEFT = 0
    UP = 1
    RIGHT = 2
    DWON = 3
    # 蛇头初始方向，向右
    DIRECT = RIGHT
    # 步长
    STEP = SIZE

    # 蛇长
    LENGTH = 1
    # 蛇每个单位的左下角坐标
    SNAKES = [position]

    # 随机食物坐标
    food = None

    # 游戏是否停止
    STOP = False
    # 游戏速率 [0,1]
    UPDATE_RATE = 0.2


    def __init__(self):
        self.win = pyglet.window.Window.__init__(self,width=self.WIDTH,height=self.HEIGHT,caption=self.CAPTION)
        pyglet.clock.schedule_interval(self.update, self.UPDATE_RATE)
        self.scene()
        pass

    def draw_points(self,x,y,isSnake=False,color = (1.0, 1.0, 1.0)):
        """
        画单位
        蛇是绿色
        食物是红色
        :param x:
        :param y:
        :return:
        """
        def draw():
            if isSnake:
                pyglet.gl.glColor3f(0.0, 1.0, 0.0)
            else:
                pyglet.gl.glColor3f(color[0], color[1], color[2])
            pyglet.gl.glPointSize(self.SIZE)
            pyglet.gl.glBegin(pyglet.gl.GL_POINTS)
            pyglet.gl.glVertex2f(x, y)
            pyglet.gl.glEnd()
        return draw

    def move(self):
        """
        蛇移动
        成功 = True
        :return:
        """
        # 计算下一次前进坐标，等于 蛇头坐标 + 方向偏移值
        target = None
        if self.DIRECT == self.LEFT:
            # 左
            target = [self.SNAKES[0][0] - self.STEP,self.SNAKES[0][1]]
        elif self.DIRECT == self.UP:
            # 上
            target = [self.SNAKES[0][0], self.SNAKES[0][1]  + self.STEP]
        elif self.DIRECT == self.RIGHT:
            # 右
            target = [self.SNAKES[0][0] + self.STEP, self.SNAKES[0][1]]
        else:
            # 下
            target = [self.SNAKES[0][0], self.SNAKES[0][1] - self.STEP]
        r = self.collision_detect(target[0],target[1])
        if r:
            return not r
        else:
            b = self.is_eat(target[0],target[1])
            if not b:
                del self.SNAKES[self.LENGTH - 1]
                del self.snakePoints[self.LENGTH - 1]
            else:
                del self.food
                del self.draw_food
                self.LENGTH += 1
                self.random_food()
            self.SNAKES.insert(0,target)
            self.snakePoints.insert(0,self.draw_points(target[0],target[1], True))
            return not r

    def collision_detect(self,x,y):
        """
        蛇碰撞检测
        x,y 是蛇头下一次前进的坐标
        1. 判断是否超出边界
        2. 判断是否碰撞蛇身 (只有蛇身长度大于 4 才需要检测)
        碰撞 = True
        :return:
        """
        if x <= 0 or y <= 0 or x >= self.WIDTH or y >= self.HEIGHT:
            return True
        if self.LENGTH > 4 :
            if [x,y] in self.SNAKES:
                return True
        return False

    def draw_snake(self):
        self.snakePoints = []
        for i,s in enumerate(self.SNAKES):
            self.snakePoints.append(self.draw_points(s[0],s[1],i == 0))

    def random_food(self):
        """
        随机食物
        1. 不出现在蛇身上
        2. 食物是红色的
        :return:
        """
        z = self.WIDTH // self.SIZE - 1
        while True:
            f = [random.randint(0,z)*self.SIZE + self.OFFSET,random.randint(0,z)*self.SIZE + self.OFFSET]
            if f not in self.SNAKES:
                self.food = f
                self.draw_food = self.draw_points(f[0],f[1],color=(1.0,0,0))
                return

    def is_eat(self,x,y):
        """
        吃食物
        蛇头下一次前进的坐标是否等于食物坐标
        :return:
        """
        if self.food is None:
            return False
        if x == self.food[0] and y == self.food[1]:
            # 可以吃
            return True
        return False

    def scene(self):
        """
        场景设置
        :return:
        """
        self.draw_snake()
        self.random_food()
        self.fps_display = pyglet.clock.ClockDisplay()
        pass

    def update(self,dt):
        # 0.1秒调用一次
        if not self.STOP:
            self.STOP = self.move() == False

    def on_draw(self):
        self.clear()
        for p in self.snakePoints:
            p()
        self.draw_food()

    def on_key_press(self, symbol, modifiers):
        # 改变蛇头的方向
        # 蛇头的方向不能指向蛇尾
        if (symbol == pyglet.window.key.A or symbol == pyglet.window.key.LEFT)  and self.DIRECT != self.RIGHT:
            self.DIRECT = self.LEFT
        elif (symbol == pyglet.window.key.W or symbol == pyglet.window.key.UP)  and self.DIRECT != self.DWON:
            self.DIRECT = self.UP
        elif (symbol == pyglet.window.key.D or symbol == pyglet.window.key.RIGHT) and self.DIRECT != self.LEFT:
            self.DIRECT = self.RIGHT
        elif (symbol == pyglet.window.key.S or symbol == pyglet.window.key.DOWN)  and self.DIRECT != self.UP:
            self.DIRECT = self.DWON
        else:
            # 其他按键是切换暂停和开始
            self.STOP = not self.STOP

if __name__ == '__main__':
    s = Snake()
    pyglet.app.run()
