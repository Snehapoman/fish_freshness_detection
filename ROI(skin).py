import cv2
import numpy as np
import matplotlib.pyplot as plt

# Function to resize image to a fixed size
def resize_image(image, width, height):
    return cv2.resize(image, (width, height))

# Load the image
image_path = 'path_to_your_image.jpg'  # Change this to the path of your image file
IRGB = cv2.imread(image_path)

if IRGB is None:
    raise FileNotFoundError(f"Image not found at the path: {image_path}")

# Resize the image to a fixed size
resized_image = resize_image(IRGB, 907, 975)

# Convert image to grayscale
Igray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

# Parameters for the rectangular shape (skin)
# Move the rectangle towards the rightmost end
x, y, w, h = 907 - 292, 260 * 975 // 1080, 292, 168

# Increase the area of the rectangle by 25%
w = int(w * 1.25)
h = int(h * 1.25)

# Create a binary mask for the skin region
Bmask_skin = np.zeros_like(Igray)
Bmask_skin[y:y+h, x:x+w] = 255

# Convert RGB image to HSV
IRGB_HSV = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)

# Extract saturation (S) channel from the HSV image
saturation_channel = IRGB_HSV[:, :, 1]

# Using binary mask Bmask_skin, segment the ROI from saturation channel
ROI_segmented = saturation_channel * (Bmask_skin / 255)

# Calculate mean intensity value of the segmented ROI for skin rectangle
mean_intensity_skin = np.mean(saturation_channel * (Bmask_skin / 255))

print(f"Mean intensity of segmented skin region: {mean_intensity_skin}")

# Display the images
plt.figure(figsize=(16, 6))

# RGB image
plt.subplot(2, 3, 1)
plt.imshow(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))
plt.title('RGB Image')
plt.axis('off')
cv2.imwrite('RGB_Image.jpg', resized_image)

# Grayscale image
plt.subplot(2, 3, 2)
plt.imshow(Igray, cmap='gray')
plt.title('Grayscale')
plt.axis('off')
cv2.imwrite('Grayscale_Image.jpg', Igray)

# Binary Mask - Skin Rectangle
plt.subplot(2, 3, 3)
plt.imshow(Bmask_skin, cmap='gray')
plt.title('Binary Mask - Skin Rectangle')
plt.axis('off')
cv2.imwrite('Binary_Mask_Skin_Rectangle.jpg', Bmask_skin)

# HSV image
plt.subplot(2, 3, 4)
plt.imshow(cv2.cvtColor(IRGB_HSV, cv2.COLOR_HSV2RGB))
plt.title('HSV Image')
plt.axis('off')
cv2.imwrite('HSV_Image.jpg', cv2.cvtColor(IRGB_HSV, cv2.COLOR_HSV2BGR))

# Saturation channel
plt.subplot(2, 3, 5)
plt.imshow(saturation_channel, cmap='gray')
plt.title('Saturation Channel')
plt.axis('off')
cv2.imwrite('Saturation_Channel.jpg', saturation_channel)

# Segmented ROI
plt.subplot(2, 3, 6)
plt.imshow(ROI_segmented, cmap='gray')
plt.title('Segmented ROI')
plt.axis('off')
cv2.imwrite('Segmented_ROI.jpg', ROI_segmented)

plt.tight_layout()
plt.show()
