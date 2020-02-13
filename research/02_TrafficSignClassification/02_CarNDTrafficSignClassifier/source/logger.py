import pandas
import matplotlib.pyplot as pyplot
import keras
import path
import os

def addAccuracyPlot(run):
    log = pandas.read_csv(run.log)

    figure, axes = pyplot.subplots(1, 2, figsize=(8, 4))
    axes[0].set_title('Accuracy')
    axes[0].plot(log['epoch'], log['accuracy'], log['val_accuracy'])
    axes[0].legend(['training accuracy', 'validation accuracy'])
    axes[0].set_xlabel('epoch')

    axes[1].set_title('Loss')
    axes[1].plot(log['epoch'], log['loss'], log['val_loss'])
    axes[1].legend(['training loss', 'validation loss'])
    axes[1].set_xlabel('epoch')
    
    figure.subplots_adjust(top=0.85)
    figure.suptitle('Accuracy & Loss of Training & Validation Sets per Epoch')

    pyplot.savefig(run.accuracy)

    
def addModelDiagram(run):
    model = keras.models.load_model(run.model)
    keras.utils.plot_model(model, run.modelDiagram)

    
if __name__ == '__main__':
    for runName in next(os.walk(path.run.directory))[1]:
        run = path.run.loadFromName(runName)
        if not path.run.has(run.accuracy):
            addAccuracyPlot(run)
        if not path.run.has(run.modelDiagram):
            addModelDiagram(run)
