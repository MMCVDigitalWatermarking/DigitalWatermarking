# Digital Watermarking
***
## 0. Setup
```
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```
***
## 1. LSBWatermarker
#### 1.1 basic usage - text messages
```
>>> from watermarker import LSBWatermarker
>>> import cv2
>>> image = cv2.imread('media/test.png')
>>> watermarker = LSBWatermarker(image=image, mode='encode-message', message='secret', filename='result.png')
>>> watermarker.run()
>>> image = cv2.imread('result.png')
>>> watermarker = LSBWatermarker(image=image, mode='decode-message')
>>> watermarker.run()
Decoded message is: 'secret'
```
***
