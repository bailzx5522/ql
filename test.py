
import pandas as pd
import numpy as np
from pandas.io.data import DataReader

from matplotlib.pyplot import plot, show


df = DataReader("AAPL", "yahoo")
x = df['Adj Close']
plot(x)
show()
