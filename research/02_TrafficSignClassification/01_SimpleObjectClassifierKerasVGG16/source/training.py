from keras.optimizers import SGD

import batch
from model import model

model.compile(
    loss = 'categorical_crossentropy',
    optimizer = SGD(lr=1e-3),
    metrics = ['accuracy'])

model.fit_generator(
    batch.trainingBatchIterator,
    steps_per_epoch = batch.sampleSize/batch.size,
    epochs = 2)
        
model.save('fine_tune.h5')
