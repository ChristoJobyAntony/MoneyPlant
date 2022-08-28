import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import os
import cv2 as cv

new_model = tf.keras.models.load_model('weights.h5')
new_model.summary()
