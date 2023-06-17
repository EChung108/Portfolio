import numpy as np
import pandas as pd
import matplotlib.pyplot as plt#to plot accuracy
import tensorflow as tf
from PIL import Image, ImageOps
import os

from sklearn import metrics
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split #to split training and testing data
from keras.utils import to_categorical ##to convert the labels present in y_train and t_test into one-hot encoding
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout ##to create CNN


data = []
labels = []
classes = 6
cur_path = os.getcwd()
#Retrieving the images and their labels
for i in range(classes):
   path = os.path.join(cur_path,'Documents\AA Uni\Year 3\Robotics\Assignment 3\Signdata',str(i))
   images = os.listdir(path)

   for a in images:
         
         image = Image.open(path + '\\'+ a)
         image = image.resize((30,30))
         image = np.array(image)

         data.append(image)
         labels.append(i)
#Converting lists into numpy arrays

data = np.array(data)
labels = np.array(labels)

print(data.shape, labels.shape)

#Splitting training and testing dataset
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
#Converting the labels into one hot encoding
y_train = to_categorical(y_train, 6)
y_test = to_categorical(y_test, 6)
#Building the model

model = Sequential()
model.add(Conv2D(filters=32, kernel_size=(5,5), activation='relu', input_shape= X_train.shape[1:]))
model.add(Conv2D(filters=32, kernel_size=(5,5), activation='relu',))

model.add(MaxPool2D(pool_size=(2, 2)))

model.add(Dropout(rate=0.25))

model.add(Conv2D(filters=64, kernel_size=(3,3), activation='relu'))
model.add(Conv2D(filters=64, kernel_size=(3,3), activation='relu'))

model.add(MaxPool2D(pool_size=(2, 2)))


model.add(Dropout(rate=0.25))

model.add(Flatten())

model.add(Dense(256, activation='relu'))

model.add(Dropout(rate=0.5))

model.add(Dense(6, activation='softmax'))
#Compilation of the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
eps = 30
anc = model.fit(X_train, y_train, batch_size=32, epochs=eps, validation_data=(X_test, y_test))
model.save('Documents\AA Uni\Year 3\Robotics\Assignment 3\CNN_modelV2.h5')
model.summary()
a
#testing accuracy on test dataset

y_test = pd.read_csv('Documents\AA Uni\Year 3\Robotics\Assignment 3\Signdata\Test.csv')
labels = y_test["ClassId"].values
imgs = y_test["Path"].values
print('imgs holds:', imgs)
print(len(imgs))
# imgs = os.listdir(imgs)
data=[]


for i in range(2160):
   img = imgs[i]
   image = Image.open('Documents\AA Uni\Year 3\Robotics\Assignment 3\Signdata' + '\\' + img)
   image = image.resize((30,30))
   data.append(np.array(image))
X_test=np.array(data)
pred = np.argmax(model.predict(X_test), axis=-1)
#Accuracy with the test data
print("Accuracy score: ", accuracy_score(labels,pred))
model.save('Documents\AA Uni\Year 3\Robotics\Assignment 3\CNN_test2.h5')
