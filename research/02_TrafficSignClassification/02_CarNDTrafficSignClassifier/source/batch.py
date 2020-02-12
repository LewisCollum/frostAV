from keras.preprocessing.image import ImageDataGenerator
import numpy
import matplotlib.pyplot as pyplot
from textwrap import wrap

import common
import preprocessing

size = 32

batchGenerator = ImageDataGenerator(
    rescale = 1./255,
    preprocessing_function = preprocessing.execute,
    validation_split = 0.2)

trainIterator = batchGenerator.flow_from_directory(
    directory = common.trainPath,
    batch_size = size,
    shuffle = True,
    target_size = (common.imageSize, common.imageSize),
    color_mode = 'grayscale',
    subset = 'training')

validationIterator = batchGenerator.flow_from_directory(
    directory = common.trainPath,
    batch_size = size,
    shuffle = True,
    target_size = (common.imageSize, common.imageSize),
    color_mode = 'grayscale',
    subset = 'validation')

_images, _labels = trainIterator.next()
classCount = len(_labels[0])
sampleClasses = trainIterator.labels
sampleSize = trainIterator.n
imageShape = _images[0].shape

def classFromLabelsAt(labels, index):
    return numpy.where(labels[index] == 1)[0][0]

def signNameFromLabelsAt(labels, index):
    return common.signNames[classFromLabelsAt(labels, index)]

def plot(images, labels, titles=True, columns=5, rows=5):
    figure, axes = pyplot.subplots(rows, columns, figsize=(8,2*rows))
    figure.subplots_adjust(hspace = .6)

    for n in range(min(columns*rows, size)):
        if len(images[n, 0, 0]) == 1:
            figure.axes[n].imshow(images[n].reshape((32, 32)), cmap='gray')
        else:
            figure.axes[n].imshow(images[n])
        if titles:
            title = signNameFromLabelsAt(labels, n).title()
            wrappedTitle = "\n".join(wrap(title, 18))
            figure.axes[n].set_title(wrappedTitle, fontsize=10)

    for subplotAxes in figure.axes: subplotAxes.axis('off')
    figure.tight_layout()
