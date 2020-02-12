import keras
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as pyplot
import numpy as np

import common
import preprocessing
import batch

model = load_model('fine_tune.h5')

test_generator = batch.batchGenerator.flow_from_directory(
    directory="../data", 
    target_size=(common.imageSize, common.imageSize),
    color_mode='grayscale',
    shuffle=False,
    batch_size=1,
    classes=['test'])

filenames = test_generator.filenames
nb_samples = len(filenames)

fig=pyplot.figure()
columns = 4
rows = 4

for i in range(1, columns*rows):
    x_batch, y_batch = test_generator.next()

    name = model.predict(x_batch)
    name = np.argmax(name, axis=-1)
    true_name = y_batch
    true_name = np.argmax(true_name, axis=-1)

    label_map = (batch.trainIterator.class_indices)
    label_map = dict((v,k) for k,v in label_map.items()) #flip k,v
    predictions = [label_map[k] for k in name]
    true_value = [label_map[k] for k in true_name]

    image = x_batch[0]
    fig.add_subplot(rows, columns, i)
    pyplot.axis('off')
    pyplot.title(f"guess: {predictions[0]}\nactual: {true_value[0]}")
    pyplot.imshow(image[:,:,0], cmap='gray')

pyplot.show()
