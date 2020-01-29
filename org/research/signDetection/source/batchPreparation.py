from keras.preprocessing.image import ImageDataGenerator
import numpy as np
import matplotlib.pyplot as plt

train_path = '../images/train/'
test_path = '../images/test/'
batch_size = 16
image_size = 224
num_class = 8

train_datagen = ImageDataGenerator(
    validation_split = 0.3,
    shear_range = 0.2,
    zoom_range = 0.2,
    horizontal_flip = True)

train_generator = train_datagen.flow_from_directory(
    directory = train_path,
    target_size = (image_size,image_size),
    batch_size = batch_size,
    class_mode = 'categorical',
    color_mode = 'rgb',
    shuffle = True)

x_batch, y_batch = train_generator.next()
