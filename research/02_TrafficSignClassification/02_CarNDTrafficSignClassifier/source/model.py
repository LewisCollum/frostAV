import keras
import keras.layers as layers

import batch
 
model = keras.models.Sequential()

for i in range(3):
    model.add(layers.Conv2D(filters=32*2**i, kernel_size=(3, 3), activation='relu', input_shape=batch.imageShape))
    model.add(layers.Dropout(0.1))
    model.add(layers.MaxPool2D(pool_size=(2, 2)))

model.add(layers.BatchNormalization())
model.add(layers.Flatten())

model.add(layers.Dense(units=120, activation='relu'))
model.add(layers.Dense(units=84, activation='relu'))
model.add(layers.Dense(units=batch.classCount, activation = 'softmax'))

if __name__ == '__main__':
    print(model.summary())
