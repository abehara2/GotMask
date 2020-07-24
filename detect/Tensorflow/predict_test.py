import tensorflow as tf
import cv2
import numpy as np

model = tf.keras.models.load_model('model.h5')
model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

img = cv2.imread('/Users/ashankbehara/Desktop/test.png')
img = cv2.resize(img,(150,150))
img = np.reshape(img,[1,150,150,3])

classes = model.predict(img)
print(classes)
