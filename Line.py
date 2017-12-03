#Author: Gautier Dagan

class Point(object):
    """Class for Point - coordinate."""
    def __init__(self, x, y):
        super(Point, self).__init__()
        if x > 640:
            self.x = 640 #these values are fixed based on the height and width of all our images
        else:
            self.x = x

        if y > 480:
            self.y = 480
        else:
            self.y = y

    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"


class Line(object):
    """class for Line."""
    def __init__(self, x0, y0, x1, y1):
        super(Line, self).__init__()
        self.point0 = Point(x0, y0)
        self.point1 = Point(x1, y1)

    def __str__(self):
        return "["+str(self.point0)+"-->"+str(self.point1)+"]"

    def get_coords(self):
        return self.point0.x, self.point0.y, self.point1.x, self.point1.y

    def get_coords_arr(self):
        return [int(self.point0.x), int(self.point0.y), self.point1.x, self.point1.y]
