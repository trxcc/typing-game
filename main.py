"""
capoo的打字世界
1. 声明列表word、xx(x坐标值)、yy（y坐标值）
2. 创建init()函数，初始化三个列表
3. 第四部分：paint ===>绘制字符
4. 第三部分：action ===>进行字母移动
5. 键盘监听事件  循环比对
拓展练习：
1. 分数 score 
2. 根据分数处理 速度问题
3. 加速度
"""

import sys
import pygame
import random
import graphic
import hit

tick = 20 # tick是游戏内时间计量单位

MAPX = 800 # (MAPX, MAPY) 是游戏窗口的大小
MAPY = 600

MAX_WORD_NUM = 10 # MAX_WORD_NUM 是游戏界面中同一时刻出现字母的最大数量, 建议数值小于15
# word properties
word = []     # word列表存储当前屏幕上的所有字母
color = []    # color列表存储每个字母的RGB颜色, 即color[i]存储word[i]的颜色
xx = []       # xx列表存储每个字母在屏幕中的横坐标, 即xx[i]存储word[i]的横坐标, xx[i]越大, 在屏幕中越靠右
yy = []       # yy列表存储每个字母在屏幕中的纵坐标, 即yy[i]存储word[i]的纵坐标, yy[i]越大, 在屏幕中越靠下
speed = []    # speed列表存储每个字母的当前速度, 即color[i]存储word[i]的速度. speed中每个元素是一个元组(speed_x, speed_y), 代表横向和纵向的速度
state = []    # state列表存储每个字母的状态, state[i] == True时, 表示此字母 word[i] 正在下落, 未被命中; state[i] == False时, 表示字母 word[i] 已命中, 正在上升


acc = 0.005 # 1 unit per tick square
           # 你猜猜这是啥? 提示: 看看上面这行英文注释是什么单位

score = 0  # score 代表capoo当前得到的分数
combo = 0  # combo 代表capoo当前的连击次数. 若打错字母或字母落到屏幕最下方还没被击中, 则连击中断, combo置0

def init():
    '''
    init函数进行一系列数据, 图像的初始化
    '''
    global MAPX, MAPY, MAX_WORD_NUM         # 想一想刚刚的课, global有什么用呢?
    graphic.init(MAPX, MAPY, MAX_WORD_NUM)  # 这一行初始化画图相关的对象

    for i in range(0,MAX_WORD_NUM):
        # 初始化MAX_WORD_NUM个字母, 并填充对应列表.
        # 注意, 一个字母的大小是 50 * 50
        word.append(97 + i)
        color.append(graphic.get_initial_color())
        xx.append(random.randint(200,700))
        yy.append(random.randint(-50,0))
        speed.append((random.choice([random.uniform(1,1.3), random.uniform(2,2.3)]), 0))
        state.append(True)
    

def new_word(idx, col):
    color[idx] = col
    word[idx] = random.randint(97,122)
    xx[idx] = random.randint(200,700)
    yy[idx] = random.randint(-50, 0)
    speed[idx] = (random.uniform(1,2), 0)
    state[idx] = True


def out_of_limit(x, y):
    '''
    TODO: 判断字母是否出界.
    参数x: 待判断字母的横坐标; y: 待判断字母的纵坐标
    出界的标准: x + 字母的宽度 < 0 或 x > 屏幕宽度
              y + 字母的宽度 < 0 或 y > 屏幕深度
    '''
    # return False
    return (x < -50 or x > MAPX) or (y < -50 or y > MAPY)

# hit_word函数在word[index]字母被命中后进行一系列处理
def hit_word(index):
    global color, speed, state, score, combo
    '''
    TODO: 1. 修改命中字母后的字母颜色, 可使用graphic.py文件中的get_hit_color()函数
          2. 维护连击次数combo. 
                capoo很想知道自己到底连击了多少次. 那么命中后, combo应怎么办呢? 
    '''
    color[index] = graphic.get_hit_color()
    speed[index] = hit.hit(graphic.sprite, (xx[index], yy[index]), speed[index])
    state[index] = False

    combo += 1
    score += min(combo, 20)

# hit_word函数在输入错误字母后进行一系列处理, 请勿修改
def miss():
    global combo
    combo = 0
    graphic.set_capoo(["capoo_miss", 0, graphic.pos_capoo])

'''
action函数维护每一个字母的速度, 加速度, 以及当前坐标
'''
def action():
    global score, combo, acc, capoo, pos_capoo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            target_index = -1
            key = event.key
            max_depth = -1
            for index in range(0,MAX_WORD_NUM):
                '''
                TODO: 键盘按下后, 判断按键是否与屏幕上未命中的字母相同, 即正在往下走的字母. 若出现多个相同的字母, 则返回屏幕中最靠下的字母的下标,
                        将所需要返回的字母的下标储存在 max_idx 中.
                参数: key: 当前按下的字母; 
                     target_index: 将要修改状态的字母的索引值
                     index: 当前循环到的字母的索引值
                     word: 屏幕上展示的字母列表(可重复), 比如, 若屏幕上此时有A, A, B, C, 
                            则word是一个包含了两个'A', 一个'B', 一个'C'的列表(顺序未知)
                     state: 当前字母的状态, state[i] == True时, 表示此字母 word[i] 正在下落, 未被命中; 
                            state[i] == False时, 表示字母 word[i] 已命中, 正在上升
                     yy: 表示字母的纵坐标, 如 yy[i] 表示字母 word[i] 的纵坐标. 且yy[i]数值越大, 字母在屏幕上的位置越靠下
                     xx: 表示字母的横坐标, 如 xx[i] 表示字母 word[i] 的横坐标. 且xx[i]数值越大, 字母在屏幕上的位置越靠右
                注意: i的取值在range(0, MAX_WORD_NUM), 即屏幕上同一时间最多只有MAX_WORD_NUM个字母
                '''
                # target_index = random.choice(range(0, MAX_WORD_NUM)) # XXX: need to be modified
                if key == word[index] and max_depth < yy[index]:
                    max_depth = yy[index]
                    target_index = index

            # 以下的 if-else 结构进行命中或不命中的判断与处理, 调用前面定义的 hit_word 和 miss 函数
            if target_index >= 0:
                hit_word(target_index)
            else:
                miss()

    # 以下三行进行字母坐标的移动, 见文知义
    for i in range(0,MAX_WORD_NUM):
        yy[i] += speed[i][0]
        xx[i] += speed[i][1]

        '''
        TODO: (可选做, 不难) 引入加速度概念. v = v0 + at, 此处默认 t = 1 tick 
        '''
        speed[i] = (speed[i][0] + acc, speed[i][1])

        # 进行出界的判断和处理. 判断是否出现 miss 的情况, 并生成一个新的字母
        if out_of_limit(xx[i], yy[i]) == True:
            if state[i] == True:
                miss()
            new_word(i, graphic.get_initial_color())

# menu函数是程序主循环, 请勿修改!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def menu():
    pygame.display.set_caption("Capoo Typing")
    while True:
        action()
        graphic.paint(word, color, xx, yy, score, combo)
        pygame.time.delay(tick)
        pygame.display.update()

# 程序主函数
if __name__ == '__main__':
    init()
    menu()