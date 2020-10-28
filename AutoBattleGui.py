import tkinter as tk
import pyautogui
from time import sleep, time, localtime, strftime

# Set configuration
running = True
battles = 0
time_per_battle = 100

rounds = 0
counts = 1
start_time = time()


# Define main functions
def start_battle():
    global rounds
    global start_time
    rounds += 1
    if running and rounds <= battles:
        start_time = time()
        start_time_str = strftime('%H:%M:%S', localtime(start_time))
        print(f'------Battle({rounds}) starts at {start_time_str}------')
        execute_battle()


def execute_battle():
    global rounds
    global counts
    if running:
        stage_one = pyautogui.locateCenterOnScreen('pic/start_1.png', confidence=0.8)
        stage_two = pyautogui.locateCenterOnScreen('pic/start_2.png', confidence=0.8)
        stage_complete = pyautogui.locateCenterOnScreen('pic/complete.png', confidence=0.8)
        sleep(1)
        if stage_one:
            pyautogui.click(stage_one)
            sleep(2)
            window.after(100, execute_battle)
        elif stage_two:
            pyautogui.click(stage_two)
            sleep(time_per_battle)  # Wait until the battle finished
            window.after(100, execute_battle)
        elif stage_complete:
            pyautogui.click(stage_complete)
            end_time = time()
            cost_time = round(end_time - start_time, 2)
            print(f'Battle {rounds} Finished in {cost_time}!')
            counts = 1
            sleep(5)
            window.after(100, start_battle)
        else:
            print(f'Wait a moment -- {counts} times!')
            counts += 1
            sleep(5)
            window.after(100, execute_battle)


def start():
    global running
    global battles
    global time_per_battle
    global rounds
    global counts
    running = True
    rounds = 0
    counts = 1
    battles = int(battle_entry.get())
    time_per_battle = int(time_entry.get())
    whole_time_cost = (time_per_battle + 30) * battles
    print('----------Ready----------')
    print(f'Expected {battles} Battles in {whole_time_cost}s')
    print('----------Ready----------')


def stop():
    global running
    running = False
    print('----------Stop----------')


# Set up GUI
window = tk.Tk()
window.title('ARKNIGHTS APP')
window.geometry('300x300')
window.configure(background='white')

header_label = tk.Label(window, text='Auto Battle')
header_label.pack()

# Set estimated time of a battle
time_frame = tk.Frame(window)
time_frame.pack(side=tk.TOP)
time_label = tk.Label(time_frame, text='每場耗時(s)')
time_label.pack(side=tk.LEFT)
time_entry = tk.Entry(time_frame)
time_entry.pack(side=tk.LEFT)

# Set the number of battles
battle_frame = tk.Frame(window)
battle_frame.pack(side=tk.TOP)
battle_label = tk.Label(battle_frame, text='要打幾場')
battle_label.pack(side=tk.LEFT)
battle_entry = tk.Entry(battle_frame)
battle_entry.pack(side=tk.LEFT)
confirm_btn = tk.Button(text='Confirm', command=start)
confirm_btn.pack()

button_frame = tk.Frame(window)
button_frame.pack(side=tk.TOP)
start_btn = tk.Button(button_frame, text='Start', command=start_battle)
start_btn.pack(side=tk.LEFT)
stop_btn = tk.Button(button_frame, text='Stop', command=stop)
stop_btn.pack(side=tk.LEFT)

# 運行主程式
window.mainloop()