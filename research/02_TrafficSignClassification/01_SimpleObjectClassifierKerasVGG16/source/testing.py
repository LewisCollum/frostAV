import keras
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator

import matplotlib.pyplot as pyplot
import numpy as np
import common

model = load_model('fine_tune.h5')

test_datagen = ImageDataGenerator()

test_generator = test_datagen.flow_from_directory(
                        directory=common.testPath, 
                        target_size=(common.imageSize, common.imageSize),
                        color_mode='rgb',
                        shuffle=False,
                        class_mode='categorical',
                        batch_size=1)

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

    label_map = (test_generator.class_indices)
    label_map = dict((v,k) for k,v in label_map.items()) #flip k,v
    predictions = [label_map[k] for k in name]
    true_value = [label_map[k] for k in true_name]

    image = x_batch[0].astype(np.int)
    fig.add_subplot(rows, columns, i)
    pyplot.axis('off')
    pyplot.title(f"guess: {predictions[0]}\nactual: {true_value[0]}")
    pyplot.imshow(image)

pyplot.show()
