# code reference : https://medium.com/datadriveninvestor/using-the-super-resolution-convolutional-neural-network-for-image-restoration-ff1e8420d846

import sys
import os
import cv2

# prepare degraded image by introducing quality distortions via resizing

FACTOR = 2

def prepare_images(path, FACTOR):

    # loop through the file in the directory
    for file in os.listdir(path):

        # open the file
        img = cv2.imread(path + '/' + file)

        # find old and new image dimension
        h, w, _ = img.shape
        new_height = h // FACTOR
        new_width = w // FACTOR

        # resize the image - down
        img = cv2.resize(img, (new_width, new_height), interpolation = cv2.INTER_LINEAR)

        # resize the image - up
        img = cv2.resize(img, (w, h), interpolation = cv2.INTER_LINEAR)

        # save the image
        print("Saving {}".format(file))
        cv2.imwrite("dataset/0.5-resize-enlarged/{}".format(file), img)


def resize_images(path, FACTOR):

    # loop through the file in the directory
    for file in os.listdir(path):

        # open the file
        img = cv2.imread(path + '/' + file)

        # find old and new image dimension
        h, w, _ = img.shape
        new_height = h // FACTOR
        new_width = w // FACTOR

        # resize the image - down
        img = cv2.resize(img, (new_width, new_height), interpolation = cv2.INTER_LINEAR)

        # save the image
        print("Saving {}".format(file))
        cv2.imwrite("dataset/0.5-resize/{}".format(file), img)


if __name__ == "__main__":

    prepare_images('dataset/original/', FACTOR)
    print("Resize images to factor " + str(FACTOR) + " and enlarged Done!")

    resize_images('dataset/original/', FACTOR)
    print("Resize images to factor " + str(FACTOR) + ", Done!")

