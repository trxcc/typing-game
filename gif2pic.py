import gifList
import os
from PIL import Image, ImageSequence

if __name__ == "__main__":
    for gif in gifList.gif_list:
        gifName = gif[0]
        if not os.path.isfile(f"./pic/gif/{gifName}.gif"):
            continue
        if gifName[-1]=='\n':
            gifName = gifName[:-1]
        image = Image.open(f"./pic/gif/{gifName}.gif")
        if not os.path.exists(f"./pic/pic_{gifName}/"):
            os.mkdir(f"./pic/pic_{gifName}/")
        index = 0
        for frame in ImageSequence.all_frames(image):
            frame.save(f"./pic/pic_{gifName}/{gifName}_{index}.png", quality=100)
            index += 1