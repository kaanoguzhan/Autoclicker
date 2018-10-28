import ctypes
import threading
from time import sleep
from tkinter import *

from Clicker.KeyClicker import key_press
from Clicker.MouseClicker import LeftClicker
from Constants import *
from Enum import *
from Memory import *
from RandomDelayPicker import *

SetCursorPos = ctypes.windll.user32.SetCursorPos
mouse_event = ctypes.windll.user32.mouse_event
keyboard_event = ctypes.windll.user32.keybd_event
testing = False
clicking = False
mode = mouse_click


class Timer:
    label = None
    time = None
    func = None
    aborted = False
    running = False
    frame = None

    def __init__(self):
        self.aborted = False

    def set(self, label, time, func):
        self.label = label
        self.time = time
        self.func = func
        self.aborted = False

    def time_worker(self):
        for i in range(0, self.time):
            self.label.config(text="Starting in...  " + str(self.time - i))
            sleep(1)
            if self.aborted:
                self.label.config(text="! Aborted !")
                frame.btn_clicker_start.config(state="active", text="Start")
                self.running = False
                return True
        self.running = False
        self.func()

    def run(self, framee):
        self.frame = framee
        if self.running:
            return
        frame.btn_clicker_start.config(text="Cancel")
        t = threading.Thread(target=self.time_worker)
        t.start()
        self.running = True

    def abort(self):
        frame.btn_clicker_start.config(state="disabled", text="Canceling")
        self.aborted = True


class Clicker:
    running = False

    def __init__(self, clickmem, txt_key_hex):
        self.txt_key_hex = txt_key_hex
        self.clickmemory = clickmem
        self.LClicker = LeftClicker(clickmem)

    def worker(self):
        global mode
        delay_before = 0
        delay_between = 0
        while self.running:
            delay_before = rand_delay_before(delay_before)
            delay_between = rand_delay_between(delay_between)
            if clickmemory.totalClick > 100000:
                break
            if mode is mouse_click:
                if self.LClicker.left_click(delay_before=delay_before,
                                            delay_between=delay_between,
                                            testing=testing):
                    break
            if mode is keyboard_click:
                if key_press(int(self.txt_key_hex.get("1.0", 'end-1c'), 16),
                             self.clickmemory,
                             delay_before=delay_before,
                             delay_between=delay_between,
                             testing=testing):
                    break
            diff_before.add(delay_before)
            diff_between.add(delay_between)
            clickmemory.add_leftclick(delay_before, delay_between)
            frame.label.config(text=clickmemory.overview_text())
            frame.graph_update()
        print("Stopped")

    def infitineclick(self):
        self.running = True

        t = threading.Thread(target=self.worker)
        t.start()
        print("Started")

    def stop(self):
        self.running = False


