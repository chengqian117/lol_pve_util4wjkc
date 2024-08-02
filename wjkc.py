#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cv2
import numpy as np
import pyautogui
from pynput import keyboard
from pynput.mouse import Controller, Button

# 加载待匹配的图像模板
wq_png = cv2.imread('resource/wqk2.png')
bdk_png = cv2.imread('resource/bdk.png')
ym_png = cv2.imread('resource/ym.png')
re_png = cv2.imread('resource/re.png', 0)
w, h = wq_png.shape[:-1]

wq_png_threshold =0.84

bdk_png_threshold = 0.84


ym_png_threshold=0.83

def find_image_on_screen():
    global wq_png
    global bdk_png
    global ym_png
    # 截取屏幕
    screenshot = pyautogui.screenshot()
    # # 将截图转换为 OpenCV 图像格式
    # screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    #
    # # 显示截屏图像
    # cv2.imshow('Screenshot', screenshot)
    #
    # # 等待用户按键关闭窗口
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    imageMainR, imageMainG, imageMainB = cv2.split(screenshot)
    imageNeedleR, imageNeedleG, imageNeedleB = cv2.split(bdk_png)
    imageNeedleR2, imageNeedleG2, imageNeedleB2 = cv2.split(wq_png)
    imageNeedleR3, imageNeedleG3, imageNeedleB3 = cv2.split(ym_png)


    global wq_png_threshold
    global bdk_png_threshold
    global ym_png_threshold
    # 模板匹配
    result = cv2.matchTemplate(imageMainG, imageNeedleG2, cv2.TM_CCORR_NORMED)
    a_list = np.where(result >= wq_png_threshold)

    result = cv2.matchTemplate(imageMainR, imageNeedleR, cv2.TM_CCORR_NORMED)
    b_list = np.where(result >= bdk_png_threshold)

    result = cv2.matchTemplate(imageMainG, imageNeedleG3, cv2.TM_CCORR_NORMED)
    c_list = np.where(result >= ym_png_threshold)

    positions = []
    for pt in zip(*a_list[::-1]):
        center = (pt[0] + 100, pt[1] +200)
        positions.append(center)
    for pt in zip(*b_list[::-1]):
        center = (pt[0] + 100, pt[1] + 200)
        positions.append(center)
    for pt in zip(*c_list[::-1]):
        center = (pt[0] + 100, pt[1] + 200)
        positions.append(center)

    x_dict = {}
    for x, y in positions:
        grid_key = x
        x_ter = {}
        if grid_key not in x_dict:
            if len(x_dict) == 0:
                x_dict[grid_key] = []
                x_dict[grid_key].append((x, y))
            else:
                for x_value in list(x_dict.keys()):
                    if abs(x - x_value) <= 15:
                        x_dict[x_value].append((x, y))
                        x_ter = {}
                        break
                    else:
                        x_ter[0] = x

                if len(x_ter) != 0:
                    x_dict[grid_key] = []
                    x_dict[grid_key].append((x, y))

    print(x_dict)
    sorted_x_dict = {k: x_dict[k] for k in sorted(x_dict)}
    # 提取每个网格的代表性点（这里选择网格内的第一个点作为代表）
    representative_points = [(np.mean([p[0] for p in points]), np.mean([p[1] for p in points]))
                             for points in sorted_x_dict.values() if points]

    # 如果想要每个网格的中心点，可以这样计算
    # representative_points = [(grid_key[0] * grid_size + grid_size // 2, grid_key[1] * grid_size + grid_size // 2)
    #                          for grid_key in grid_dict.keys()]

    # for grid_key in grid_dict.keys():
    #

    print(representative_points)
    return representative_points


def find_re_image_on_screen():

    global re_png
    # 截取屏幕
    screenshot = pyautogui.screenshot()
    # # 将截图转换为 OpenCV 图像格式
    # screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    #
    # # 显示截屏图像
    # cv2.imshow('Screenshot', screenshot)
    #
    # # 等待用户按键关闭窗口
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # 模板匹配
    result = cv2.matchTemplate(gray_screenshot, re_png, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val>=0.99:
        return max_loc
    else:
        return None

positions = {}
index = -1


def on_press(key):
    global positions
    global index

    wq_list = {}
    bd_list = {}
    ym_list = {}
    try:
        if key == keyboard.KeyCode.from_char("q"):
            positions = find_image_on_screen()

            if len(positions) > 0:

                print("Found positions: ", positions)
                index = index + 1
                print(index)
                if index >= len(positions):
                    index = 0
                var = positions[index]
                print(var)
                pyautogui.moveTo(var[0], var[1])
                # if len(positions) == 1:
                #     var = positions[0]
                #     pyautogui.moveTo(var[0], var[1])
                #     mouse = Controller()
                #     mouse.click(Button.left, 1)
                #     positions = {}
                #     index = -1
                # else:
                #     print("Found positions: ", positions)
                #     index = index + 1
                #     print(index)
                #     if index >= len(positions):
                #         index = 0
                #     var = positions[index]
                #     print(var)
                #     pyautogui.moveTo(var[0], var[1])
            else:
                print("No matching images found.")
                index = -1
        if key == keyboard.Key.space:
            # print("空格")
            mouse = Controller()
            mouse.click(Button.left, 1)
            positions = {}
            index = -1
        # 2024/8/2 回城bug修复
        # if key == keyboard.KeyCode.from_char("b"):
        #     # 获取屏幕尺寸
        #     screen_width, screen_height = pyautogui.size()
        #
        #     # 计算目标位置的像素坐标（50%）
        #     target_x = screen_width * 0.670
        #     target_y = screen_height * 0.920
        #
        #     pyautogui.moveTo(target_x, target_y)
        #     mouse = Controller()
        #     mouse.click(Button.left, 1)
        if key == keyboard.KeyCode.from_char("f"):
            print("re")
            max_loc = find_re_image_on_screen()

            if max_loc is not None:
                print("Found re positions: ", max_loc)
                var = max_loc
                pyautogui.moveTo(var[0], var[1])
            else:
                print("No re images found.")
    except Exception as e:
        print(f"Error: {e}")


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
