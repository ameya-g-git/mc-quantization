import matplotlib.pyplot as plt
import numpy as np
from time import time
import csv
from skimage.io import imread, imsave
import settings

input_path = settings.input_path    
sample_img = imread(f'{input_path}.png')
trials = settings.trials

def median_cut_quantize(img, img_arr):
    # when it reaches the end, color quantize
    print("to quantize: ", len(img_arr))
    r_average = np.mean(img_arr[:,0])
    g_average = np.mean(img_arr[:,1])
    b_average = np.mean(img_arr[:,2])
    
    for data in img_arr:
        sample_img[data[3]][data[4]] = [r_average, g_average, b_average, 255]
    
def split_into_buckets(img, img_arr, depth):
    if len(img_arr) == 0:
        return
        
    if depth == 0:
        median_cut_quantize(img, img_arr)
        return
    
    r_range = np.max(img_arr[:,0]) - np.min(img_arr[:,0])
    g_range = np.max(img_arr[:,1]) - np.min(img_arr[:,1])
    b_range = np.max(img_arr[:,2]) - np.min(img_arr[:,2])
    
    space_with_highest_range = 0

    if g_range >= r_range and g_range >= b_range:
        space_with_highest_range = 1
    elif b_range >= r_range and b_range >= g_range:
        space_with_highest_range = 2
    elif r_range >= b_range and r_range >= g_range:
        space_with_highest_range = 0

    print("space_with_highest_range:",space_with_highest_range)

    # sort the image pixels by color space with highest range 
    # and find the median and divide the array.
    img_arr = img_arr[img_arr[:,space_with_highest_range].argsort()]
    median_index = int((len(img_arr)+1)/2)
    print("median_index:", median_index)

    
    #split the array into two buckets along the median
    split_into_buckets(img, img_arr[0:median_index], depth-1)
    split_into_buckets(img, img_arr[median_index:], depth-1)
    
flattened_img_array = []
for rindex, rows in enumerate(sample_img):
    for cindex, color in enumerate(rows):
        flattened_img_array.append([color[0],color[1],color[2],rindex, cindex]) 
        
flattened_img_array = np.array(flattened_img_array)

# open csv file to begin file tracking

with open(settings.csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Palette Size (expressed as 2^n)'] + [f'Time Taken {x + 1}' for x in range(trials)] + ['Mean SSIM Index'])  # Write header
    for n in range(1,settings.iterations + 1):
        output_path = f'{settings.output_path}_{n}.png'

        time_results = []

        for i in range(trials):
            start = time()
            split_into_buckets(sample_img, flattened_img_array, n)
            end = time()

            time_taken = end - start
            time_results.append(time_taken)

        # TODO: add MSE data collection? maybe? we'll see

        writer.writerow([n] + time_results + [0])

        imsave(output_path, sample_img)
        print(f"Image compressed with {2**n} colors. Time taken: {time_taken} seconds. Saved as {output_path}")
# the 3rd parameter represents how many colors are needed in the power of 2. If the parameter 
# passed is 4 its means 2^4 = 16 colors

