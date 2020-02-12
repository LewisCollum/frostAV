from keras.optimizers import SGD
from keras.callbacks import CSVLogger

import batch
from model import model

logger = CSVLogger('training.log', separator=',', append=False)

model.compile(
    loss = 'categorical_crossentropy',
    optimizer = SGD(lr=1e-3),
    metrics = ['accuracy'])

model.fit_generator(
    batch.trainIterator,
    validation_data = batch.validationIterator,
    steps_per_epoch = batch.sampleSize/batch.size,
    epochs = 20,
    callbacks=[logger])
        
model.save('fine_tune.h5')
