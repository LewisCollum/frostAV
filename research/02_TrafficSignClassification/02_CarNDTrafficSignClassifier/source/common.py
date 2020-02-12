import pandas

signNames = pandas.read_csv("../data/signnames.csv")['SignName'].values

trainPath = "../data/train"
testPath = "../data/test"
modelPath = "./model"
imageSize = 32
