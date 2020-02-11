import pandas

signNames = pandas.read_csv("../data/signnames.csv")['SignName'].values

trainPath = "../data/train"
modelPath = "./model"
imageSize = 30
