import numpy as np
import cv2
from PIL import Image
from collections import namedtuple
import pyautogui

global dimensions
dimensions:tuple[tuple[int, int, int, int], tuple[int, int, int, int]]

CROP_LIFE_AND_MANA = (1,6,93,7)
RANGE_MANA_POSITION = 13


HSV_LIFE_MINIMA = (0, 58.7, 29.4)
HSV_LIFE_MAXIMA = (0, 255, 255)

HSV_MANA_MINIMA = (172, 23, 66)
HSV_MANA_MAXIMA = (173 , 255, 255)


HEART_IMAGE = [[[68, 68, 69], [84, 54, 54], [122, 83, 83], [131, 65, 65], [89, 56, 55], [74, 74, 75], [88, 55, 54], [131, 65, 65], [131, 65, 65], [88, 61, 60], [68, 68, 69]], [[67, 59, 59], [148, 107, 107], [201, 167, 167], [144, 46, 46], [144, 46, 46], [94, 53, 52], [144, 46, 46], [144, 46, 46], [144, 46, 46], [102, 54, 54], [72, 72, 73]], [[94, 64, 64], [201, 160, 160], [176, 78, 78], [167, 51, 51], [167, 51, 51], [167, 51, 51], [167, 51, 51], [167, 51, 51], [167, 51, 51], [167, 51, 51], [96, 67, 66]], [[125, 85, 85], [192, 96, 96], [192, 64, 64], [192, 64, 64], [192, 64, 64], [192, 64, 64], [192, 64, 64], [192, 64, 64], [192, 64, 64], [192, 64, 64], [123, 63, 63]], [[124, 64, 64], [211, 79, 79], [219, 79, 79], [219, 79, 79], [219, 79, 79], [219, 79, 79], [219, 79, 79], [219, 79, 79], [219, 79, 79], [211, 79, 79], [124, 64, 64]], [[103, 56, 56], [219, 91, 91], [241, 97, 97], [241, 97, 97], [241, 97, 97], [241, 97, 97], [241, 97, 97], [241, 97, 97], [241, 97, 97], [219, 91, 91], [103, 55, 55]], [[77, 78, 78], [85, 58, 57], [193, 86, 86], [251, 113, 113], [255, 113, 113], [255, 113, 113], [255, 113, 113], [251, 113, 113], [193, 87, 87], [87, 59, 58], [72, 72, 73]], [[68, 68, 69], [73, 74, 74], [89, 61, 60], [211, 107, 107], [255, 125, 125], [255, 125, 125], [255, 125, 125], [211, 107, 107], [85, 58, 57], [74, 74, 75], [68, 68, 69]], [[78, 78, 79], [68, 68, 69], [72, 72, 73], [85, 65, 65], [180, 97, 97], [221, 113, 113], [180, 97, 97], [85, 65, 65], [73, 73, 74], [68, 68, 69], [65, 66, 66]], [[72, 72, 72], [65, 66, 66], [72, 72, 73], [74, 74, 75], [84, 64, 64], [183, 93, 93], [81, 61, 61], [69, 70, 70], [69, 70, 70], [70, 70, 71], [68, 68, 69]], [[80, 80, 81], [72, 72, 73], [65, 66, 65], [70, 70, 71], [76, 76, 77], [118, 54, 54], [73, 74, 74], [74, 74, 75], [72, 72, 73], [65, 66, 66], [70, 70, 71]]]


def get_bar_dimensions(location_life):
    if location_life != None:
        inicio_x = location_life.left + 14
        inicio_y = location_life.top + 5
        final_x = inicio_x + 92
        final_y = location_life.height + location_life.top - 5
        return (inicio_x, inicio_y, final_x, final_y), (inicio_x, inicio_y+RANGE_MANA_POSITION, final_x, final_y+RANGE_MANA_POSITION)
    else:
        return None

def set_dimensions(img:Image):
    ar = Image.fromarray(np.uint8(np.asarray(HEART_IMAGE)))
    dimensions = get_bar_dimensions(location_life=pyautogui.locate(ar, img, confidence=.8))

def convert_to_HSV(img:Image):
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2HSV_FULL)

def get_bars(image:Image):
    img_t = image
    if(dimensions != None):
        life = img_t.crop(dimensions[0])
        mana = img_t.crop(dimensions[1])
        return convert_to_HSV(life), convert_to_HSV(mana)
    else:
        return (np.array([]), np.array([]))

def main(image:Image):
    lifemana = namedtuple("lifemana", ["life","mana"])
    life, mana = get_bars(image=image)

    if((life.size != 0) and (mana.size != 0)):
        life_mask = cv2.inRange(life, HSV_LIFE_MINIMA, HSV_LIFE_MAXIMA)
        mana_mask = cv2.inRange(mana, HSV_MANA_MINIMA, HSV_MANA_MAXIMA)

        life = int((np.count_nonzero(life_mask)/92)*100)
        mana = int((np.count_nonzero(mana_mask)/92)*100)

        return lifemana(life,mana)
    else:
        return None
    
"""Esta funcão tem como responsabilidade configurar as variáveeis para localizar a barra de vida e mana do personagem

    Args:
        Uma imagem (Image) do tipo Image da lib Pillow

    Returns:
        

    Raises:
        ValueError: Parâmetro incorreto.

"""
def setup(image:Image):
    set_dimensions(img=image)