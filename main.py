from tkinter import *
from PIL import ImageTk, Image
import os

class MainWindow(Frame):
    def __init__(self, main):
        self.current = None
        self.image_ind = 0
        self.image_path = 'imgs/image0.jpg'
        self.max_image_ind = 5

        # set frame to listen to keys.
        Frame.__init__(self, main)
        # make sure we can use self.main.destroy()
        self.main = main

        #Buttons:
        self.right_button = Button(root, text="<- Previous Picture", command=self.prev_button)
        self.right_button.pack(side=LEFT)
        self.left_button = Button(root, text="Next Picture ->", command=self.next_button)
        self.left_button.pack(side=RIGHT)

        #Image Label
        self.image_path_label = Label(root, text=self.image_path, fg="black")
        self.image_path_label.pack(side=TOP)

        #Drawing:
        self.drawing_area = Canvas(root, width=640, height=480, bg='white')
        self.drawing_area.pack()
        # Load the image file
        im = Image.open(self.image_path)
        im = im.resize((640, 480))

        # Put the image into a canvas compatible class, and stick in an
        self.drawing_area.image = ImageTk.PhotoImage(im)
        # Add the image to the canvas, and set the anchor to the top left / north west corner
        self.drawing_area.create_image(0, 0, image=self.drawing_area.image, anchor='nw')

        self.drawing_area.bind("<Escape>", self.reset)
        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.Mousedown)



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
            # the new line starts at the end of the previously
            # drawn line
            coords = event.widget.coords(self.current)
            x0 = coords[2]
            y0 = coords[3]

            #Draw the final line
            event.widget.create_line(x0, y0, event.x, event.y)
            self.current = None

    def motion(self, event):
        if self.current:
            # modify the current line by changing the end coordinates
            # to be the current mouse position
            coords = event.widget.coords(self.current)
            coords[2] = event.x
            coords[3] = event.y

            event.widget.coords(self.current, *coords)

    def prev_button(self):
        if self.image_ind > 0:
            self.image_ind -= 1
        print(self.image_ind)
        self.update_image(self.image_ind)

    def next_button(self):
        if self.image_ind < self.max_image_ind:
            self.image_ind += 1
        print(self.image_ind)
        self.update_image(self.image_ind)

    def update_image(self, image_ind):
        self.image_path = 'imgs/image'+str(image_ind)+'.jpg'
        self.image_path_label.config(text=self.image_path)

        if os.path.exists(self.image_path):
            im = Image.open(self.image_path)
            im = im.resize((640, 480))
            self.drawing_area.image = ImageTk.PhotoImage(im)
            self.drawing_area.create_image(0, 0, image=self.drawing_area.image, anchor='nw')
        else:
            print ("No image at this index")
            self.prev_button()



if __name__ == "__main__":

    root = Tk()
    MainWindow(root)
    root.geometry("1000x500")
    root.mainloop()
