
from matplotlib.pyplot import plot, show

class Plot(object):
    def __init__(self, data, field=None):
    	if field is not None:
        	self.data = data[field]
        else:
        	self.data = data

    def draw(self):
        plot(self.data)
        show()
