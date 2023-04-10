"""
打字游戏
1. 声明列表word、xx(x坐标值)、yy（y坐标值）
2. 创建init()函数，初始化三个列表
3. 第四部分：paint ===>绘制字符
4. 第三部分：action ===>进行字母移动
5. 键盘监听事件  循环比对
拓展练习：
1. 分数 score +5
2. 根据分数处理 速度问题
3. 加速度
"""

import sys
import pygame
import random
import graphic

import hit

MAX_WORD_NUM = 5

tick = 20

MAPX = 800
MAPY = 600


# word properties
word = []
color = []
xx = []
yy = []
speed = []
state = []


acc = 0.01 # 1 unit per tick square

score = 0
combo = 0

def init():
    global MAPX, MAPY, MAX_WORD_NUM
    graphic.init(MAPX, MAPY, MAX_WORD_NUM)

    for i in range(0,MAX_WORD_NUM):

        word.append(97 + i)
        color.append(graphic.get_not_green())
        xx.append(random.randint(200,700))
        yy.append(random.randint(-50,0))
        speed.append((random.choice([random.uniform(1,1.3), random.uniform(2,2.3)]), 0))
        state.append(True)
    

def new_word(idx, col):
# TODO
    color[idx] = col
    word[idx] = random.randint(97,122)
    xx[idx] = random.randint(200,700)
    yy[idx] = random.randint(-50, 0)
    speed[idx] = (random.uniform(1,2), 0)
    state[idx] = True


def out_of_limit(x, y):
    return (x < -50 or x > MAPX + 50) or (y < -50 or y > MAPY)


def hit_word(index):
    global color, speed, state, score, combo
# TODO
#    color[index] = graphic.get_green()
    speed[index] = hit.hit(graphic.sprite, (xx[index], yy[index]), speed[index])
    state[index] = False

#    combo += 1
#    score += min(combo, 20)

def miss():
    global combo
    combo = 0
    graphic.set_capoo(["capoo_miss", 0, graphic.pos_capoo])


def action():
    global score, combo, acc, capoo, pos_capoo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            target_index = -1
            key = event.key
            for index in range(0,MAX_WORD_NUM):
                '''
                TODO: 键盘按下后, 判断按键是否与屏幕上未命中的字母相同, 即正在往下走的字母. 若出现多个相同的字母, 则返回屏幕中最靠下的字母的下标,
                        将所需要返回的字母的下标储存在 max_idx 中.
                参数: key: 当前按下的字母; 
                     word: 屏幕上展示的字母列表(可重复), 比如, 若屏幕上此时有A, A, B, C, 
                            则word是一个包含了两个'A', 一个'B', 一个'C'的列表(顺序未知)
                     state: 当前字母的状态, state[i] == True时, 表示此字母 word[i] 正在下落, 未被命中; 
                            state[i] == False时, 表示字母 word[i] 已命中, 正在上升
                     yy: 表示字母的纵坐标, 如 yy[i] 表示字母 word[i] 的纵坐标. 且yy[i]数值越大, 字母在屏幕上的位置越靠下
                     xx: 表示字母的横坐标, 如 xx[i] 表示字母 word[i] 的横坐标. 且xx[i]数值越大, 字母在屏幕上的位置越靠右
                注意: i的取值在range(0, MAX_WORD_NUM), 即屏幕上同一时间最多只有MAX_WORD_NUM个字母
                '''
                if key == word[index] and state[index]:
                    target_index = index
                       
            if target_index >= 0:
                hit_word(target_index)
            else:
                miss()

    for i in range(0,MAX_WORD_NUM):
        yy[i] += speed[i][0]
        xx[i] += speed[i][1]
# TODO
#        speed[i] = (speed[i][0] + acc, speed[i][1])
        if out_of_limit(xx[i], yy[i]):
            if state[i]:
                miss()
            new_word(i, graphic.get_not_green())


def menu():
    pygame.display.set_caption("Capoo Typing")
    while True:
        action()
        graphic.paint(word, color, xx, yy, score, combo)
        pygame.time.delay(tick)
        pygame.display.update()

if __name__ == '__main__':
    init()
    menu()