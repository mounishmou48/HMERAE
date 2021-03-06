from __future__ import print_function
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

#batch_size = 8
#epochs = 12

# load the dataset
X, y = dataset.load_dataset()

# reshape the features for the network and determine the shape based on the library's current image format
if K.image_data_format() == 'channels_first':
    X = X.reshape(X.shape[0], 1, dataset.IMG_ROWS, dataset.IMG_COLS)
    input_shape = (1, dataset.IMG_ROWS, dataset.IMG_COLS)
else:
    X = X.reshape(X.shape[0], dataset.IMG_ROWS, dataset.IMG_COLS, 1)
    input_shape = (dataset.IMG_ROWS, dataset.IMG_COLS, 1)

X = X.astype('float32')

# convert class vectors to binary class matrices
y = keras.utils.to_categorical(y, dataset.NUM_CLASSES)

# split the dataset into training and testing (validation) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)

# create the model
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                activation='relu',
                input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(dataset.NUM_CLASSES, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
             optimizer=keras.optimizers.Adadelta())

# train and save the model
#model.fit(X_train, y_train,
#          batch_size=batch_size,
#          epochs=epochs,
#          verbose=1,
#          validation_data=(X_test, y_test))
#model.save('model.h5')

# load and predict using the model
model.load_weights('model.h5')
model.predict_classes(X_test, verbose=0)
