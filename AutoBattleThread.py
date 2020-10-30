import cv2
import pyautogui
import threading
from queue import Queue
from pynput.keyboard import Key, Listener
from time import localtime, sleep, strftime, time


class AutoBattle:

    # Set up and load needed images
    battles = int(input('要執行幾場戰鬥：'))
    time_per_battle = int(input('預計每場戰鬥花費時間(s)：'))

    img_stage_one = cv2.imread('pic/stage_one.png')
    img_stage_two = cv2.imread('pic/stage_two.png')
    img_complete = cv2.imread('pic/complete.png')

    @classmethod
    def initialize(cls):
        # Expected costing time
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
    def process_stage_one(cls):
        stage_one = pyautogui.locateCenterOnScreen(cls.img_stage_one, confidence=0.8)
        if stage_one:
            pyautogui.click(stage_one, clicks=2, interval=0.25)
            print(f'Completed Stage One')

    @classmethod
    def process_stage_two(cls, waiting_time):
        stage_two = pyautogui.locateCenterOnScreen(cls.img_stage_two, confidence=0.8)
        if stage_two:
            pyautogui.click(stage_two, clicks=2, interval=0.25)
            print(f'Completed Stage Two')
            sleep(waiting_time)

    @classmethod
    def process_stage_complete(cls, q):
        stage_complete = pyautogui.locateCenterOnScreen(cls.img_complete, confidence=0.8)
        if stage_complete:
            pyautogui.click(stage_complete, clicks=2, interval=0.25)
            q.put(stage_complete)

    @classmethod
    def run(cls):

        cls.initialize()

        # Start battles
        finish_battles = 0
        initial_time = int(time())

        for i in range(cls.battles):

            if not running:
                break

            start_time = time()
            start_time_str = strftime('%H:%M:%S', localtime(start_time))
            print(f'----------Battle({i + 1}) starts at {start_time_str}----------')

            while running:
                q = Queue()
                threads = [threading.Thread(target=cls.process_stage_one),
                           threading.Thread(target=cls.process_stage_two, args=(cls.time_per_battle,)),
                           threading.Thread(target=cls.process_stage_complete, args=(q,))]

                for thread in threads:
                    thread.start()

                for thread in threads:
                    thread.join()

                sleep(2)

                # End the round and calculate cost time
                if not q.empty():
                    finish_battles += 1
                    end_time = time()
                    spend_time = round(end_time - start_time, 2)
                    print(f'Completed Battle({i + 1}) in {spend_time}s! \n')
                    break

        # Calculate total cost time
        complete_time = int(time())
        final_time_cost = complete_time - initial_time
        final_cost_min = final_time_cost // 60
        final_cost_second = final_time_cost % 60
        print(f'完成{finish_battles}場戰鬥，總花費時間為 {final_cost_min}分{final_cost_second}秒')


def on_release(key):
    global running
    if key == Key.esc:
        running = False
        print('程式中止中，請稍後！')
        return False


if __name__ == '__main__':
    running = True

    lis = Listener(on_release=on_release)
    lis.start()

    AutoBattle.run()
