from keras.preprocessing.image import ImageDataGenerator
import numpy

import common

size = 32

batchGenerator = ImageDataGenerator(rescale=1./255)
batch = batchGenerator.flow_from_directory(
    directory = common.trainPath,
    batch_size = size,
    shuffle = True,
    target_size = (common.imageSize, common.imageSize))

images, labels = batch.next()

classCount = len(labels[0])

def classAt(index):
    return numpy.where(labels[index] == 1)[0][0]

sampleClasses = batch.labels
sampleSize = batch.n
