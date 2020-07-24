import tensorflow as tf
import cv2
import numpy as np
import PIL

def train_glove_model():

    class myCallback(tf.keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs={}):
            if(logs.get('accuracy') > 0.998):
                print("\nReached 99.9% accuracy so cancelling training!")
                self.model.stop_training = True
    
    model = tf.keras.models.Sequential([
        
        tf.keras.layers.Conv2D(16, (3,3), activation='relu', input_shape=(150, 150, 3)),
        tf.keras.layers.MaxPooling2D(2, 2),
        # 2
        tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2,2),
        # 3
        tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2,2),
        # Flatten the results to feed into a DNN
        tf.keras.layers.Flatten(),
        # 512 neuron hidden layer
        tf.keras.layers.Dense(256, activation='relu'),
        # Only 1 output neuron. Sigmoid is binary classifier
    tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    from tensorflow.keras.optimizers import RMSprop

    model.compile(loss='binary_crossentropy',
              optimizer=RMSprop(lr=0.001),
              metrics=['accuracy'])
        
    from tensorflow.keras.preprocessing.image import ImageDataGenerator

    train_datagen = ImageDataGenerator(rescale=1/255)

    train_generator = train_datagen.flow_from_directory(
        './dataset',
        target_size=(150, 150),
        batch_size=50,
        class_mode='binary'
        )
    # Expected output: 'Found 80 images belonging to 2 classes'

    history = model.fit_generator(
          train_generator,
      steps_per_epoch=4,  
      epochs=25,
      verbose=1,
      callbacks=myCallback())
    model.save('model.h5')
    return history.history['accuracy'][-1]

value = train_glove_model()
print("Accuracy: " + str(value*100) + "%")
