from keras.preprocessing.image import ImageDataGenerator
import numpy as np
import common

size = 16

trainingBatchGenerator = ImageDataGenerator(
    validation_split = 0.3,
    shear_range = 0.2,
    zoom_range = 0.2,
    horizontal_flip = True)

trainingBatchIterator = trainingBatchGenerator.flow_from_directory(
    directory = common.trainPath,
    target_size = (common.imageSize, common.imageSize),
    batch_size = size,
    class_mode = 'categorical',
    color_mode = 'rgb',
    shuffle = True)

x, y = trainingBatchIterator.next()
sampleSize = trainingBatchIterator.n