class Frame:
    root = Tk()
    clicker = None
    datatype = None
    framesize = fs.Small
    graphDataType = gtd.Between

    data = []

    # Bar graph and its variables
    c_height = 350
    c = Canvas(root, width=650, height=c_height, bg='white')
    c.grid(row=0, column=5, rowspan=5)
    maxy = 999999
    y_stretch = 100     # The highest y = max_data_value * y_stretch
    y_gap = 0           # The gap between lower canvas edge and x axis
    x_stretch = 0       # Stretch x wide enough to fit the variables
    x_width = 1         # The width of the x-axis
    x_gap = 0           # The gap between left canvas edge and y axis

    def __init__(self):
        self.datatype = diff_between
        self.root.protocol('WM_DELETE_WINDOW', self.program_exit)
        self.root.geometry("355x340")
        self.root.resizable(width=True, height=True)

        self.btn_clicker_start = Button(self.root,
                                        text='Start',
                                        font=("Sans", 40),
                                        command=self.clicker_start)
        self.btn_clicker_start.grid(row=0,
                                    column=0,
                                    rowspan=2,
                                    columnspan=3,
                                    sticky="nesw",)

        self.btn_stop = Button(self.root,
                               text='Stop',
                               font=("Sans", 15),
                               command=self.clicker_stop)
        self.btn_stop.grid(row=2,
                           column=0,
                           columnspan=3,
                           sticky="nesw")

        self.label = Label(self.root,
                           height=9,
                           width=50,
                           background='black',
                           foreground='yellow',
                           text=clickmemory.overview_text())
        self.label.grid(row=4,
                        column=0,
                        columnspan=5,
                        sticky="nesw")

        self.btn_graph = Button(self.root,
                                text='Show Graph',
                                font=48,
                                command=self.graph_showhide)
        self.btn_graph.grid(row=0,
                            column=3,
                            columnspan=2,
                            sticky="nesw")

        self.btn_graphdatatype = Button(self.root,
                                        text='Between Time',
                                        font=("Sans", 12),
                                        width=13,
                                        command=self.graph_changedata)
        self.btn_graphdatatype.grid(row=1,
                                    column=3,
                                    columnspan=2,
                                    sticky="nesw")

        self.btn_test = Button(self.root,
                               text='Testing: False',
                               font=("Sans", 12),
                               command=self.test)
        self.btn_test.grid(row=2,
                           column=3,
                           columnspan=2,
                           sticky="nesw")

        self.txt_key_hex = Text(self.root,
                                width=5,
                                height=1)
        self.txt_key_hex.grid(row=3,
                              column=0)

        self.txt_key_hex_info = Text(self.root,
                                     width=7,
                                     font=1,
                                     height=1)
        self.txt_key_hex_info.grid(row=3,
                                   column=1)

        self.btn_click_mode = Button(self.root,
                                     text="Mode: Mouse Click",
                                     font=("Sans", 13),
                                     width=10,
                                     background="#29b6f6",
                                     command=self.mode_change)
        self.btn_click_mode.grid(row=3,
                                 column=2,
                                 columnspan=3,
                                 sticky="nesw")

        self.clicker = Clicker(clickmemory, self.txt_key_hex)
        self.txt_key_hex_info.insert(INSERT, "http://www.flint.jp/misc/?q=dik&lang=en")
        self.txt_key_hex_info.config(state="disabled")

    def clicker_start(self):
        if timer.running:
            timer.abort()
        if self.clicker.running:
            self.clicker.stop()
            return

        self.txt_key_hex.config(state="disabled")
        timer.set(self.label, DELAY_BEFORE_START, self.clicker.infitineclick)
        timer.run(self)

    def clicker_stop(self):
        timer.abort()
        self.clicker.stop()
        self.btn_clicker_start.config(state="active", text="Start")
        self.txt_key_hex.config(state="normal")

    def graph_update(self):
        if self.framesize == fs.Big:
            self.c.delete("all")
            if self.maxy < 0 and self.y_stretch > 1:
                self.maxy = 9999999
                self.y_stretch -= 1
            data = self.datatype.sorted_values()
            for x, d2 in enumerate(data):
                temp, y = d2                              # A Loop to calculate the rectangle coordinates of each bar
                x0 = x * self.x_stretch + x * self.x_width + self.x_gap                     # Bottom left coordinate
                y0 = self.c_height - (y * self.y_stretch + self.y_gap)                      # Top left coordinates
                x1 = x * self.x_stretch + x * self.x_width + self.x_width + self.x_gap      # Bottom right coordinates
                y1 = self.c_height - self.y_gap                                             # Top right coordinates
                try:
                    self.c.create_rectangle(x0, y0, x1, y1)                                 # Draw the bar
                    self.maxy = min(self.maxy, y0)
                except Exception as e:
                    print(e)

    def graph_showhide(self):
        if self.framesize == fs.Small:
            self.btn_graph["text"] = "Hide Graph"
            self.root.geometry("1010x340")
            self.framesize = fs.Big
            self.graph_update()
        else:
            self.btn_graph["text"] = "Show Graph"
            self.root.geometry("355x340")
            self.framesize = fs.Small

    def graph_changedata(self):
        if self.graphDataType == gtd.Between:
            self.datatype = diff_before
            self.btn_graphdatatype["text"] = "Before Time"
            self.graphDataType = gtd.Before
        else:
            self.datatype = diff_between
            self.btn_graphdatatype["text"] = "Between Time"
            self.graphDataType = gtd.Between
        self.graph_update()

    def test(self):
        global testing
        if testing:
            self.btn_test["text"] = "Testing: False"
            testing = False
        else:
            self.btn_test["text"] = "Testing: True"
            testing = True

    def mode_change(self):
        global mode
        if mode is mouse_click:
            self.btn_click_mode["text"] = "Mode: Keyboard"
            mode = keyboard_click
        else:
            self.btn_click_mode["text"] = "Mode: Mouse Click"
            mode = mouse_click

    def program_exit(self):
        self.clicker.stop()
        self.root.destroy()

    def run(self):
        self.root.wm_title(PROGRAM_TITLE)
        self.root.mainloop()


diff_before = Diffmemory(0.3, 1, (1 - 0.3) / 355)
diff_between = Diffmemory(0.070, 0.185, (0.185 - 0.07) / 355)
clickmemory = ClickMemory()
timer = Timer()
frame = Frame()


def run():
    frame.run()
