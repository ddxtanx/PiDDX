#import pyautogui
#import pyscreenshot
# from gi.repository import Gdk
from PIL import Image, ImageGrab
import time
from threading import Thread, Condition
from mss import mss, tools
#960 x 1440

import sys

w = 256
h = 192

if len(sys.argv) == 3:
    w = int(sys.argv[1])
    h = int(sys.argv[2])

tot_time = 0

sx = 0
sy = 61
ex = sx+w
ey = sy+2*h



monitor = {"top": sy, "left": sx, "width": w, "height":2*h}
def parse_pix_data(fr_num):
    data = None
    with mss() as sct:
        data = sct.grab(monitor).bgra
        #print(len(data))
    #print(f"Len of data is {len(data)}")
    #top goes from 0,0 to 1760, 720
    #bot goes from 800,720 to 1760, 1440

    top = Image.new('RGB', (w, h))
    bot = Image.new('RGB', (w, h))

    ety = sy + h
    sby = ety
    eby = sby + h

    #print(f"{sy},{h},{ety},{eby}")

    for y_inc in range(0,h):
        for x_inc in range(0,w):
            x = x_inc
            y = y_inc

            coord = 4*(w*y + x)
            #print(f"T: {x},{y},{coord}")
            b,g,r,a = data[coord:coord+4]

            top.putpixel((x_inc, y_inc), (r,g,b))


    top.save(f"./frames/{fr_num}_top.png")

    px = 0
    py = 0

    for y_inc in range(0,h):
        for x_inc in range(0,w):
            x = x_inc
            y = h + y_inc

            #print(f"B: {x},{y},{coord}")

            #print(f"{x},{y}")

            coord = 4*(w*y + x)
            b,g,r,a = data[coord:coord+4]

            bot.putpixel((x_inc, y_inc), (r,g,b))

    bot.save(f"./frames/{fr_num}_bot.png")

# #t1 = Thread(target=master, args=(c_wait, c_done,))
# t2 = Thread(target=parse_top)
# t3 = Thread(target=parse_bot)

# t2.start()
# t3.start()
# #t1.start()

# #t1.join()
# #print("Master done")
# # t2.join()
# # print("Top done")
# # t3.join()
# # print("Bot done")

num_iters = 1000

for i in range(0,num_iters):
    s_time = time.time_ns() // 1000000
    #sc = pyautogui.screenshot(region=(800,0,960,1440))
    parse_pix_data(i)
    # t1 = Thread(target=parse_top, args=(i,))
    # t2 = Thread(target=parse_bot, args=(i,))
    # t1.start()
    # t2.start()
    # # t1.join()
    # # t2.join()
    e_time = time.time_ns() // 1000000
    time_taken = e_time - s_time
    if time_taken < 16:
        time.sleep((16 - time_taken) / 1000.0)
    tot_time += time_taken
    print(f"MS taken {time_taken}")

print(f"Avg time taken is {tot_time / num_iters} ms")

