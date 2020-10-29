import pyautogui
import cv2
from time import localtime, sleep, strftime, time
from pynput.keyboard import Key, Listener


def on_press(key):
    global running
    if key == stop_key:
        running = False
        print('程式中止中，請稍後！')


class AutoBattle:

    @classmethod
    def start(cls):
        # Set configurations
        battles = int(input('要執行幾場戰鬥：'))
        time_per_battle = int(input('預計每場戰鬥花費時間(s)：'))
        predict_time_cost = (time_per_battle + 30) * battles
        cost_min = predict_time_cost // 60
        cost_second = predict_time_cost % 60
        print(f'預計總花費時間為 {cost_min}分{cost_second}秒')

        # Messages before start
        print('自動戰鬥將於5秒後開始......')
        print('============================')
        print('==   Press Esc to stop!   ==')
        print('============================')
        sleep(5)

        # Start battles
        cls.battle(battles, time_per_battle)

    @staticmethod
    def battle(battles, time_per_battle):
        finish_battles = 0
        initial_time = int(time())

        for i in range(battles):
            if not running:
                break

            start_time = time()
            start_time_str = strftime('%H:%M:%S', localtime(start_time))
            counts = 1
            print(f'----------Battle({i + 1}) starts at {start_time_str}----------')
            while running:
                stage_one = pyautogui.locateCenterOnScreen(img_stage_one, confidence=0.8)
                stage_two = pyautogui.locateCenterOnScreen(img_stage_two, confidence=0.8)
                stage_complete = pyautogui.locateCenterOnScreen(img_complete, confidence=0.8)
                if stage_one:
                    pyautogui.click(stage_one, clicks=2, interval=0.25)
                    print(f'Completed Stage One')
                    sleep(2)
                elif stage_two:
                    pyautogui.click(stage_two, clicks=2, interval=0.25)
                    print(f'Completed Stage Two')
                    sleep(time_per_battle)
                elif stage_complete:
                    sleep(2)
                    pyautogui.click(stage_complete, clicks=2, interval=0.25)
                    sleep(5)
                    finish_battles += 1
                    end_time = time()
                    cost_time = round(end_time - start_time, 2)
                    print(f'Completed Battle({i + 1}) in {cost_time}s!')
                    break
                else:
                    print(f'Wait a moment({counts})')
                    counts += 1
                    sleep(5)

        # Calculate total cost time
        complete_time = int(time())
        final_time_cost = complete_time - initial_time
        final_cost_min = final_time_cost // 60
        final_cost_second = final_time_cost % 60
        print(f'完成{finish_battles}場戰鬥，總花費時間為 {final_cost_min}分{final_cost_second}秒')


if __name__ == '__main__':

    # Set up and load needed images
    running = True
    stop_key = Key.esc

    img_stage_one = cv2.imread('pic/stage_one.png')
    img_stage_two = cv2.imread('pic/stage_two.png')
    img_complete = cv2.imread('pic/complete.png')

    lis = Listener(on_press=on_press)
    lis.start()

    AutoBattle.start()

    lis.stop()
