import cv2
import numpy as np
import fastcv
from imwatermark import WatermarkDecoder

l = 32

img = cv2.imread('/Users/cfu/Downloads/titang1.png')
decoder = WatermarkDecoder('bytes', l)
watermark = decoder.decode(img, 'dwtDct')
watermark = str(watermark)
print(watermark)
img = cv2.imread('/Users/cfu/Downloads/titang12.png')
decoder = WatermarkDecoder('bytes', l)
watermark = decoder.decode(img, 'dwtDct')
watermark = str(watermark)
print(watermark)

img = cv2.imread('/Users/cfu/Downloads/sd.png')
decoder = WatermarkDecoder('bytes', l)
watermark = decoder.decode(img, 'dwtDct')
watermark = str(watermark)
print(watermark)


import matplotlib.pyplot as plt
from PIL import Image

# 加载图片
image_path = '/Users/cfu/Downloads/titang1.png'
image = Image.open(image_path).convert('L')  # 转换为灰度图
image_array = np.array(image)

# 执行FFT
fft_result = np.fft.fft2(image_array)
fft_shift = np.fft.fftshift(fft_result)

# 计算幅度谱
magnitude_spectrum = 20 * np.log(np.abs(fft_shift))

# 绘制频谱图
plt.figure(figsize=(10, 6))
plt.imshow(magnitude_spectrum, cmap='gray')
plt.title("Frequency Spectrum")
plt.colorbar()
plt.show()
