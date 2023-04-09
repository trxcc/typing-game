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
3. 更改颜色 每个字母只有一个颜色
4. 更改背景 将背景改为图片
"""
import pygame, sys
# 导入随机函数模块
import random
 
"""
第一部分：主函数
"""
def menu():
    # 1.设置窗口标题
    pygame.display.set_caption("打字游戏")
    # 2.死循环
    while True:
        # 3.设置背景颜色填充
        # screen.fill((255, 255, 255))
        # 绘制哪张图，以及起始点位置
        screen.blit(back, (0, 0))
 
        # 4.调用业务处理函数
        action()
        # 5.调用图形图案绘制函数
        paint()
        # 7.屏幕刷新延迟
        pygame.time.delay(speed)
        # 6.设置窗口刷新屏幕
        pygame.display.update()
 
"""
第二部分:变量声明初始化区域
"""
# 设置窗体
screen = pygame.display.set_mode((800, 600), 0, 0)
# 存储字母列表
word = []
# 字母颜色列表
color = []
# 存储字母坐标值列表
xx = []
yy = []
speed_unit = []
state = []
# 存储得分
score = 0
# 存储RGB颜色值
R = 0
G = 0
B = 0
# 存储速度
speed = 20
# 加载图片（选一张好看的图片作为背景）
back = pygame.image.load("1.png")
 
"""
第五部分:初始化函数
"""
def init():
    for i in range(0,12): #range(0,10):
        # 字母 ===》A :65  a==>97
        word.append(97 + i)
        # 调用updateColor
        updateColor()
        color.append((R,G,B))
        # 坐标值
        xx.append(random.randint(0,760))
        yy.append(random.randint(0,300))
        speed_unit.append(random.choice([random.uniform(1,1.3), random.uniform(2,2.3)]))
        state.append(True)

 
"""
第三部分:业务逻辑处理区域
"""
def action():
    global score
    # 4.1 循环迭代事件监听
    for event in pygame.event.get():
        # 4.2 判断是否退出系统
        if event.type == pygame.QUIT:
            sys.exit()
        # 4.4 循环比对
        if event.type == pygame.KEYDOWN:  # 键盘按下
            # 4.5 循环遍历与按键比较
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
                # 4.7 业务处理
                updateColor()
                color[max_idx] = (R,G,B)
                speed_unit[max_idx] = -5
                state[max_idx] = False
                # word[max_idx] = random.randint(65,90)  # 使得word“消失”
                # xx[max_idx] = random.randint(0,750)  # xx坐标另产生一个随机数，表现为“消失”
                # # 使得yy坐标“消失”,yy坐标变负号，消失在屏幕看不见的位置
                # yy[max_idx] = -random.randint(0,600)
                score += 5

    # 4.3 字母移动
    for i in range(0,12):
        yy[i] += speed_unit[i]
        # 循环判断
        if yy[i] > 600:
            yy[i] = -50
            score -= 20
        elif yy[i] < -50:
            word[i] = random.randint(97,122)  # 使得word“消失”
            xx[i] = random.randint(0,760)  # xx坐标另产生一个随机数，表现为“消失”
                # 使得yy坐标“消失”,yy坐标变负号，消失在屏幕看不见的位置
            # yy[i] = -random.randint(0,600)
            speed_unit[i] = random.uniform(1,2)
            state[i] = True
    # 4.4 根据分数修改速度
    global speed
    if score > 500:  # 20个字
        speed = 3
    elif score > 250:  # 50个字
        speed = 5
    elif score > 100:  # 100个字
        speed = 10
 
 
"""
第四部分:图形图案绘制区域
"""
def paint():
    # 4.1 初始化字体
    pygame.font.init()
    # 4.2 设置字体样式 （ps: wryh.ttf是字体库的文件，该文件已经上传，下载后和项目文件放到一个文件夹中）
    font = pygame.font.Font("arial.ttf", 40)
    # 4.3 循环迭代
    for i in range(0,12):
        
        # 4.4 设置绘制内容
        fontRead = font.render(chr(word[i]-32),True,color[i]) # int转字符串，字体为黑色
        scoreShow = font.render("score:%s"%score,True,(255,0,0))
        # 4.5 设置绘制内容的坐标
        screen.blit(fontRead,(xx[i],yy[i]))  # 将字符串绘制到该窗口上
        # 4.6 绘制分数
        screen.blit(scoreShow, (20,20))  # 将字符串绘制到该窗口上
 
"""
第六部分:更改RGB颜色值
"""
def updateColor():
    global R,G,B
    """
    R = 140
    G = 200
    B = 10
    """
    R = random.randint(0,255)
    G = random.randint(0, 255)
    B = random.randint(0, 255)

 
# main函数
if __name__ == '__main__':
    init()
    menu()