from tkinter import *
from PIL import ImageTk, Image
from Line import Line, Point
import pickle
import copy
import os

class DrawingArea(object):
    """docstring for DrawingArea."""
    def __init__(self, root, image_ind=0, max_image_ind=5, lines={}):
        super(DrawingArea, self).__init__()
        self.current = None
        self.image_ind = image_ind
        self.max_image_ind = 5

        self.lines = lines #list of lines
        self.line_buffer = {}

        #Image Label
        self.image_path_label = Label(root, text="image_path", fg="black")
        self.image_path_label.pack(side=TOP)

        #Buttons:
        self.left_button = Button(root, text="<- Previous Picture", command=self.prev_image)
        self.left_button.pack(side=LEFT)
        self.right_button = Button(root, text="Next Picture ->", command=self.next_image)
        self.right_button.pack(side=RIGHT)

        #Undo Last Line Removed
        self.undo_remove = Button(root, text="Undo Remove Line", command=self.undo_remove_line)
        self.undo_remove.pack(side=BOTTOM)

        #Remove Last Line Added Button
        self.remove_last = Button(root, text="Remove Last Line Added", command=self.remove_last_line)
        self.remove_last.pack(side=BOTTOM)

        #Drawing:
        self.canvas = Canvas(root, width=640, height=480, bg='white')

        self.canvas.pack()
        self.load_image()
        self.bind_controls()

    def load_image(self, image_ind=None):
        if image_ind is None:
            image_ind = self.image_ind

        image_path = 'imgs/image'+str(image_ind)+'.jpg'
        self.image_path_label.config(text=image_path)

        if os.path.exists(image_path):
            # Load the image file
            im = Image.open(image_path)
            im = im.resize((640, 480))

            # Put the image into a canvas compatible class, and stick in an
            self.canvas.image = ImageTk.PhotoImage(im)

            # Add the image to the canvas, and set the anchor to the top left / north west corner
            self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

            self.load_lines()
            self.draw_lines()

        else:
            print ("No image at this index")
            self.prev_image()

    def bind_controls(self):
        self.canvas.bind("<Escape>", self.reset)
        self.canvas.bind("<Motion>", self.motion)
        self.canvas.bind("<ButtonPress-1>", self.Mousedown)
        self.canvas.bind("<Delete>", self.remove_last_line)

    def reset(self, event):
        self.current = None

    def Mousedown(self, event):
        event.widget.focus_set()  # so escape key will work
        if self.current is None:
            # the new line starts where the user clicked
            x0 = event.x
            y0 = event.y

            # Start the new line:
            self.current = event.widget.create_line(x0, y0, event.x, event.y)

        else:
            coords = event.widget.coords(self.current)
            x0 = coords[0]
            y0 = coords[1]

            #Draw the final line
            event.widget.create_line(x0, y0, event.x, event.y)

            self.lines[self.image_ind].append(Line(x0, y0, event.x, event.y))
            print ("Creating line: {0}, {1}, {2}, {3}".format(x0, y0, event.x, event.y))
            self.print_lines()
            self.current = None

    def motion(self, event):
        if self.current:
            # modify the current line by changing the end coordinates
            # to be the current mouse position
            coords = event.widget.coords(self.current)
            coords[2] = event.x
            coords[3] = event.y

            event.widget.coords(self.current, *coords)

    def next_image(self, event=None):
        self.save_lines()
        if self.image_ind < self.max_image_ind:
            self.image_ind += 1
        self.load_image()

    def prev_image(self, event=None):
        self.save_lines()
        if self.image_ind > 0:
            self.image_ind -= 1
        self.load_image()

    def print_lines(self):
        print("For image: {0}".format(self.image_ind))
        for l in self.lines[self.image_ind]:
            print(l)
        print("\n")

    def draw_lines(self):
        print("Drawing Lines Saved")
        if self.image_ind in self.lines.keys():
            for l in self.lines[self.image_ind]:
                self.canvas.create_line(l.get_coords(), fill="red")
        else:
            self.lines[self.image_ind] = []

        if self.image_ind not in self.line_buffer.keys():
            self.line_buffer[self.image_ind] = []

    def save_lines(self, line_filename="lines"):
        print("Saving Lines")
        with open('labels/'+ line_filename +'.pkl', 'wb') as f:
            pickle.dump(self.lines, f, pickle.HIGHEST_PROTOCOL)

    def load_lines(self, line_filename="lines"):
        print("Loading Lines")
        line_path = 'labels/' + line_filename + '.pkl'
        if os.path.exists(line_path):
            with open(line_path, 'rb') as f:
                self.lines = pickle.load(f)

    def remove_last_line(self, event=None):
        print("Removing Last Line")
        if len(self.lines[self.image_ind]) > 0:
            last_line = self.lines[self.image_ind].pop()
            self.line_buffer[self.image_ind].append(last_line)
            self.save_lines()
            self.load_image()

    def undo_remove_line(self, event=None):
        if len(self.line_buffer[self.image_ind]) > 0:
            new_line = self.line_buffer[self.image_ind].pop()
            self.lines[self.image_ind].append(new_line)
            self.save_lines()
            self.load_image()
