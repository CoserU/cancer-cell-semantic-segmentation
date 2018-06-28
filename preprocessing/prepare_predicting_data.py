# Credit to Wei Cao

import os
import argparse

import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imsave


def search_LR(img, threshold, is_plot=False):
    center_y = int(img.shape[0]/2)
    center_line = img[center_y]
    mean_RGB = center_line.mean(axis=1)
    length = len(mean_RGB)

    indices = np.argwhere(mean_RGB > threshold)
    idx1, idx2 = indices[0][0], indices[-1][0]
    left = mean_RGB[idx1:idx1+1000].argmin()+idx1
    right = mean_RGB[idx2-1000:idx2].argmin()+idx2-1000

    return left, right


def tif_cut(img, left, right):
    cut_idx = np.arange(left, right, 1)
    img_v = np.take(img, cut_idx, axis=1)
    return img_v[:3200]


def photo_cut(img, name, folder, threshold=35, cut_size=320):
    left, right = search_LR(img, threshold, is_plot=False)
    center = (left+right)//2
    width = 3520
    left, right = center-width//2, center+width//2

    img = tif_cut(img, left, right)
    imsave(folder+'{}_ORIG.tif'.format(name[:-4]), img)


parser = argparse.ArgumentParser(description='Cut old photos -> 3200 * 3520')
parser.add_argument('--name', '-n', default=None, type=str, help='Plot the old photo and check the boundries (left and right)')
parser.add_argument('--left', '-l', default=None, type=int, help='The position of the left boundry (int)')
parser.add_argument('--right', '-r', default=None, type=int, help='The position of the left boundry (int)')
args = parser.parse_args()

name = args.name
left = args.left
right = args.right

old_dir = 'F:/old/'
new_dir = 'F:/photo_cut/'

if name is None:
    threshold = 35
    # threshold = 80 

    old_files = [file for file in os.listdir(old_dir) if file.endswith('.tif')]
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)

    for old_file in old_files:
        img = plt.imread(old_dir+old_file)
        photo_cut(img, old_file, new_dir, threshold=threshold)
        print('{} completed!'.format(old_file))

else:
    img = plt.imread(old_dir+name)
    if (left is None and right is None):
        plt.imshow(img)
        plt.show()
    else:
        center = (left+right)//2
        width = 3520
        left, right = center-width//2, center+width//2
        img = tif_cut(img, left, right)
        imsave(new_dir+'{}_ORIG.tif'.format(name[:-4]), img)
        print('{} updated!'.format(name))
