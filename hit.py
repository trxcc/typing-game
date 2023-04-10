import pygame
import gifList
import random

def hit(sprite, pos, speed, acc):
    gifName = random.choice(
        ["capoo_hit1",
         "capoo_hit2_left",
         "capoo_hit2_right",
         "capoo_hit3",
         "capoo_hit4"])
    return get_impact(sprite, gifName, pos, speed, acc)


def get_impact(sprite, gifName, pos, speed, acc):
    for gif in gifList.gif_list:
        if gif[0] == gifName:
            sprite.append([gifName,
                           0,
                           (pos[0] + gif[2][0], pos[1] + gif[2][1])])
            return (speed[0] + gif[3][0], speed[1] + gif[3][1])
    print("Not found")
