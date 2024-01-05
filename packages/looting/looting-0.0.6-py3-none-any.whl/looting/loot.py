import pyautogui as pg
from time import sleep
import keyboard as k

def calc_positions_to_loot():
    k.wait("=")
    inicio_x, inicio_y = pg.position()
    k.wait("=")
    final_x, final_y = pg.position()

    size_between_pixels = int(round((final_x-inicio_x)/2, 0))
    global LOOT_0
    global LOOT_1
    global LOOT_2
    global LOOT_3
    global LOOT_4
    global LOOT_5
    global LOOT_8
    global LOOT_6
    global LOOT_7
    global LOOT_8

    LOOT_0 = (inicio_x + size_between_pixels, inicio_y + size_between_pixels)
    LOOT_1 = (inicio_x, inicio_y)
    LOOT_2 = (size_between_pixels + inicio_x, inicio_y)
    LOOT_3 = (final_x, inicio_y)
    LOOT_4 = (final_x, inicio_y + size_between_pixels)
    LOOT_5 = (final_x, final_y)
    LOOT_6 = (final_x - size_between_pixels, final_y)
    LOOT_7 = (inicio_x, final_y)
    LOOT_8 = (inicio_x , inicio_y + size_between_pixels)

def setup_config(x):
    calc_positions_to_loot()
    global loot_speed
    loot_speed = x


def lootting_around() :
    pg.PAUSE = loot_speed
    previous_position = pg.position()
    pg.keyDown("shift")       
    pg.rightClick(*LOOT_0) 
    pg.rightClick(*LOOT_1) 
    pg.rightClick(*LOOT_2)
    pg.rightClick(*LOOT_3)
    pg.rightClick(*LOOT_4)
    pg.rightClick(*LOOT_5)
    pg.rightClick(*LOOT_6)
    pg.rightClick(*LOOT_7)
    pg.rightClick(*LOOT_8)
    sleep(0.05)
    pg.keyUp("shift")
    pg.moveTo(*previous_position)