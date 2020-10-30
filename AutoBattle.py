import cv2
import pyautogui
from pynput.keyboard import Key, Listener
from time import localtime, sleep, strftime, time


def on_release(key):
    global running
    if key == Key.esc:
        running = False
        print('程式中止中，請稍後！')
        return False


class AutoBattle:

    # Set up and load needed images
    battles = int(input('要執行幾場戰鬥：'))
    time_per_battle = int(input('預計每場戰鬥花費時間(s)：'))
    finish_battles = 0

    img_stage_one = cv2.imread('pic/stage_one.png')
    img_stage_two = cv2.imread('pic/stage_two.png')
    img_complete = cv2.imread('pic/complete.png')

    @classmethod
    def initialize(cls):
        # Expected total costing time
        predict_time_cost = (cls.time_per_battle + 30) * cls.battles
        cost_min = predict_time_cost // 60
        cost_second = predict_time_cost % 60
        print(f'預計總花費時間為 {cost_min}分{cost_second}秒')

        # Messages before start
        print('自動戰鬥將於5秒後開始......')
        print('============================')
        print('==   Press Esc to stop!   ==')
        print('============================')
        sleep(5)

    @classmethod
    def battle(cls):

        for i in range(cls.battles):
            if not running:
                break

            start_time = time()
            start_time_str = strftime('%H:%M:%S', localtime(start_time))
            counts = 1
            print(f'----------Battle({i + 1}) starts at {start_time_str}----------')
            while running:
                stage_one = pyautogui.locateCenterOnScreen(cls.img_stage_one, confidence=0.8)
                stage_two = pyautogui.locateCenterOnScreen(cls.img_stage_two, confidence=0.8)
                stage_complete = pyautogui.locateCenterOnScreen(cls.img_complete, confidence=0.8)
                if stage_one:
                    pyautogui.click(stage_one, clicks=2, interval=0.25)
                    print(f'Completed Stage One')
                    sleep(2)
                elif stage_two:
                    pyautogui.click(stage_two, clicks=2, interval=0.25)
                    print(f'Completed Stage Two')
                    sleep(cls.time_per_battle)
                elif stage_complete:
                    sleep(5)
                    pyautogui.click(stage_complete, clicks=2, interval=0.25)
                    sleep(5)
                    cls.finish_battles += 1
                    end_time = time()
                    cost_time = round(end_time - start_time, 2)
                    print(f'Completed Battle({i + 1}) in {cost_time}s! \n')
                    break
                else:
                    print(f'Wait a moment({counts})')
                    counts += 1
                    sleep(5)

    @classmethod
    def run(cls):

        cls.initialize()

        start_time = int(time())
        cls.battle()

        # Calculate total cost time
        complete_time = int(time())
        final_time_cost = complete_time - start_time
        final_cost_min = final_time_cost // 60
        final_cost_second = final_time_cost % 60
        print(f'完成{cls.finish_battles}場戰鬥，總花費時間為 {final_cost_min}分{final_cost_second}秒')


if __name__ == '__main__':

    # Set up and load needed images
    running = True

    lis = Listener(on_release=on_release)
    lis.start()

    AutoBattle.run()
