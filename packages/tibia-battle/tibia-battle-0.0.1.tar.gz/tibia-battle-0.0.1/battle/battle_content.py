import pyautogui as pg
from PIL import Image
import constants.constants as const


def get_battle_container_region(battle_icon_location, height_screen:int):
    return (battle_icon_location.left + const.BATTLE_IMAGE_MINUS_ONE, 
            battle_icon_location.top, 
            (battle_icon_location.left + const.BATTLE_IMAGE_MINUS_ONE )+const.CONTAINER_WIDTH, 
            height_screen - battle_icon_location.top
        )

def battle_container_location(img:Image, battle_icon_location):
    region_to_locate_battle_container = get_battle_container_region(battle_icon_location=battle_icon_location, height_screen=img.height)
    botoom_image = const.BOTTOM_BATTLE_CONTAINER
    bt = pg.locate(botoom_image, img, region=region_to_locate_battle_container, confidence=.99)
    const.BATTLE_CONTAINER_LOCATION = (battle_icon_location.left+const.BATTLE_IMAGE_MINUS_ONE, battle_icon_location.top + const.BATTLE_IMAGE_PLUS_TWELVE, battle_icon_location.left+bt.width, bt.top)

def localize_battle_list(img:Image):
    return pg.locate(const.BATTLE_IMAGE, img, confidence=.9)

def battle_container_setup(img:Image):
    battle_container_location(img=img, battle_icon_location=localize_battle_list(img=img))
    adjust_battle_list_size()

def adjust_battle_list_size():
    pg.moveTo(int(const.BATTLE_CONTAINER_LOCATION[2]), const.BATTLE_CONTAINER_LOCATION[3], .7)
    pg.dragTo(x=const.BATTLE_CONTAINER_LOCATION[2], y=const.BATTLE_CONTAINER_LOCATION[1]+const.BATTLE_WITH_EIGTH_SLOTS, duration= .5, button='left')

def count_creatures(img:Image):
    count_creatures = 0
    imgCropped = img.crop(const.BATTLE_CONTAINER_LOCATION)
    slots = int(imgCropped.size[1]/22)
    for i in range(slots-1) :
        x = 22
        y = (i * 22) + 16
        if imgCropped.getpixel((x,y)) == (0,0,0) :
            count_creatures = count_creatures+1
    return count_creatures

def check_attacking_pixel(img:Image):
    imgCropped = img.crop(const.BATTLE_CONTAINER_LOCATION)
    slots = int(imgCropped.size[1]/22)
    for i in range(slots) :
        x:int = 0
        y:int = 0
        if i == 0 :
            y = 0
        else :
            y = (i * 22) + 1
        if imgCropped.getpixel((x,y)) == (255,0,0) :
            return True
        