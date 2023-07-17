#Version 0.1.0
#17/07/2023
#RichRadd Bad Programming

import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import time
import os

#### SETTINGS ####
#### Make sure the True/False has the first letter as a capital letter ####
defence_build = True
#Short Run Defence
#perk_choices = ['coins', 'gt', 'gamespeed', 'bosshealthbutspeed', 'maxhealth', 'defenceprecent', 'freeups', 'orbs', 'bounceshot', 'lmd', 'pwr', 'dw', 'damagemulti', 'cfradius', 'randultimate', 'sldamage', 'enemydamtowerdam']
#Long Run Defence
perk_choices = ['pwr', 'gt', 'coins', 'gamespeed', 'bosshealthbutspeed', 'freeups', 'defenceprecent', 'maxhealth', 'orbs', 'enemydamtowerdam', 'damagemulti', 'bounceshot', 'cfradius', 'dw', 'lmd', 'sldamage', 'randultimate']
#Long Run Damage
#perk_choices = ['pwr', 'gt', 'coins', 'gamespeed', 'sldamage', 'freeups', 'enemyspeedbutenemydamage', 'damagemulti', 'bosshealthbutspeed', 'bounceshot', 'cfradius', 'lmd', 'orbs', 'rangebutdamage', 'defenceprecent', 'dw', 'maxhealth', 'randultimate']
#### END SETTINGS ####

# Load images from the "images" folder
image_folder = 'images/'
image_files = {}
threshold = 0.85

# Iterate over the files in the "images" folder
for filename in os.listdir(image_folder):
    if filename.endswith('.png'):
        key = os.path.splitext(filename)[0]
        image_path = os.path.join(image_folder, filename)
        image_files[key] = image_path

# Load target images from the "images" folder
target_images = {}
for name, filename in image_files.items():
    target_images[name] = cv2.imread(filename)

# Load images from the "perkimages" folder
perk_folder = 'perkimages/'
perk_files = {}

# Iterate over the files in the "perkimages" folder
for filename in os.listdir(perk_folder):
    if filename.endswith('.png'):
        key = os.path.splitext(filename)[0]
        image_path = os.path.join(perk_folder, filename)
        perk_files[key] = image_path

# Load target images from the "perkimages" folder
perk_images = {}
for name, filename in perk_files.items():
    perk_images[name] = cv2.imread(filename)

perks_enabled = True

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

def perks():
    global perks_enabled

    # Take a new screenshot
    bluestacks = gw.getWindowsWithTitle("Bluestacks")[0]
    x, y, w, h = bluestacks.left, bluestacks.top, bluestacks.width, bluestacks.height
    screenshot = take_screenshot(x, y, w, h)

    # Calculate the top half of the screenshot
    top_half = screenshot[:h//2, :]

    # Look for images in perk_choices in the top half
    for perk_choice in perk_choices:
        image_path = perk_files.get(perk_choice)
        if image_path:
            target_image = cv2.imread(image_path)
            result = cv2.matchTemplate(top_half, target_image, cv2.TM_CCOEFF_NORMED)
            loc = np.where(result >= threshold)
            if len(loc[0]) > 0 and len(loc[1]) > 0:
                center_x = int(loc[1][0] + target_image.shape[1] / 2)
                center_y = int(loc[0][0] + target_image.shape[0] / 2)
                center = (center_x, center_y)
                click_image_center(target_image, center, x, y)
                pyautogui.click(x + 465, y + 108)
                return

    # No images found, click on x + 465, y + 108 and set perks_enabled to False
    pyautogui.click(x + 465, y + 108)
    perks_enabled = False

def perform_action(x, y, action_name, result_max_val, result_max_loc):
    if result_max_val < threshold:
        return
    
    if action_name == 'claim1' or action_name == 'tor_claim' or action_name == 'tor_end' or action_name == 'tor_next' or action_name == 'claim2':
        click_image_center(target_images[action_name], result_max_loc, x, y)
        print("__*** Non regular button pressed ***__" * 1)
        print(action_name, "\n")
        main_cycle()
        return

    if action_name == 'health_upgrade':
        click_image_center(target_images[action_name], result_max_loc, x+130, y)
        return
    
    if action_name == 'damage_upgrade':
        click_image_center(target_images[action_name], result_max_loc, x+130, y)
        return
    
    if action_name == 'retry_game' or action_name == 'start_game':
        click_image_center(target_images[action_name], result_max_loc, x, y)
        if defence_build == True:
            click_defence_icon(x, y)
        global perks_enabled
        perks_enabled = True
        main_cycle()
        return
    
    if action_name == 'new_perk':
        if perks_enabled == True:
            click_image_center(target_images[action_name], result_max_loc, x, y)
            perks()
        return

    click_image_center(target_images[action_name], result_max_loc, x, y)
    return

# Function to take a screenshot of the window
def take_screenshot(x, y, w, h):
    screenshot = np.array(pyautogui.screenshot(region=(x, y, w, h)))
    screenshot_rgb = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot_rgb

# Define the main loop
def main_cycle():
    # Get the Bluestacks window's position and size
    bluestacks = gw.getWindowsWithTitle("Bluestacks")[0]
    x, y, w, h = bluestacks.left, bluestacks.top, bluestacks.width, bluestacks.height
    if bluestacks.height != 990:
        print("*** WINDOW WRONG SIZE *** - PLEASE ENSURE THE WINDOW HAS A HEIGHT OF 990 - Use Window Size.py to see window size and adjust\n" * 3)
    
    # Take a screenshot of the window
    screenshot = take_screenshot(x, y, w, h)

    # Perform template matching to find the target images
    results = {}
    for name, target_image in target_images.items():
        results[name] = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)

    # Get the positions of the best matches and perform the corresponding action
    for name, result in results.items():
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        perform_action(x, y, name, max_val, max_loc)

# Run the main loop
while True:
    main_cycle()
    time.sleep(20)
