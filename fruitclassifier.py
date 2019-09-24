# -*- coding: utf-8 -*-
"""fruitclassifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16-dEdH40cf424lABQebMHv4ipd0mK0Q4
"""

from fastai.vision import *
from fastai import *
from imutils import paths

!pip install imutils

from google.colab import drive
drive.mount('/content/drive')

classes=['apples','mango','grapes','orange']

path = Path('/content/drive/My Drive/classification')

for c in classes:
    print(c)
    verify_images(path/c,delete=True,max_size=500)

np.random.seed(42)
data=ImageDataBunch.from_folder(path,train=".",valid_pct=0.2,ds_tfms=get_transforms(),bs=2,size=224,num_workers=5).normalize(imagenet_stats)

data.classes

data.show_batch(rows=3,figsize=(7,8))

data.classes, data.c, len(data.train_ds), len(data.valid_ds)

learn = cnn_learner(data, models.resnet34, metrics=accuracy)

learn.fit_one_cycle(6)

learn.save('stage-1')

learn.unfreeze()
learn.fit_one_cycle(10)

learn.load('stage-1');

interp = ClassificationInterpretation.from_learner(learn)

interp.plot_confusion_matrix()

learn.export()

learn = load_learner(path)

img = open_image('/content/drive/My Drive/classification/appletest.jpg')
img

pred_class,pred_idx,outputs = learn.predict(img)
pred_class