#Version 0.0.4
#20/06/2023
#RichRadd Bad Programming

import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import time
import os

image_folder = 'images/'  # Path to the folder containing the images
image_files = {}
threshold = 0.85

# Iterate over the files in the folder
for filename in os.listdir(image_folder):
    if filename.endswith('.png'):  # Filter only PNG files (modify as per your requirements)
        key = os.path.splitext(filename)[0]  # Use the filename (without extension) as the dictionary key
        image_path = os.path.join(image_folder, filename)  # Create the full path to the image file
        image_files[key] = image_path  # Add the key-value pair to the dictionary

# Load target images
target_images = {}
for name, filename in image_files.items():
    target_images[name] = cv2.imread(filename)

# Define functions for each action
def click_image_center(img, loc, x, y):
    h, w = img.shape[::-1][:2]
    center_x = loc[0] + w // 2
    center_y = loc[1] + h // 2
    pyautogui.moveTo(x + center_x, y + center_y, duration=.1)
    pyautogui.click(clicks=1, interval=1)

def click_defence_icon(x, y):
    pyautogui.moveTo(x + 200, y + 960, duration=.1)
    pyautogui.click(clicks=1, interval=1)

def perform_action(x, y, action_name, result_max_val, result_max_loc):
    if result_max_val < threshold:
        return
    
    if action_name == 'claim1' or action_name == 'tor_claim' or action_name == 'tor_end' or action_name == 'tor_next'or action_name == 'claim2':
        click_image_center(target_images[action_name], result_max_loc, x, y)
        print("__*** Non regular button pressed ***__" * 1)
        print(action_name, "\n")
        return

    if action_name == 'health_upgrade':
        click_image_center(target_images[action_name], result_max_loc, x+130, y)
        return
    
    if action_name == 'retry_game' or action_name == 'start_game':
        click_image_center(target_images[action_name], result_max_loc, x, y)
        click_defence_icon(x, y)
        return

    click_image_center(target_images[action_name], result_max_loc, x, y)
    return

# Define the main loop
def main_cycle():
    # Get the Bluestacks window's position and size
    bluestacks = gw.getWindowsWithTitle("Bluestacks")[0]
    x, y, w, h = bluestacks.left, bluestacks.top, bluestacks.width, bluestacks.height
    if bluestacks.height != 990:
        print("*** WINDOW WRONG SIZE *** - PLEASE ENSURE THE WINDOW HAS A HEIGHT OF 990 - Use Window Size.py to see window size and adjust\n" * 10)
    
    # Take a screenshot of the window
    screenshot = np.array(pyautogui.screenshot(region=(x, y, w, h)))
    screenshot_rgb = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    # Perform template matching to find the target images
    results = {}
    for name, target_image in target_images.items():
        results[name] = cv2.matchTemplate(screenshot_rgb, target_image, cv2.TM_CCOEFF_NORMED)

    # Get the positions of the best matches and perform the corresponding action
    for name, result in results.items():
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        perform_action(x, y, name, max_val, max_loc)

# Run the main loop
while True:
    main_cycle()
    time.sleep(20)
