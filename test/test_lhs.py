import numpy as np
import matplotlib.pyplot as plt
from smt.sampling_methods import LHS
import math

xlimits = np.array([[2, 5], 
                    [1, 1.5],
                    [2, 5],
                    [3, 6],
                    [0.1, 0.2,],
                    [math.pi/6, math.pi/4],
                    [1, 100]])
sampling = LHS(xlimits=xlimits)

num = 50
x = sampling(num)

print(x.shape)