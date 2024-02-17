import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image

# Load the image
image_path = 'FALAK2.png'
image = Image.open(image_path)
image = image.convert('RGB')

width, height = image.width, image.height

pixel_data = list(image.getdata())

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

rgb_data = [list(pixel) for pixel in pixel_data]
normalized_rgb_data = list(map( lambda rgb : [value/255 for value in rgb], rgb_data ))

r_data = list(map(lambda pixel : pixel[0], rgb_data))
g_data = list(map(lambda pixel : pixel[1], rgb_data))
b_data = list(map(lambda pixel : pixel[2], rgb_data))

# for i in range(height):
#     for j in range(width):
#         pixel = rgb_data[i]
#         x = pixel[0]
#         y = pixel[1]
#         z = pixel[2]

ax.scatter(r_data, g_data, b_data, color=normalized_rgb_data, s=2)

ax.set_xlabel('Red')
ax.set_ylabel('Green')
ax.set_zlabel('Blue')

ax.axes.set_xlim(0, 255)
ax.axes.set_ylim(0, 255)
ax.axes.set_zlim(0, 255)

ax.view_init(-140, 120)

fig.show()