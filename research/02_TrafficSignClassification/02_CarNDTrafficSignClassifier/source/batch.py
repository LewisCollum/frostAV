from keras.preprocessing.image import ImageDataGenerator

import common

size = 32

trainGenerator = ImageDataGenerator(rescale=1./255)
trainIterator = trainGenerator.flow_from_directory(
    directory = common.trainPath,
    batch_size = size,
    shuffle = True,
    target_size = (common.imageSize, common.imageSize))
