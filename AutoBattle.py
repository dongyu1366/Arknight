import pyautogui
from time import localtime, sleep, strftime, time

# Set how many battles
battles = int(input('要執行幾場戰鬥：'))
time_per_battle = int(input('預計每場戰鬥花費時間(s)：'))
total_time_cost = (time_per_battle + 30) * battles
cost_min = total_time_cost // 60
cost_second = total_time_cost % 60
print(f'預計總花費時間為 {cost_min}分{cost_second}秒')

for i in range(battles):
    start_time = time()
    start_time_str = strftime('%H:%M:%S', localtime(start_time))
    counts = 1
    print(f'----------Battle({i+1}) starts at {start_time_str}----------')
    while True:
        stage_one = pyautogui.locateCenterOnScreen('pic/start_1.png', confidence=0.8)
        stage_two = pyautogui.locateCenterOnScreen('pic/start_2.png', confidence=0.8)
        stage_complete = pyautogui.locateCenterOnScreen('pic/complete.png', confidence=0.8)
        if stage_one:
            pyautogui.click(stage_one)
            sleep(2)
        elif stage_two:
            pyautogui.click(stage_two)
            sleep(time_per_battle)
        elif stage_complete:
            pyautogui.click(stage_complete)
            end_time = time()
            cost_time = round(end_time - start_time, 2)
            print(f'Battle {i+1} Finished in {cost_time}!')
            sleep(3)
            break
        else:
            print(f'Wait a moment -- {counts} times')
            counts += 1
            sleep(5)
