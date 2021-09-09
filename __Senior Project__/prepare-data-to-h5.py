# Code References  :
# https://github.com/MarkPrecursor/SRCNN-keras
# https://github.com/rezaeiii/SRCNN

import os
import cv2
import h5py
import numpy

# set dataset path
DATA_PATH = "dataset/original-sharpened/"
TEST_PATH = "dataset/test-sharpened/"

Random_Crop = 100
Patch_size = 32
label_size = 32
conv_side = 0
scale = 2

def prepare_data(_path):
    names = os.listdir(_path)
    names = sorted(names)
    nums = names.__len__()

    data = numpy.zeros((nums * Random_Crop, 1, Patch_size, Patch_size), dtype=numpy.double)
    label = numpy.zeros((nums * Random_Crop, 1, label_size, label_size), dtype=numpy.double)

    for i in range(nums):
        name = _path + names[i]
        hr_img = cv2.imread(name, cv2.IMREAD_COLOR)
        shape = hr_img.shape

        hr_img = cv2.cvtColor(hr_img, cv2.COLOR_BGR2YCrCb)
        hr_img = hr_img[:, :, 0]

        # two resize operation to produce training data and labels
        lr_img = cv2.resize(hr_img, (int(shape[1] / scale), int(shape[0] / scale)))
        lr_img = cv2.resize(lr_img, (shape[1], shape[0]))

        # produce Random_Crop random coordinate to crop training img
        Points_x = numpy.random.randint(0, min(shape[0], shape[1]) - Patch_size, Random_Crop)
        Points_y = numpy.random.randint(0, min(shape[0], shape[1]) - Patch_size, Random_Crop)

        for j in range(Random_Crop):
            lr_patch = lr_img[Points_x[j]: Points_x[j] + Patch_size, Points_y[j]: Points_y[j] + Patch_size]
            hr_patch = hr_img[Points_x[j]: Points_x[j] + Patch_size, Points_y[j]: Points_y[j] + Patch_size]

            lr_patch = lr_patch.astype(float) / 255.
            hr_patch = hr_patch.astype(float) / 255.

            data[i * Random_Crop + j, 0, :, :] = lr_patch
            label[i * Random_Crop + j, 0, :, :] = hr_patch

            #for showing data
            # cv2.imshow("lr", lr_patch)
            # cv2.imshow("hr", hr_patch)
            # cv2.waitKey(0)
            
    return data, label

BLOCK_STEP = 16
BLOCK_SIZE = 32

def prepare_crop_data(_path):
    names = os.listdir(_path)
    names = sorted(names)
    nums = names.__len__()

    data = []
    label = []

    for i in range(nums):
        name = _path + names[i]
        hr_img = cv2.imread(name, cv2.IMREAD_COLOR)
        hr_img.astype(float)
        hr_img = cv2.cvtColor(hr_img, cv2.COLOR_BGR2YCrCb)
        hr_img = hr_img[:, :, 0]
        shape = hr_img.shape
        h, w = hr_img.shape
        new_height = h / scale
        new_width = w / scale

        # two resize operation to produce training data and labels
        lr_img = cv2.resize(hr_img, (int(new_width), int(new_height)))
        lr_img = cv2.resize(lr_img, (w, h))
        width_num = (shape[0] - (BLOCK_SIZE - BLOCK_STEP) * 2) / BLOCK_STEP
        height_num = (shape[1] - (BLOCK_SIZE - BLOCK_STEP) * 2) / BLOCK_STEP
        for k in range(int(width_num)):
            for j in range(int(height_num)):
                x = k * BLOCK_STEP
                y = j * BLOCK_STEP
                hr_patch = hr_img[x: x + BLOCK_SIZE, y: y + BLOCK_SIZE]
                lr_patch = lr_img[x: x + BLOCK_SIZE, y: y + BLOCK_SIZE]

                lr_patch = lr_patch.astype(float) / 255.
                hr_patch = hr_patch.astype(float) / 255.

                lr = numpy.zeros((1, Patch_size, Patch_size), dtype=numpy.double)
                hr = numpy.zeros((1, label_size, label_size), dtype=numpy.double)

                lr[0, :, :] = lr_patch
                hr[0, :, :] = hr_patch

                data.append(lr)
                label.append(hr)
    
                #for showing data
                # cv2.imshow("lr", lr_patch)
                # cv2.imshow("hr", hr_patch)
                # cv2.waitKey(0)

    data = numpy.array(data, dtype=float)
    label = numpy.array(label, dtype=float)
    return data, label


def write_hdf5(data, labels, output_filename):
    # write data and label into h5 file 

    x = data.astype(numpy.float32)
    y = labels.astype(numpy.float32)

    with h5py.File(output_filename, 'w') as h:
        h.create_dataset('data', data=x, shape=x.shape)
        h.create_dataset('label', data=y, shape=y.shape)
        # h.create_dataset()


def read_training_data(file):

    with h5py.File(file, 'r') as hf:
        data = numpy.array(hf.get('data'))
        label = numpy.array(hf.get('label'))
        train_data = numpy.transpose(data, (0, 2, 3, 1))
        train_label = numpy.transpose(label, (0, 2, 3, 1))
        return train_data, train_label


if __name__ == "__main__":

    data, label = prepare_crop_data(DATA_PATH)
    write_hdf5(data, label, "h5-dataset/train.h5")
    data, label = prepare_data(TEST_PATH)
    write_hdf5(data, label, "h5-dataset/test.h5")
    print("Done!")

