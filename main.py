from tkinter import *
from DrawingArea import DrawingArea

class MainWindow(Frame):
    def __init__(self, main):

        # set frame to listen to keys.
        Frame.__init__(self, main)
        # make sure we can use self.main.destroy()
        self.main = main

        #Drawing Area
        self.drawing_area = DrawingArea(root)
        self.main.bind('<Left>', self.drawing_area.prev_image)
        self.main.bind('<Right>', self.drawing_area.next_image)


if __name__ == "__main__":

    root = Tk()
    MainWindow(root)
    root.geometry("1000x500")
    root.mainloop()
