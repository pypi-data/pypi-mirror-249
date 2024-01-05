import looting.configs.setup as init
import pyautogui as pg
import looting.constants.constants as const
from time import sleep

def init_setup():
    init.calc_positions_to_loot()


def lootting_around() :
    pg.PAUSE = 0.001
    previous_position = pg.position()
    pg.keyDown("shift")       
    pg.rightClick(*const.LOOT_0) 
    pg.rightClick(*const.LOOT_1) 
    pg.rightClick(*const.LOOT_2)
    pg.rightClick(*const.LOOT_3)
    pg.rightClick(*const.LOOT_4)
    pg.rightClick(*const.LOOT_5)
    pg.rightClick(*const.LOOT_6)
    pg.rightClick(*const.LOOT_7)
    pg.rightClick(*const.LOOT_8)
    sleep(0.05)
    pg.keyUp("shift")
    pg.moveTo(*previous_position)