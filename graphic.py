import os
import pygame
import random
import gifList

screen = None
word_num = 0

sprite = []
capooList = []
capoo = []
pos_capoo = (0, 400)

def set_capoo(cap):
    global capoo
    capoo = cap

gif = {}

deep_color_lim = (192, 255)
light_color_lim = (0, 64)

def init(MAPX, MAPY, MAX_WORD_NUM):
    global screen, capooList, capoo, word_num
    word_num = MAX_WORD_NUM
    screen = pygame.display.set_mode((MAPX, MAPY), 0, 0)
    for gifFile in gifList.gif_list:
        gifName = gifFile[0]
        print(gifName)
        index = 1
        gif[gifName] = []
        while os.path.isfile(f"./pic/pic_{gifName}/{gifName}_{index}.png"):
            gif[gifName].append(pygame.transform.scale(pygame.image.load(f"./pic/pic_{gifName}/{gifName}_{index}.png"), gifFile[1]))
            index += 1
    capooList = [("capoo_miss",-1), ("capoo_lazy", 0), ("capoo_easy", 10), ("capoo_crazy", 20)]
    capoo = ["capoo_hello", 0, pos_capoo]


def get_not_green():
    return get_color(rlim=deep_color_lim, glim=light_color_lim, blim=deep_color_lim)


def get_green():
    return get_color(rlim=light_color_lim, glim=deep_color_lim, blim=light_color_lim)


def get_color(rlim=(0,255), glim=(0,255), blim=(0,255)):
    R = random.randint(rlim[0], rlim[1])
    G = random.randint(glim[0], glim[1])
    B = random.randint(blim[0], blim[1])
    return (R, G, B)


def paint(word, color, xx, yy, score, combo):
    global sprite, capoo, pos_capoo, word_num
    screen.fill((255, 255, 255))
    pygame.font.init()
    font = pygame.font.Font("arial.ttf", 40)

    TPP = 2
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
        if (len(sprite) > 0):
            sprite = [sp for sp in sprite if (sp[1] // TPP) < len(gif[sp[0]])]

    for i in range(0,word_num):
        fontRead = font.render(chr(word[i]-32),True,color[i])
        scoreShow = font.render("score:%s"%score,True,(255,0,0))
        comboShow = font.render("combo x%s"%combo, True, (255,0,0))

        screen.blit(fontRead,(xx[i],yy[i]))

    screen.blit(scoreShow, (20,20))
    if combo > 0:
        screen.blit(comboShow, (20,60))