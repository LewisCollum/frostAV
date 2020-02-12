import keras
import keras.layers as layers

import common
import batch
 
model = keras.models.Sequential()
model.add(layers.Conv2D(filters=6, kernel_size=(3, 3), activation='relu', input_shape=batch.images[0].shape))
model.add(layers.AveragePooling2D())

model.add(layers.Conv2D(filters=16, kernel_size=(3, 3), activation='relu'))
model.add(layers.AveragePooling2D())

model.add(layers.Flatten())

model.add(layers.Dense(units=1024, activation='relu'))
model.add(layers.BatchNormalization(axis=1))
model.add(layers.Dense(units=1024, activation='relu'))
model.add(layers.BatchNormalization(axis=1))
model.add(layers.Dense(units=batch.classCount, activation = 'softmax'))

if __name__ == '__main__':
    print(model.summary())
    keras.utils.plot_model(model, to_file='model.png')
