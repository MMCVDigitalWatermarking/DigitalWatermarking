[![Build Status](https://travis-ci.com/MMCVDigitalWatermarking/DigitalWatermarking.svg?branch=main)](https://travis-ci.com/MMCVDigitalWatermarking/DigitalWatermarking)
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
## 2. DCTWatermarker
#### 2.1 basic usage - images


```
>>> from Watermark_DCT import WatermarkDCT
>>> dct_wm = WatermarkDCT('media/test.png', num_of_co=1000, alpha=0.1)
>>> dct_wm.encode_watermark()
>>> print('is the input image our watermarked image?: ' + str(dct_wm.detect_watermark()))
>>> print('is the input image our watermarked image?: ' + str(dct_wm.detect_watermark('media/landscape.png')))
>>> dct_wm.show_watermark_results()
>>> dct_wm.decode_watermark()
>>> dct_wm.show_watermark_results()
```

