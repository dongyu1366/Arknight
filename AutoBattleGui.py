import cv2
import pyautogui
import threading
from queue import Queue
import tkinter as tk
from PIL import Image, ImageTk
from time import localtime, sleep, strftime, time


# Application UI
class Application:
    def __init__(self, master):
        self.master = master

        master.title('明日方舟自動戰鬥工具')
        master.geometry('400x450')
        master.resizable(width=0, height=0)

        self.btn_status = 0

        # Set the icon
        self.image = Image.open('pic/icon.png')
        self.photo = ImageTk.PhotoImage(self.image)
        master.tk.call('wm', 'iconphoto', root._w, self.photo)

        # The input area
        self.input_frame = tk.Frame(self.master)
        self.input_frame.pack(side=tk.TOP)

        self.battle_entry = tk.Entry(self.input_frame)
        self.time_entry = tk.Entry(self.input_frame)

        self.battle_label = tk.Label(self.input_frame, text='要打幾場：').grid(sticky='w', padx=5, pady=5)
        self.battle_entry.grid(row=0, column=1)
        self.time_label = tk.Label(self.input_frame, text='每場耗時(s)：').grid(sticky='w', padx=5, pady=5)
        self.time_entry.grid(row=1, column=1)
        self.confirm_btn = tk.Button(self.input_frame, text='確認', command=self.confirm)
        self.confirm_btn.grid(row=0, column=2, columnspan=2, rowspan=2, padx=5, pady=5)

        # The button area
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(side=tk.TOP)

        self.start_btn = tk.Button(self.button_frame, text='開始', command=lambda: self.thread_it(self.start),
                                   state=tk.DISABLED)
        self.stop_btn = tk.Button(self.button_frame, text='停止', command=self.stop, state=tk.DISABLED)
        self.start_btn.grid(row=0, column=0, padx=5, pady=5)
        self.stop_btn.grid(row=0, column=1, padx=5, pady=5)

        # The log area
        self.log_frame = tk.Frame(self.master, width=400, height=300)
        self.log_frame.pack(side=tk.TOP)

        self.y_scrollbar = tk.Scrollbar(self.log_frame)
        self.log = tk.Text(self.log_frame, height=20, width=50)
        self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log.pack(side=tk.LEFT, fill=tk.Y)
        self.y_scrollbar.config(command=self.log.yview)
        self.log.config(yscrollcommand=self.y_scrollbar.set)

    def confirm(self):
        global running

        try:
            battles = int(app.battle_entry.get())
            time_per_battle = int(app.time_entry.get())
            if battles > 0 and time_per_battle > 0:
                running = True

                # Activate the start button
                self.btn_status = 1
                self.switch_button_state()

                predict_time_cost = time_per_battle * battles
                self.add_log(f'設定完成')
                self.add_log(f'戰鬥：{battles}場')
                self.add_log(f'預計總花費時間為 {predict_time_cost // 60}分{predict_time_cost % 60}秒')
            else:
                self.add_log('輸入數字不應小於0')
        except ValueError:
            self.add_log('請輸入正確數字')

    def start(self):
        battles = int(app.battle_entry.get())
        time_per_battle = int(app.time_entry.get())

        if battles > 0:
            # Disable the confirm button
            self.btn_status = 2
            self.switch_button_state()

            AutoBattle(battles, time_per_battle).run()

            # Activate the confirm button
            self.btn_status = 0
            self.switch_button_state()

    def stop(self):
        global running

        running = False
        self.add_log('程式中止中，請稍後！')

    def switch_button_state(self):
        if self.btn_status == 0:
            self.confirm_btn['state'] = tk.NORMAL
            self.start_btn['state'] = tk.DISABLED
            self.stop_btn['state'] = tk.DISABLED
        elif self.btn_status == 1:
            self.confirm_btn['state'] = tk.NORMAL
            self.start_btn['state'] = tk.NORMAL
            self.stop_btn['state'] = tk.DISABLED
        else:
            self.confirm_btn['state'] = tk.DISABLED
            self.start_btn['state'] = tk.DISABLED
            self.stop_btn['state'] = tk.NORMAL

    def add_log(self, string):
        self.log.insert(tk.END, string + '\n')
        self.log.see("end")

    @staticmethod
    def thread_it(func, *args):
        thread = threading.Thread(target=func, args=args)
        thread.setDaemon(True)
        thread.start()


class AutoBattle:

    def __init__(self, battles, time_per_battle):
        self.img_stage_one = cv2.imread('pic/stage_one.png')
        self.img_stage_two = cv2.imread('pic/stage_two.png')
        self.img_complete = cv2.imread('pic/complete.png')

        self.battles = battles
        self.finish_battles = 0
        self.stage_one = 1
        self.stage_two = 2
        self.stage_three = 3
        self.waiting_time_one = 3
        self.waiting_time_two = time_per_battle - 20
        self.waiting_time_three = 5

    @staticmethod
    def initialize():
        app.add_log('=============================')
        app.add_log('==    自動戰鬥將於5秒後開始   ==')
        app.add_log('=============================')
        sleep(5)

    @staticmethod
    def search_target(q, img, stage, waiting_time, complete):
        mouse_position = pyautogui.locateCenterOnScreen(img, confidence=0.8)
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
                app.add_log(f'Stage {stage} completed!')
                sleep(waiting_time)

                # Complete all clicks or not
                if not complete:
                    self.click_target()

            else:
                app.add_log('Battle processing......')
                sleep(5)
                self.click_target()

    def battle(self):
        if running:
            # The battle starting message
            current_battle_round = self.finish_battles + 1
            current_battle_start_time = time()
            current_battle_start_time_str = strftime('%H:%M:%S', localtime(current_battle_start_time))
            app.add_log(f'-------Battle({current_battle_round}) starts at {current_battle_start_time_str}-------')

            self.click_target()

            # Calculate costing time and print battle complete message
            current_battle_end_time = time()
            current_battle_cost_time = round(current_battle_end_time - current_battle_start_time, 2)
            app.add_log(f'Completed Battle({current_battle_round}) in {current_battle_cost_time}s!\n')
            self.finish_battles += 1

            if self.finish_battles < self.battles:
                self.battle()

    def run(self):
        if running:
            self.initialize()
            start_time = time()
            self.battle()

            # Calculate total cost time
            complete_time = time()
            final_time_cost = int(complete_time - start_time)
            app.add_log('*****************************')
            app.add_log(f'完成{self.finish_battles}場戰鬥，總花費時間為 {final_time_cost // 60}分{final_time_cost % 60}秒')
            app.add_log('*****************************')


if __name__ == '__main__':
    running = False

    root = tk.Tk()

    app = Application(root)

    root.mainloop()
