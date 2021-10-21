import numpy as np
import cv2

# read
img = cv2.imread('../data/test/CARDCARESTUB1-PN0004372-2019-12-16.jpg', cv2.IMREAD_GRAYSCALE)

# increase contrast
pxmin = np.min(img)
pxmax = np.max(img)
imgContrast = (img - pxmin) / (pxmax - pxmin) * 255

# increase line width
kernel = np.ones((3, 3), np.uint8)
imgMorph = cv2.erode(imgContrast, kernel, iterations = 1)

# write
cv2.imshow("preprocess", imgMorph)
cv2.waitKey()
cv2.imwrite('out.jpg', imgMorph)