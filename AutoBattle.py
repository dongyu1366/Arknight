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
    finish_battles = 0

    img_stage_one = cv2.imread('pic/stage_one.png')
    img_stage_two = cv2.imread('pic/stage_two.png')
    img_complete = cv2.imread('pic/complete.png')

    @classmethod
    def initialize(cls):
        # Expected costing time
        predict_time_cost = cls.time_per_battle * cls.battles
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
    def search_target(cls, q, image, stage, waiting_time, complete):
        mouse_position = pyautogui.locateCenterOnScreen(image, confidence=0.8)
        if mouse_position:
            q.put(mouse_position)
            q.put(stage)
            q.put(waiting_time)
            q.put(complete)

    @classmethod
    def battle(cls, battle_round):
        if running:
            q = Queue()
            threads = [threading.Thread(target=cls.search_target, args=(q, cls.img_stage_one, 1, 3, False,)),
                       threading.Thread(target=cls.search_target,
                                        args=(q, cls.img_stage_two, 2, (cls.time_per_battle - 20), False,)),
                       threading.Thread(target=cls.search_target, args=(q, cls.img_complete, 3, 5, True,))]

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            # Executed click
            if not q.empty():
                data = []
                for _ in range(4):
                    data.append(q.get())

                sleep(2)
                pyautogui.click(data[0], clicks=2, interval=0.25)
                print(f'Stage {data[1]} completed!')
                sleep(data[2])

                # Finish the battle round or not
                if not data[3]:
                    cls.battle(battle_round)

            else:
                print('Battle processing......')
                sleep(5)
                cls.battle(battle_round)

    @classmethod
    def run(cls):

        cls.initialize()
        start_time = time()

        # Start battles
        for i in range(cls.battles):
            if not running:
                break

            # The battle starting message
            battle_round = i + 1
            battle_start_time = time()
            battle_start_time_str = strftime('%H:%M:%S', localtime(battle_start_time))
            print(f'----------Battle({battle_round}) starts at {battle_start_time_str}----------')

            cls.battle(battle_round)

            # The battle ending message
            cls.finish_battles += 1
            battle_end_time = time()
            battle_spend_time = round(battle_end_time - battle_start_time, 2)
            print(f'Completed Battle({battle_round}) in {battle_spend_time}s! \n')

        # Calculate total cost time
        complete_time = time()
        final_time_cost = int(complete_time - start_time)
        final_cost_min = final_time_cost // 60
        final_cost_second = final_time_cost % 60
        print(f'完成{cls.finish_battles}場戰鬥，總花費時間為 {final_cost_min}分{final_cost_second}秒')


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
