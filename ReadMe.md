# Got a Mask?

This project is a means to screen medical and non personell to make sure that they are wearing adequate equipment prior to entering a building. The capture is segmented into two segments for hand detection which was passed through a CNN built with ```Tensorflow``` and ```Keras```. The transfer learning model is held in the ```./detect/Tensorflow/model.h5``` file if you want to run your own glove detection for a project.

 The mask detection is done with a HAAR Cascade Classifier implemented in ```OpenCV```. It tracks the mouth and frontal face and if there is a mouth contained in the frontal face it identifies the person as unmasked. If two gloves and a masked face are detected in the frame, the system will print out that all safety checks have passed. <br/>


![gif](media/shortened.gif)


## Raspberry Pi Setup

### Downloads

The major installs to run the file ```./detect/integrate.py``` successfully on the Raspberry Pi are Tensorflow, Keras and OpenCV. The install for opencv is fairly straightforward as all it needs is a pip install. Due to the ARM architecture of the board, the install of Tensorflow and Keras are a little more complicated run the following bashc commands in order to install all the necessary dependencies

```
pip install opencv-contrib-python==4.1.0.25
sudo apt-get install -y libhdf5-dev libc-ares-dev libeigen3-dev
python3 -m pip install keras_applications==1.0.8 --no-deps
python3 -m pip install keras_preprocessing==1.1.0 --no-deps
python3 -m pip install h5py==2.9.0
sudo apt-get install -y openmpi-bin libopenmpi-dev
sudo apt-get install -y libatlas-base-dev
python3 -m pip install -U six wheel mock
wget https://github.com/lhelontra/tensorflow-on-arm/releases/download/v2.0.0/tensorflow-2.0.0-cp37-none-linux_armv7l.whl
python3 -m pip uninstall tensorflow
python3 -m pip install tensorflow-2.0.0-cp37-none-linux_armv7l.whl
```
### Coniguration

The circuit I built require use of an i2c interface and external camera.
