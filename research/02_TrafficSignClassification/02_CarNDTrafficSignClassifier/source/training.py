import keras
from keras.callbacks import CSVLogger

import path
from model import model
import batch
import logger

path.run.make()
run = path.run.loadCurrent()

model.compile(
    loss = 'categorical_crossentropy',
    optimizer = keras.optimizers.Adam(),
    metrics = ['accuracy'])

model.fit_generator(
    batch.trainIterator,
    validation_data = batch.validationIterator,
    steps_per_epoch = batch.trainIterator.n/batch.size,
    epochs = 1,
    callbacks = [
        keras.callbacks.CSVLogger(run.log, separator=',', append=False)
    ])

model.save(run.model)
logger.addModelDiagram(run)
logger.addAccuracyPlot(run)
