# This file contains examples on how to create plots according to 1 agreed standard. 


# scatter plot
import matplotlib.pyplot as plt
import random

# Random seed
random.seed(2022)

# data with added noise
datax = [i for i in range(6)]
datay = [(x**2+x*random.random()) for x in datax]

fig, ax = plt.subplots()
ax.scatter(datax, datay)
ax.set_xlabel('time [s]')
ax.set_ylabel('distance [m]')
#plt.savefig('<filename>.pdf', bbox_inches='tight')
plt.show()


# errorbar plot
import numpy as np
import matplotlib.pyplot as plt

# number of points
N = 20

fig, ax = plt.subplots()

# data with noise
x = np.arange(N)
y = 2.5 * np.sin(x / N /2 * np.pi)
yerr = np.random.rand(N)

# multiple plots can be added in the same axes (see next for multiple subplots)
ax.errorbar(x, y + 3, yerr=yerr, label='both limits (default)')

ax.errorbar(x, y + 2, yerr=yerr, uplims=True, label='uplims=True')

ax.errorbar(x, y + 1, yerr=yerr, uplims=True, lolims=True, label='uplims=True, lolims=True')
# legend is automatically placed in best spot
plt.legend()
#plt.savefig('<filename>.pdf', bbox_inches='tight')
plt.show()


# Subplots
from matplotlib.markers import MarkerStyle
import numpy as np
import matplotlib.pyplot as plt

# Fixing random state for reproducibility
np.random.seed(2022)

dt = 0.1
t = np.arange(0, 30, dt)
noise = np.random.randn(len(t))*10

# our prediction
model = t**2 + 10

# our measurement
signal = t**2 + 10 + noise

fig, axs = plt.subplots(2, 1)
axs[0].plot(t, signal, color='tab:red', linestyle='-', label='measurement')
axs[0].plot(t, model, color='tab:blue', linestyle='--', label='model')

axs[0].set_xlabel('time [ns]')
axs[0].set_ylabel('Model and measurement')
axs[0].grid(True)
axs[0].legend()

# you can see that signficance (or signal/noise) ratio drops
ratio = (signal-model)/model
axs[1].plot(t, ratio, linewidth=1)
axs[1].set_ylabel('Relative ratio')
plt.tight_layout()
#plt.savefig('<filename>.pdf', bbox_inches='tight')
plt.show()
