import ctypes
from time import sleep
from tkinter import Tk, Button, Label, Canvas
import datetime
from Memory import *
from RandomDelayPicker import *
from Constants import *
from Enum import *
import threading

SetCursorPos = ctypes.windll.user32.SetCursorPos
mouse_event = ctypes.windll.user32.mouse_event
testing = False
clicking = False


class Timer:
    label = None
    time = None
    func = None
    aborted = False
    running = False

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
                self.running = False
                return True
        self.running = False
        self.func()

    def run(self):
        if self.running:
            return
        t = threading.Thread(target=self.time_worker)
        t.start()
        self.running = True

    def abort(self):
        self.aborted = True


class LeftClicker:
    isLeftDown = False
    isLeftUp = False
    inUse = False

    def __init__(self):
        self.isLeftDown = False
        self.isLeftUp = True

    def left_click(self, x=-1, y=-1, clicks=1, delay_before=0, delay_between=0):
        global downtime
        if self.inUse:
            return True

        if testing:
            return False

        self.inUse = True
        if x != 1 and y != -1:
            SetCursorPos(x, y)

        for i in range(clicks):
            if self.isLeftUp:
                sleep(delay_before)
                downtime = datetime.datetime.now().time()

                mouse_event(2, 0, 0, 0, 0)
                self.isLeftUp = False
                self.isLeftDown = True

            if self.isLeftDown:
                sleep(delay_between)

                print("Click:", clickmemory.totalClick + 1,
                      "\t", downtime, " - ", datetime.datetime.now().time(),
                      "\t waited/Lasted", delay_before, " - ", delay_between)
                mouse_event(4, 0, 0, 0, 0)
                self.isLeftUp = True
                self.isLeftDown = False
        self.inUse = False


class Clicker:
    running = False
    LClicker = LeftClicker()

    def __init__(self):
        self.LClicker = LeftClicker()

    def worker(self):
        delay_before = 0
        delay_between = 0
        while self.running:
            delay_before = rand_delay_before(delay_before)
            delay_between = rand_delay_between(delay_between)
            if clickmemory.totalClick > 100000:
                break
            if self.LClicker.left_click(delay_before=delay_before, delay_between=delay_between):
                break
            diff_before.add(delay_before)
            diff_between.add(delay_between)
            clickmemory.add_leftclick(delay_before, delay_between)
            frame.label.config(text=clickmemory.overview_text())
            frame.graph_update()
        print("Paused")

    def infitineclick(self):
        self.running = True
        print("Started")

        t = threading.Thread(target=self.worker)
        t.start()

    def stop(self):
        self.running = False


class Frame:
    root = Tk()
    clicker = Clicker()
    datatype = None
    framesize = fs.Small
    graphDataType = gtd.Between
    testing = False

    data = []

    # Bar graph and its variables
    c_height = 350
    c = Canvas(root, width=650, height=c_height, bg='white')
    c.grid(row=0, column=2, rowspan=4)
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
        self.root.resizable(width=False, height=False)

        self.btn_startClicker = Button(self.root,
                                       text='Start',
                                       height=3,
                                       width=20,
                                       font=48,
                                       command=self.clicker_start)
        self.btn_startClicker.grid(row=0, column=0, rowspan=2)

        self.btn_stop = Button(self.root,
                               text='Stop',
                               height=3,
                               width=20,
                               font=48,
                               command=self.clicker_stop)
        self.btn_stop.grid(row=2, column=0)

        self.label = Label(self.root,
                           height=9,
                           width=50,
                           background='black',
                           foreground='yellow',
                           text=clickmemory.overview_text())
        self.label.grid(row=3,
                        column=0,
                        columnspan=2)

        self.btn_graph = Button(self.root,
                                text='Show Graph',
                                width=12, font=48,
                                command=self.graph_showhide)
        self.btn_graph.grid(row=0,
                            column=1)

        self.btn_graphdatatype = Button(self.root,
                                        text='Between Time',
                                        width=12,
                                        font=48,
                                        command=self.graph_changedata)
        self.btn_graphdatatype.grid(row=1,
                                    column=1)

        self.btn_test = Button(self.root,
                               text='Normal',
                               width=12,
                               font=48,
                               command=self.test)
        self.btn_test.grid(row=2,
                           column=1)

    def clicker_start(self):
        timer.set(self.label, DELAY_BEFORE_START, self.clicker.infitineclick)
        timer.run()
        self.btn_startClicker.config(state="disabled")

    def clicker_stop(self):
        timer.abort()
        self.clicker.stop()
        self.btn_startClicker.config(state="active")

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
            self.btn_test["text"] = "Normal"
            testing = False
        else:
            self.btn_test["text"] = "Testing"
            testing = True

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
