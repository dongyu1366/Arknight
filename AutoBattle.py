import cv2
import pyautogui
import threading
from queue import Queue
from pynput.keyboard import Key, Listener
from time import localtime, sleep, strftime, time


class AutoBattle:

    img_stage_one = cv2.imread('pic/stage_one.png')
    img_stage_two = cv2.imread('pic/stage_two.png')
    img_complete = cv2.imread('pic/complete.png')

    def __init__(self):
        self.battles = int(input('要執行幾場戰鬥：'))
        self.time_per_battle = int(input('預計每場戰鬥花費時間(s)：'))
        self.finish_battles = 0
        self.stage_one = 1
        self.stage_two = 2
        self.stage_three = 3
        self.waiting_time_one = 3
        self.waiting_time_two = self.time_per_battle - 20
        self.waiting_time_three = 5

    def initialize(self):
        # Expected costing time
        predict_time_cost = self.time_per_battle * self.battles
        print(f'預計總花費時間為 {predict_time_cost // 60}分{predict_time_cost % 60}秒')

        # Messages before start
        print('自動戰鬥將於5秒後開始......')
        print('============================')
        print('==   Press Esc to stop!   ==')
        print('============================')
        sleep(5)

    @staticmethod
    def search_target(q, image, stage, waiting_time, complete):
        mouse_position = pyautogui.locateCenterOnScreen(image, confidence=0.8)
        if mouse_position:
            q.put(mouse_position)
            q.put(stage)
            q.put(waiting_time)
            q.put(complete)

    def click_target(self):
        if running:
            # Search target images
            q = Queue()
            threads = [threading.Thread(target=self.search_target,
                                        args=(q, self.img_stage_one, self.stage_one, self.waiting_time_one, False,)),
                       threading.Thread(target=self.search_target,
                                        args=(q, self.img_stage_two, self.stage_two, self.waiting_time_two, False,)),
                       threading.Thread(target=self.search_target,
                                        args=(q, self.img_complete, self.stage_three, self.waiting_time_three, True,))]

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            # Executed click
            if not q.empty():
                mouse_position = q.get()
                stage = q.get()
                waiting_time = q.get()
                complete = q.get()

                sleep(2)
                pyautogui.click(mouse_position, clicks=2, interval=0.25)
                print(f'Stage {stage} completed!')
                sleep(waiting_time)

                # Complete all clicks or not
                if not complete:
                    self.click_target()

            else:
                print('Battle processing......')
                sleep(5)
                self.click_target()

    def battle(self):
        if running:
            # The battle starting message
            current_battle_round = self.finish_battles + 1
            current_battle_start_time = time()
            current_battle_start_time_str = strftime('%H:%M:%S', localtime(current_battle_start_time))
            print(f'----------Battle({current_battle_round}) starts at {current_battle_start_time_str}----------')

            self.click_target()

            # Calculate costing time and print battle complete message
            current_battle_end_time = time()
            current_battle_cost_time = round(current_battle_end_time - current_battle_start_time, 2)
            print(f'Completed Battle({current_battle_round}) in {current_battle_cost_time}s! \n')
            self.finish_battles += 1

            if self.finish_battles < self.battles:
                self.battle()

    def run(self):

        self.initialize()
        start_time = time()
        self.battle()

        # Calculate total cost time
        complete_time = time()
        final_time_cost = int(complete_time - start_time)
        print(f'完成{self.finish_battles}場戰鬥，總花費時間為 {final_time_cost // 60}分{final_time_cost % 60}秒')


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

    AutoBattle().run()
