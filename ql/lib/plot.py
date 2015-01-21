
from matplotlib.pyplot import plot, show

class Plot(object):
    def __init__(self, data, field=None):
        self.data = data

    def draw(self):
        plot(self.data)
        show()
