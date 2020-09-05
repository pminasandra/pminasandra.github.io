import matplotlib.pyplot as plt
from scipy.spatial import *
import numpy as np
import random

img1 = plt.imread("download.png")
img2 = plt.imread("download2.png")

a = [-10, -4, 5, 9, 12, 14]
b = [0, -7, 2, 7, -1, -4]

aa = []
for i in range(len(a)):
       aa.append((a[i], b[i])) 

ss = 0.9
fig, ax = plt.subplots()
for point in aa:
        ax.imshow(random.choice([img1, img2]), extent = [point[0]-ss, point[0]+ss, point[1]-ss, point[1]+ss])

vor = Voronoi(aa)
voronoi_plot_2d(vor, ax=ax, show_vertices=False, show_points=False, line_colors="darkgray")
plt.xlim(-11, 15)
plt.ylim(-8, 8)
plt.xticks([])
plt.yticks([])
plt.savefig('banner.png', bbox_inches='tight')

