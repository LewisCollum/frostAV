from keras.optimizers import SGD

import batch
from model import model

model.compile(
    loss = 'categorical_crossentropy',
    optimizer = SGD(lr=1e-3),
    metrics = ['accuracy'])

# # Start the training process
# model.fit(x_train, y_train, validation_split=0.30, size=32, epochs=50, verbose=2)

# # #save the model
# model.save('catdog.h5')

history = model.fit_generator(
    batch.trainingBatchIterator,
    steps_per_epoch = batch.sampleSize/batch.size,
    epochs = 10)
        
model.save('fine_tune.h5')
