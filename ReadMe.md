# Got a Mask?

This project is a means to screen medical and non personell to make sure that they are wearing adequate equipment prior to entering a building. The capture is segmented into two segments for hand detection which was passed through a CNN built with ```Tensorflow``` and ```Keras```. The transfer learning model is held in the ```./detect/Tensorflow/model.h5``` file if you want to run your own glove detection for a project.

 The mask detection is done with a HAAR Cascade Classifier implemented in ```OpenCV```. It tracks the mouth and frontal face and if there is a mouth contained in the frontal face it identifies the person as unmasked. If two gloves and a masked face are detected in the frame, the system will print out that all safety checks have passed. <br/>

In the near future I hope to release this on a Raspberry Pi 4 with a Coral Edge TPU in order to isolate this from my computer and have it run on a separate device with its own camera and display. <br/>

![gif](media/shortened.gif)



