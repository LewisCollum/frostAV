import keras
from keras.models import Model, load_model
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.vgg16 import VGG16

import common

baseModel = VGG16(
    weights = 'imagenet',
    include_top = False,
    input_shape = (common.imageSize, common.imageSize, 3))

for layer in baseModel.layers: 
    layer.trainable = False
 
model = keras.models.Sequential()
model.add(baseModel)

model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dense(1024, activation='relu'))
model.add(Dense(common.classCount, activation='softmax'))

if __name__ == '__main__':
    print(model.summary())
