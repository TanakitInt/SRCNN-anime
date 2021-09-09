# ---- tensorflow test ----

import tensorflow as tf

tf.test.is_built_with_cuda()

tf.test.is_gpu_available(cuda_only=False, min_cuda_compute_capability=None)

print("Num GPUs Available :", len(tf.config.list_physical_devices('GPU')))
print("Tensorflow version :", tf.__version__)

# ---- Nvidia GPU Test ----

import GPUtil

GPUtil.getGPUs()
GPUtil.showUtilization(all=True)

# ---- package version test ----

import sys
import keras
import cv2
import numpy
import matplotlib
import skimage
import h5py
#import pydotplus

print("GPUtil : " + GPUtil.__version__)
print("Python : " + sys.version)
print("Keras : " + keras.__version__)
print("OpenCV : " + cv2.__version__)
print("NumPy : " + numpy.__version__)
print("Matplotlib : " + matplotlib.__version__)
print("Skimage : " + skimage.__version__)
print("h5py : " + h5py.__version__)
#print("pydotplus : " + pydotplus.__version__)

