#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2
import numpy as np

#import pyautogui
print("你好，世界")

# pyautogui.moveTo(600, 200)
# pyautogui.rightClick()
# pyautogui.click()

wq_png = cv2.imread('wqk2.png')
w, h = wq_png.shape[:-1]
bdk_png = cv2.imread('bdk.png')
ym_png = cv2.imread('ym.png')
test = cv2.imread('test3.png')
ym_test = cv2.imread('ym_test.png')
re_png = cv2.imread('re.png')
dd_png = cv2.imread('dd.png')
jy_png = cv2.imread('jy2.png')
nu_png = cv2.imread('nu2.png')
money_png = cv2.imread('money.png')
ys_png = cv2.imread('ys.png')
zd_png = cv2.imread('zd.png')


wq_png_threshold = 0.79
bdk_png_threshold = 0.614
ym_png_threshold=0.8

# result = cv2.matchTemplate(test, wq_png, cv2.TM_CCORR_NORMED)
# a_list = np.where(result >= 0.76)

imageMainR, imageMainG, imageMainB = cv2.split(ym_test)
imageNeedleR, imageNeedleG, imageNeedleB = cv2.split(ym_png)

result = cv2.matchTemplate(imageMainG, imageNeedleG, cv2.TM_CCORR_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
b_list = np.where(result >= 0.83)

# result = cv2.matchTemplate(test, ym_png, cv2.TM_CCORR_NORMED)
# c_list = np.where(result >= 0.8)

# # 初始化列表来存储匹配结果
# match_results = []
#
# # 遍历整个 result 矩阵，找到所有可能的匹配点
# for y in range(result.shape[0]):
#     for x in range(result.shape[1]):
#         match_val = result[y, x]
#         match_loc = (x, y)
#         match_results.append((match_val, match_loc))
#
# # 对 match_results 按匹配度排序（从高到低）
# match_results.sort(key=lambda x: x[0], reverse=True)
#
# # 输出前几个匹配结果（例如前 5 个）
# top_n = 20
# for i in range(min(top_n, len(match_results))):
#     match_val, match_loc = match_results[i]
#     print(f"Match {i + 1}: Value={match_val}, Location={match_loc}")

# # 找到匹配的最佳位置
# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
#
# print(min_loc)
#
# print(min_val)
#
# print(max_loc)
#
# print(max_val)

positions = []

# for pt in zip(*a_list[::-1]):
#     center = (pt[0] + w // 2, pt[1] + h // 2)
#     positions.append(center)
for pt in zip(*b_list[::-1]):
    center = (pt[0], pt[1])
    positions.append(center)
# for pt in zip(*c_list[::-1]):
#     center = (pt[0] + w // 2, pt[1] + h // 2)
#     positions.append(center)
# 设定网格大小
grid_size = 10

# 初始化网格字典来存储每个网格的点
grid_dict = {}
x_dict = {}


# 遍历点集，将点分配到网格
for x, y in positions:
    grid_key = x  # 计算网格的键
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
                         for points in x_dict.values() if points]


# 如果想要每个网格的中心点，可以这样计算
# representative_points = [(grid_key[0] * grid_size + grid_size // 2, grid_key[1] * grid_size + grid_size // 2)
#                          for grid_key in grid_dict.keys()]

# for grid_key in grid_dict.keys():
#

print(representative_points)
