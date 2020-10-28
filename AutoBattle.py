import pyautogui
from time import sleep

# Set how many battles
battles = 4

for i in range(battles):
    count = 0
    while True:
        start1 = pyautogui.locateCenterOnScreen('pic/start_1.png', confidence=0.8)
        start2 = pyautogui.locateCenterOnScreen('pic/start_2.png', confidence=0.8)
        complete = pyautogui.locateCenterOnScreen('pic/complete.png', confidence=0.8)
        if start1:
            pyautogui.click(start1)
            sleep(2)
        elif start2:
            pyautogui.click(start2)
            sleep(120)  # Expect a battle will finish in 120s
        elif complete:
            pyautogui.click(complete)
            print(f'------Complete {i+1} battles------')
            sleep(3)
            break
        else:
            count += 1
            print(f'Wait a moment -- {i+1} battle -- {count} times')
            sleep(5)
