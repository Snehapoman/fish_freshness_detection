import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import os


# Function to resize image to a fixed size
def resize_image(image, width, height):
    return cv2.resize(image, (width, height))


# Function to resize image while maintaining aspect ratio
def resize_with_aspect_ratio(image, target_size):
    # Calculate aspect ratio of the image
    aspect_ratio = image.shape[1] / image.shape[0]

    # Calculate new size while maintaining aspect ratio
    new_width = target_size if aspect_ratio >= 1 else int(target_size * aspect_ratio)
    new_height = int(target_size / aspect_ratio) if aspect_ratio >= 1 else target_size

    # Resize the image
    resized_image = cv2.resize(image, (new_width, new_height))

    return resized_image


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


# Function to display the input image
def display_input_image(image):
    # Resize image while maintaining aspect ratio
    resized_image = resize_with_aspect_ratio(image, 300)

    # Convert image from OpenCV format to PIL format
    image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)

    # Display image using tkinter
    img = ImageTk.PhotoImage(image)
    input_image_label.config(image=img)
    input_image_label.image = img


# Function to process the input image
def process_image(k_mean, k_var):
    # Load the input image
    input_image_path = filedialog.askopenfilename()
    input_image = cv2.imread(input_image_path)

    # Resize the input image to a fixed size
    resized_input_image = resize_image(input_image, 907, 975)

    # Display the input image
    display_input_image(resized_input_image)

    # Convert input image to grayscale
    input_gray = cv2.cvtColor(resized_input_image, cv2.COLOR_BGR2GRAY)

    x, y, w, h = 907 - 292, 260 * 975 // 1080, 292, 168
    w = int(w * 1.25)
    h = int(h * 1.25)

    # Create a binary mask for the skin region
    input_mask_skin = np.zeros_like(input_gray)
    input_mask_skin[y:y + h, x:x + w] = 255

    # Convert input RGB image to HSV
    input_rgb_hsv = cv2.cvtColor(resized_input_image, cv2.COLOR_BGR2HSV)

    # Extract saturation (S) channel from the HSV image
    input_saturation_channel = input_rgb_hsv[:, :, 1]

    # Using binary mask input_mask_skin, segment the ROI from saturation channel
    input_roi_segmented = input_saturation_channel * (input_mask_skin / 255)

    # Calculate mean intensity and variance values of the segmented ROI for input image
    input_mean_intensity, input_variance = calculate_mean_intensity_and_variance(input_saturation_channel,
                                                                                 input_mask_skin)

    # Determine freshness of the input image
    freshness = determine_freshness(input_mean_intensity, input_variance, k_mean, k_var)

    # Update the GUI with the result
    result_label.config(
        text=f"Freshness of Input Image: {freshness}\nMean Value: {input_mean_intensity:.2f}\nVariance Value: {input_variance:.2f}")


# Path to the directory containing the main folder "skin_dataset"
main_dir = r'E:\Backups\Pycharm\FishFrreshnessDetection-skin--main\FishFrreshnessDetection-skin--main\skin_dataset'

# List subfolders within the main folder
subfolders = ['fresh', 'non-fresh']

# Initialize lists to store mean intensity and variance values
mean_intensities = []
variances = []

# Loop through each subfolder
for subfolder in subfolders:
    # Path to the subfolder containing images
    subfolder_dir = os.path.join(main_dir, subfolder)

    # Check if the directory exists
    if not os.path.exists(subfolder_dir):
        print(f"Directory {subfolder_dir} does not exist. Skipping.")
        continue

    # List all image files in the subfolder
    image_files = os.listdir(subfolder_dir)

    # Loop through each image in the subfolder
    for filename in image_files:
        # Path to the image file
        image_path = os.path.join(subfolder_dir, filename)
        
        # Check if it's a valid file and not a directory
        if not os.path.isfile(image_path):
            continue

        # Load the image
        IRGB = cv2.imread(image_path)

        # Resize the image to a fixed size
        resized_image = resize_image(IRGB, 907, 975)

        # Convert image to grayscale
        Igray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

        x, y, w, h = 907 - 292, 260 * 975 // 1080, 292, 168
        w = int(w * 1.25)
        h = int(h * 1.25)

        # Create a binary mask for the skin region
        Bmask_skin = np.zeros_like(Igray)
        Bmask_skin[y:y + h, x:x + w] = 255

        # Convert RGB image to HSV
        IRGB_HSV = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)

        # Extract saturation (S) channel from the HSV image
        saturation_channel = IRGB_HSV[:, :, 1]

        # Using binary mask Bmask_skin, segment the ROI from saturation channel
        ROI_segmented = saturation_channel * (Bmask_skin / 255)

        # Calculate mean intensity and variance values of the segmented ROI
        mean_intensity, variance = calculate_mean_intensity_and_variance(saturation_channel, Bmask_skin)

        # Append mean intensity and variance values to lists
        mean_intensities.append(mean_intensity)
        variances.append(variance)

# Calculate average mean intensity and variance for fresh and non-fresh samples
avg_mean_fresh = np.mean(mean_intensities[:len(mean_intensities) // 2])
avg_mean_non_fresh = np.mean(mean_intensities[len(mean_intensities) // 2:])
avg_variance_fresh = np.mean(variances[:len(variances) // 2])
avg_variance_non_fresh = np.mean(variances[len(variances) // 2:])

# Compute threshold values
k_mean = (avg_mean_fresh + avg_mean_non_fresh) / 2
k_var = (avg_variance_fresh + avg_variance_non_fresh) / 2

# Create the main application window
root = tk.Tk()
root.title("FRESHNESS DETECTOR")

# Create a colorful background
background_label = tk.Label(root, bg="lightblue")
background_label.place(relwidth=1, relheight=1)

# Create a title label
title_label = tk.Label(root, text="FRESHNESS DETECTOR", bg="lightblue", font=("Helvetica", 20, "bold"))
title_label.pack(pady=20)

# Create a label to display the input image
input_image_label = tk.Label(root, bg="white")
input_image_label.pack(pady=10)

# Create an upload button
upload_button = tk.Button(root, text="Upload Image", command=lambda: process_image(k_mean, k_var))
upload_button.pack(pady=10)

# Create a label to display the result
result_label = tk.Label(root, bg="lightblue")
result_label.pack(pady=10)

# Run the application
root.mainloop()
