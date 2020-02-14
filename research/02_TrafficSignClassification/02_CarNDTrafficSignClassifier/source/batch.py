from keras.preprocessing.image import ImageDataGenerator
import numpy
import matplotlib.pyplot as pyplot
from textwrap import wrap
import pandas

import preprocessing
import path

signNames = pandas.read_csv(path.data.names)['SignName'].values
imageSize = 32
size = 32

batchGenerator = ImageDataGenerator(
    rescale = 1.0/255,
    preprocessing_function = preprocessing.execute,
    validation_split = 0.2)

trainIterator = batchGenerator.flow_from_directory(
    directory = path.data.train,
    batch_size = size,
    shuffle = True,
    target_size = (imageSize, imageSize),
    color_mode = 'grayscale',
    subset = 'training')

validationIterator = batchGenerator.flow_from_directory(
    directory = path.data.train,
    batch_size = size,
    shuffle = True,
    target_size = (imageSize, imageSize),
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
    return signNames[classFromLabelsAt(labels, index)]

def plot(images, labels, columns=5, rows=5):
    figure, axes = pyplot.subplots(rows, columns, figsize=(8,2*rows))
    figure.subplots_adjust(hspace = .6)

    for n in range(min(columns*rows, len(images))):
        if len(images[n, 0, 0]) == 1:
            figure.axes[n].imshow(images[n].reshape((imageSize, imageSize)), cmap='gray')
        else:
            figure.axes[n].imshow(images[n])

        title = signNameFromLabelsAt(labels, n).title()
        wrappedTitle = "\n".join(wrap(title, 18))
        figure.axes[n].set_title(wrappedTitle, fontsize=10)

    for subplotAxes in figure.axes: subplotAxes.axis('off')
    figure.tight_layout()
