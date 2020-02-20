from keras.preprocessing.image import ImageDataGenerator
import numpy
import matplotlib.pyplot as pyplot
from textwrap import wrap
import pandas

import path

names = pandas.read_csv(path.data.names)
titles = names['title'].values

imageSize = (800, 1360)
size = 32

batchGenerator = ImageDataGenerator(
    rescale = 1.0/255,
    validation_split = 0.2)

trainIterator = batchGenerator.flow_from_directory(
    directory = path.data.train,
    batch_size = size,
    shuffle = True,
    target_size = imageSize,
    subset = 'training')

validationIterator = batchGenerator.flow_from_directory(
    directory = path.data.train,
    batch_size = size,
    shuffle = True,
    target_size = imageSize,
    subset = 'validation')

_images, _labels = trainIterator.next()
classCount = len(_labels[0])
sampleClasses = trainIterator.labels
sampleSize = trainIterator.n
imageShape = _images[0].shape

def classFromLabelsAt(labels, index):
    return numpy.where(labels[index] == 1)[0][0]

def nameFromLabelsAt(labels, index):
    return titles[classFromLabelsAt(labels, index)]

def plot(images, labels, columns=5, rows=5):
    figure, axes = pyplot.subplots(rows, columns, figsize=(8,2*rows))
    figure.subplots_adjust(hspace = .6)

    for n in range(min(columns*rows, len(images))):
        if len(images[n, 0, 0]) == 1:
            figure.axes[n].imshow(images[n].reshape((imageSize, imageSize)), cmap='gray')
        else:
            figure.axes[n].imshow(images[n])

        title = nameFromLabelsAt(labels, n).title()
        wrappedTitle = "\n".join(wrap(title, 18))
        figure.axes[n].set_title(wrappedTitle, fontsize=10)

    for subplotAxes in figure.axes: subplotAxes.axis('off')
    figure.tight_layout()

def quickPlot():
    plot(_images, _labels, columns=5, rows=2)
