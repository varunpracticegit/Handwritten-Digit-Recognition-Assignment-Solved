import numpy as np
import os
import matplotlib.pyplot as plt
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout

# Get the data and pre-process it

(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train.shape, y_train.shape, X_test.shape, y_test.shape

def plot_input_image(i):
    plt.imshow(X_train[i], cmap='binary')
    plt.title(y_train[i])
    plt.axis('off')  # Turn off the axes
    plt.show()

for i in range(10):
    plot_input_image(i)


# Pre-process the images

# Normalizing the image to [0,1] range
X_train = X_train.astype(np.float32)/255
X_test = X_test.astype(np.float32)/255


# Reshape/Expand the dimensions of the images to (28, 28)
X_train = np.expand_dims(X_train, -1)
X_test = np.expand_dims(X_test, -1)


# Convert classes to one hot vectors
y_train = keras.utils.to_categorical(y_train)
y_test = keras.utils.to_categorical(y_test)

model = Sequential()

model.add(Conv2D(32, (3,3), input_shape=(28,28,1), activation='relu'))
model.add(MaxPool2D((2,2)))

model.add(Conv2D(64, (3,3), activation='relu'))
model.add(MaxPool2D((2,2)))

model.add(Flatten())

model.add(Dropout(0.25))

model.add(Dense(10, activation="softmax"))

model.summary()

model.compile(optimizer='adam', loss=keras.losses.categorical_crossentropy, metrics=['accuracy'])

# Callbacks
from keras.callbacks import EarlyStopping, ModelCheckpoint

# Easystopping
es = EarlyStopping(monitor='val_acc', min_delta=0.01, patience=4, verbose = 1)

# Model Check Point
mc = ModelCheckpoint("./bestmodel.h5", monitor="val_acc", verbose=1, save_best_only=True)

cb = [es, mc]


# Model Training
his = model.fit(X_train, y_train, epochs=2, validation_split=0.3)
model.save("bestmodel.h5")

model_S = keras.models.load_model("bestmodel.h5")

score = model_S.evaluate(X_test, y_test)

print(f" the model accuracy is {score[1]} ")