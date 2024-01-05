import pyautogui as pg
import keyboard as k
import looting.constants.constants as const

def calc_positions_to_loot():
    k.wait("=")
    inicio_x, inicio_y = pg.position()
    k.wait("=")
    final_x, final_y = pg.position()

    size_between_pixels = int(round((final_x-inicio_x)/2, 0))

    const.LOOT_0 = (inicio_x + size_between_pixels, inicio_y + size_between_pixels)
    const.LOOT_1 = (inicio_x, inicio_y)
    const.LOOT_2 = (size_between_pixels + inicio_x, inicio_y)
    const.LOOT_3 = (final_x, inicio_y)
    const.LOOT_4 = (final_x, inicio_y + size_between_pixels)
    const.LOOT_5 = (final_x, final_y)
    const.LOOT_6 = (final_x - size_between_pixels, final_y)
    const.LOOT_7 = (inicio_x, final_y)
    const.LOOT_8 = (inicio_x , inicio_y + size_between_pixels)