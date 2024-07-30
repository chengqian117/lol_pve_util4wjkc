#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cv2
import numpy as np
import pyautogui
from pynput import keyboard

# 加载待匹配的图像模板
wq_png = cv2.imread('wqk2.png', 0)
bdk_png = cv2.imread('bdk.png', 0)
ym_png = cv2.imread('ym.png', 0)
w, h = wq_png.shape[::-1]


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

    threshold = 0.8
    # 模板匹配
    result = cv2.matchTemplate(gray_screenshot, wq_png, cv2.TM_CCORR_NORMED)
    a_list = np.where(result >= threshold)

    result = cv2.matchTemplate(gray_screenshot, bdk_png, cv2.TM_CCORR_NORMED)
    b_list = np.where(result >= 0.63)

    result = cv2.matchTemplate(gray_screenshot, ym_png, cv2.TM_CCORR_NORMED)
    c_list = np.where(result >= threshold)

    positions = []
    for pt in zip(*a_list[::-1]):
        center = (pt[0] + w // 2, pt[1] + h // 2)
        positions.append(center)
    for pt in zip(*b_list[::-1]):
        center = (pt[0] + w // 2, pt[1] + h // 2)
        positions.append(center)
    for pt in zip(*c_list[::-1]):
        center = (pt[0] + w // 2, pt[1] + h // 2)
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


positions = {}
index = -1


def on_press(key):
    global positions
    global index

    wq_list = {}
    bd_list = {}
    ym_list = {}
    try:
        if key == keyboard.Key.tab:
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
            else:
                print("No matching images found.")
                index = -1
        if key == keyboard.Key.space:
            print("空格")
            var = positions[index]
            pyautogui.click(var[0], var[1], button="left")
            positions = {}
            index = -1

    except Exception as e:
        print(f"Error: {e}")


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
