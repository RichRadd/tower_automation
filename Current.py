import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import time

# Define image filenames and threshold
image_files = {
    'retry_game': 'images/retry_game.png',
    'buy_health': 'images/health_upgrade.png',
    'ad_gem': 'images/ad_gem.png',
    'start_game': 'images/start_game.png',
    'claim1': 'images/claim1.png',
    'tor_claim': 'images/tor_claim.png',
    'tor_end': 'images/tor_end.png',
    'tor_next': 'images/tor_next.png'
}
threshold = 0.85

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
    pyautogui.moveTo(x + 520, y + 960, duration=.1)
    pyautogui.click(clicks=1, interval=1)

def perform_action(x, y, action_name, result_max_val, result_max_loc):
    if result_max_val < threshold:
        return
    
    if action_name == 'buy_health':
        click_image_center(target_images[action_name], result_max_loc, x+130, y)
        return
    
    if action_name == 'retry_game' or action_name == 'start_game':
        click_image_center(target_images[action_name], result_max_loc, x, y)
        click_defence_icon(x, y)
        return
    
    if action_name == 'claim1' or action_name == 'tor_claim' or action_name == 'tor_end' or action_name == 'tor_next':
        click_image_center(target_images[action_name], result_max_loc, x, y)
        print("__*** Non Regular button Pressed ***__ \n" * 5)
        return

    click_image_center(target_images[action_name], result_max_loc, x, y)
    return

# Define the main loop
def main_cycle():
    # Get the Bluestacks window's position and size
    bluestacks = gw.getWindowsWithTitle("Bluestacks")[0]
    x, y, w, h = bluestacks.left, bluestacks.top, bluestacks.width, bluestacks.height
    
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
    time.sleep(10)
