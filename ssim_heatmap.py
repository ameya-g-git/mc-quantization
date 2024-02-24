import cv2
import csv
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import settings

from skimage import metrics

# load uncompressed image
image1 = cv2.imread(f'{settings.input_path}.png')
image1_plot = np.asarray(Image.open(f'{settings.input_path}.png')) 

# separate image into its RGB channels
image1_b = np.array(image1[:,:,0]) 
image1_g = np.array(image1[:,:,1])
image1_r = np.array(image1[:,:,2])

# create matplotlib figure with subplots to organize heatmaps
fig, axs = plt.subplots(3, 3, figsize=(8, 6))
img_num = 1 # holds the index of the current subplot

with open(settings.csv_file, mode='r', newline='') as file:
    reader = csv.reader(file)
    data = list(reader)

ssim_col_index = settings.iterations # the index of the SSIM Index column in the csv file

ssim_indices = [] # will hold the mean SSIM indices of each comparison

for y in range(3):
    for x in range(3):
        ax = axs[y, x] # set ax to be the current subplot to work on
        
        if x == 0 and y == 0:
            ax.imshow(image1_plot)
            continue

        output_path = f'{settings.output_path}_{img_num}.png' # open compressed image based on syntax specified from settings

        if img_num > settings.iterations: # break loop at 9th subplot as it is not needed
            break

        # load second image
        image2 = cv2.imread(output_path) 
        print(output_path)

        # separate second image into RGB channels
        image2_b = np.array(image2[:,:,0])
        image2_g = np.array(image2[:,:,1])
        image2_r = np.array(image2[:,:,2])

        # size of sliding window for SSIM heatmap generation
        error_size = 11

        # generate SSIM numpy arrays for each channel
        ssim_index_b, grad_b, S_b = metrics.structural_similarity(image1_b, image2_b, win_size=error_size, full=True, gradient=True)
        ssim_index_g, grad_g, S_g = metrics.structural_similarity(image1_b, image2_b, win_size=error_size, full=True, gradient=True)
        ssim_index_r, grad_r, S_r = metrics.structural_similarity(image1_b, image2_b, win_size=error_size, full=True, gradient=True)


        # average the data between each channel
        avg_S = (S_b + S_g + S_r) / 3 
        avg_ssim_index = (ssim_index_b + ssim_index_g + ssim_index_r) / 3 

        # push average SSIM index to list
        ssim_indices.append(avg_ssim_index)

        # create heatmap with colorbar set to a range of [0, 1]
        heatmap = ax.imshow(avg_S, cmap='Spectral')
        ax.set_title(f'{img_num} Iterations')
        plt.colorbar(heatmap, label="SSIM Index")
        heatmap.set_clim(0, 1)

        img_num += 1

# change data in SSIM Index column from csv row-by-row
for i, row in enumerate(data):
    if i == 0:
        continue
    row[ssim_col_index] = ssim_indices[i - 1]

# write data
with open(settings.csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

# format plot
fig.suptitle(' ')
plt.tight_layout()
plt.subplots_adjust(wspace=0.1, hspace=0.25)
plt.show()

# TODO: create implentation of this but for other channels, like contrast