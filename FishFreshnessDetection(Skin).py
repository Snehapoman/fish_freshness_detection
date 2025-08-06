import cv2
import numpy as np
import os

# Function to resize image to a fixed size
def resize_image(image, width, height):
    return cv2.resize(image, (width, height))

# Function to calculate mean intensity and variance values for segmented region
def calculate_mean_intensity_and_variance(image, mask):
    mean_intensity = np.mean(image * (mask / 255))
    variance = np.var(image * (mask / 255))
    return mean_intensity, variance

# Function to determine if the input image is fresh or not
def determine_freshness(input_mean, input_var, k_mean, k_var):
    if input_mean >= k_mean and input_var >= k_var:
        return "Fresh"
    else:
        return "Non-fresh"

# Path to the directory containing the main folder "skin_dataset"
main_dir = (r'C:\Users\perum\OneDrive\Documents\skin_dataset')

# List subfolders within the main folder
subfolders = ['fresh', 'non-fresh']

# Initialize lists to store mean intensity and variance values
mean_intensities = []
variances = []

# Loop through each subfolder
for subfolder in subfolders:
    # Path to the subfolder containing images
    subfolder_dir = os.path.join(main_dir, subfolder)

    # List all image files in the subfolder
    image_files = os.listdir(subfolder_dir)

    # Loop through each image in the subfolder
    for filename in image_files:
        # Load the image
        IRGB = cv2.imread(os.path.join(subfolder_dir, filename))

        # Resize the image to a fixed size
        resized_image = resize_image(IRGB, 907, 975)

        # Convert image to grayscale
        Igray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

        x, y, w, h = 907 - 292, 260 * 975 // 1080, 292, 168
        w = int(w * 1.25)
        h = int(h * 1.25)

        # Create a binary mask for the skin region
        Bmask_skin = np.zeros_like(Igray)
        Bmask_skin[y:y+h, x:x+w] = 255

        # Convert RGB image to HSV
        IRGB_HSV = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)

        # Extract saturation (S) channel from the HSV image
        saturation_channel = IRGB_HSV[:,:,1]

        # Using binary mask Bmask_skin, segment the ROI from saturation channel
        ROI_segmented = saturation_channel * (Bmask_skin / 255)

        # Calculate mean intensity and variance values of the segmented ROI
        mean_intensity, variance = calculate_mean_intensity_and_variance(saturation_channel, Bmask_skin)

        # Append mean intensity and variance values to lists
        mean_intensities.append(mean_intensity)
        variances.append(variance)

# Calculate average mean intensity and variance for fresh and non-fresh samples
avg_mean_fresh = np.mean(mean_intensities[:len(mean_intensities)//2])
avg_mean_non_fresh = np.mean(mean_intensities[len(mean_intensities)//2:])
avg_variance_fresh = np.mean(variances[:len(variances)//2])
avg_variance_non_fresh = np.mean(variances[len(variances)//2:])

# Compute threshold values
k_mean = (avg_mean_fresh + avg_mean_non_fresh) / 2
k_var = (avg_variance_fresh + avg_variance_non_fresh) / 2

# Display threshold values
print("\nThreshold Values:")
print("-------------------------")
print(f"Mean Threshold (k_mean): {k_mean:.2f}")
print(f"Variance Threshold (k_var): {k_var:.2f}")

# Prompt user to provide the input image path
input_image_path = input("\nPlease provide the path to the input image: ")

# Load the input image
input_image = cv2.imread(input_image_path)

# Resize the input image to a fixed size
resized_input_image = resize_image(input_image, 907, 975)

# Convert input image to grayscale
input_gray = cv2.cvtColor(resized_input_image, cv2.COLOR_BGR2GRAY)

x, y, w, h = 907 - 292, 260 * 975 // 1080, 292, 168
w = int(w * 1.25)
h = int(h * 1.25)

# Create a binary mask for the skin region
input_mask_skin = np.zeros_like(input_gray)
input_mask_skin[y:y+h, x:x+w] = 255

# Convert input RGB image to HSV
input_rgb_hsv = cv2.cvtColor(resized_input_image, cv2.COLOR_BGR2HSV)

# Extract saturation (S) channel from the HSV image
input_saturation_channel = input_rgb_hsv[:,:,1]

# Using binary mask input_mask_skin, segment the ROI from saturation channel
input_roi_segmented = input_saturation_channel * (input_mask_skin / 255)

# Calculate mean intensity and variance values of the segmented ROI for input image
input_mean_intensity, input_variance = calculate_mean_intensity_and_variance(input_saturation_channel, input_mask_skin)

# Determine freshness of the input image
freshness = determine_freshness(input_mean_intensity, input_variance, k_mean, k_var)

# Display mean and variance values of the input image
print("\nMean Value of Input Image:", input_mean_intensity)
print("Variance Value of Input Image:", input_variance)

# Determine if the mean and variance values are below or above the threshold values
if input_mean_intensity >= k_mean and input_variance >= k_var:
    print("Mean and Variance values are above the threshold values.")
    print("Freshness of Input Image:", freshness)
else:
    print("Mean and Variance values are below the threshold values.")
    print("Freshness of Input Image:", freshness)
