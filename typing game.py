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
import gifList
import os, sys
import pygame

import random
 
tick = 16

def menu():

    pygame.display.set_caption("打字游戏")

    while True:
        screen.fill((255, 255, 255))

        action()

        paint()

        pygame.time.delay(tick)

        pygame.display.update()
 
screen = pygame.display.set_mode((800, 600), 0, 0)

word = []

color = []

xx = []
yy = []
speed = []
acc = 0 # 1 unit per tick square
state = []

score = 0
combo = 0

deep_color_lim = (192, 255)
light_color_lim = (0, 64)

sprite = []
capooList = []
capoo = []
pos_capoo = (0, 400)

gif = {}


def init():
    global capoo, capooList, pos_capoo

    for i in range(0,12):

        word.append(97 + i)

        color.append(get_color(rlim=deep_color_lim, glim=light_color_lim, blim=deep_color_lim))

        xx.append(random.randint(200,700))
        yy.append(random.randint(-200,100))
        speed.append((random.choice([random.uniform(1,1.3), random.uniform(2,2.3)]), 0))
        state.append(True)
    for gifFile in gifList.gif_list:
        gifName = gifFile[0]
        index = 1
        gif[gifName] = []
        while os.path.isfile(f"./pic/pic_{gifName}/{gifName}_{index}.png"):
            gif[gifName].append(pygame.transform.scale(pygame.image.load(f"./pic/pic_{gifName}/{gifName}_{index}.png"), gifFile[1]))
            index += 1
    capooList = [("capoo_miss",-1), ("capoo_lazy", 0), ("capoo_easy", 10), ("capoo_crazy", 20)]
    capoo = ["capoo_hello", 0, pos_capoo]


def miss():
    global combo, capoo
    combo = 0
    capoo = ["capoo_miss", 0, pos_capoo]

def action():
    global score, combo, acc, capoo, pos_capoo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            max_deep = -1
            max_idx = -1
            key = event.key
            for i in range(0,12):
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
                注意: i的取值在range(0, 12), 即屏幕上同一时间最多只有12个字母
                '''
                if key == word[i] and state[i] == True:
                    if max_deep < yy[i]:
                        max_deep = yy[i]
                        max_idx = i
                pass
            
            
                
            if max_idx >= 0:
                color[max_idx] = get_color(rlim=light_color_lim, glim=deep_color_lim, blim=light_color_lim)
                speed[max_idx] = (-3, 0)
                state[max_idx] = False
                combo += 1
                score += min(combo, 10)
            else:
                miss()


    for i in range(0,12):
        yy[i] += speed[i][0]
        speed[i] = (speed[i][0] + acc, speed[i][1])
        if yy[i] > 600:
            color[i] = get_color(rlim=deep_color_lim, glim=light_color_lim, blim=deep_color_lim)
            yy[i] = -50
            score -= 20
            speed[i] = (random.uniform(1,2),0)
            miss()
            state[i] = True
        elif yy[i] < -50:
            color[i] = get_color(rlim=deep_color_lim, glim=light_color_lim, blim=deep_color_lim)
            word[i] = random.randint(97,122)
            xx[i] = random.randint(200,700)
            speed[i] = (random.uniform(1,2), 0)
            state[i] = True
 
 
"""
第四部分:图形图案绘制区域
"""
def paint():
    global sprite, capoo, pos_capoo
    pygame.font.init()
    font = pygame.font.Font("arial.ttf", 40)
    for i in range(0,12):
        fontRead = font.render(chr(word[i]-32),True,color[i])
        scoreShow = font.render("score:%s"%score,True,(255,0,0))
        comboShow = font.render("combo x%s"%combo, True, (255,0,0))

        screen.blit(fontRead,(xx[i],yy[i]))

        screen.blit(scoreShow, (20,20))

        TPP = 18

        print(capoo[0])
        screen.blit(gif[capoo[0]][capoo[1] // TPP], capoo[2])
        capoo[1] += 1
        if (capoo[1] // TPP >= len(gif[capoo[0]])):
            capoo[1] = 0
            for cp in capooList:
                if combo >= cp[1]:
                    capoo = [cp[0], 0, pos_capoo]

        for sp in sprite:
            screen.blit(gif[sp[0]][sp[1] // TPP], sp[2])
            sp[1] += 1
        
        sprite = [sp for sp in sprite if (sp[1] // TPP) < len(gif[sp[0]])]

        if combo > 0:
            screen.blit(comboShow, (20,60))

 
"""
第六部分:更改RGB颜色值
"""

def get_color(rlim=(0,255), glim=(0,255), blim=(0,255)):
    R = random.randint(rlim[0], rlim[1])
    G = random.randint(glim[0], glim[1])
    B = random.randint(blim[0], blim[1])
    return (R, G, B)



if __name__ == '__main__':
    init()
    menu()