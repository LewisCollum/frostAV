from keras.preprocessing.image import ImageDataGenerator

import common

size = 32

batchGenerator = ImageDataGenerator(rescale=1./255)
batch = batchGenerator.flow_from_directory(
    directory = common.trainPath,
    batch_size = size,
    shuffle = True,
    target_size = (common.imageSize, common.imageSize))
