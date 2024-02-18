import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
import settings

# Load the image
image_path = f'{settings.input_path}.jpg'
image = Image.open(image_path)
image = image.convert('RGB')

width, height = image.width, image.height

pixel_data = list(image.getdata())

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

rgb_data = [list(pixel) for pixel in pixel_data]
normalized_rgb = list(map( lambda rgb : [value/255 for value in rgb], rgb_data ))

r_data = list(map(lambda pixel : pixel[0], rgb_data))
g_data = list(map(lambda pixel : pixel[1], rgb_data))
b_data = list(map(lambda pixel : pixel[2], rgb_data))

r_range = max(r_data) - min(r_data)
g_range = max(g_data) - min(g_data)
b_range = max(b_data) - min(b_data)

r_1_data = []
g_1_data = []
b_1_data = []
normalized_rgb_1 = []

r_2_data = []
g_2_data = []
b_2_data = []
normalized_rgb_2 = []

r_3_data = []
g_3_data = []
b_3_data = []
normalized_rgb_3 = []

r_4_data = []
g_4_data = []
b_4_data = []
normalized_rgb_4 = []

# for index, g_value in enumerate(g_data):
#     if g_value < 128:
#         if r_data[index] < 128:
#             r_1_data.append(r_data[index])
#             g_1_data.append(g_data[index])
#             b_1_data.append(b_data[index])
#             normalized_rgb_1.append(list(map((lambda val : val / 255), rgb_data[index])))
#         else:
#             r_2_data.append(r_data[index])
#             g_2_data.append(g_data[index])
#             b_2_data.append(b_data[index])
#             normalized_rgb_2.append(list(map((lambda val : val / 255), rgb_data[index])))
#     else:
#         if r_data[index] < 128:
#             r_3_data.append(r_data[index])
#             g_3_data.append(g_data[index])
#             b_3_data.append(b_data[index])
#             normalized_rgb_3.append(list(map((lambda val : val / 255), rgb_data[index])))
#         else:
#             r_4_data.append(r_data[index])
#             g_4_data.append(g_data[index])
#             b_4_data.append(b_data[index])
#             normalized_rgb_4.append(list(map((lambda val : val / 255), rgb_data[index])))

print(f'Red Range: {r_range}, Green Range: {g_range}, Blue Range: {b_range}, ')

# for i in range(height):
#     for j in range(width):
#         pixel = rgb_data[i]
#         x = pixel[0]
#         y = pixel[1]
#         z = pixel[2]

xx1, zz1 = np.meshgrid(range(255), range(255))
yy1 = xx1*0 + 128

yy2, zz2 = np.meshgrid(range(255), range(255))
xx2 = xx1*0 + 128

def avg(list):
    if len(list) > 0:
        return round(sum(list) / len(list))
    else:
        return 0

print(f'''
Data 1 Avg. Color: {[avg(r_1_data), avg(g_1_data), avg(b_1_data)] }
Data 2 Avg. Color: {[avg(r_2_data), avg(g_2_data), avg(b_2_data)] }
Data 3 Avg. Color: {[avg(r_3_data), avg(g_3_data), avg(b_3_data)] }
Data 4 Avg. Color: {[avg(r_4_data), avg(g_4_data), avg(b_4_data)] }
''')

# ax.plot_surface(xx1,yy1,zz1, color=[0, 1, 0, 0.5], zorder=0)
# ax.plot_surface(xx2,yy2,zz2, color=[1, 0, 0, 0.5], zorder=0)

ax.scatter(r_data, g_data, b_data, color=normalized_rgb, s=2, zorder=99)


ax.set_xlabel('Red')
ax.set_ylabel('Green')
ax.set_zlabel('Blue')

ax.axes.set_xlim(0, 255)
ax.axes.set_ylim(0, 255)
ax.axes.set_zlim(0, 255)

ax.view_init(-140, 315)

plt.show()