from image_class_prep import Dataset
import os

data_dir = os.path.join('datasets')

Dataset.set_dir(data_dir)
Dataset.set_imgDim(224,224)
Dataset.set_pTrain(0.6)

Dataset.iniciar()
