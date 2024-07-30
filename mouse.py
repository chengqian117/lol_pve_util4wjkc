import pyautogui
print("你好，世界")


# 获取屏幕尺寸
screenWidth, screenHeight = pyautogui.size()

# 计算目标位置的像素坐标（50%）
targetX = screenWidth * 0.667
targetY = screenHeight * 0.920

pyautogui.moveTo(targetX, targetY)
# pyautogui.moveRel(80, 70)
# pyautogui.rightClick()
pyautogui.leftClick()