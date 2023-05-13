import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import time

# set up the target images and thresholds
retry_game_image = cv2.imread('images/retry_game.png')
buy_health_image = cv2.imread('images/health_upgrade.png')
ad_gem_image = cv2.imread('images/ad_gem.png')
start_game_image = cv2.imread('images/start_game.png')
claim1_image = cv2.imread('images/claim1.png')
tor_claim_image = cv2.imread('images/tor_claim.png')
tor_end_image = cv2.imread('images/tor_end.png')
tor_next_image = cv2.imread('images/tor_next.png')
threshold = 0.85

# find the Bluestacks window
bluestacks = gw.getWindowsWithTitle("Bluestacks")[0]
# get the window's position and size
x, y, w, h = bluestacks.left, bluestacks.top, bluestacks.width, bluestacks.height

def main_cycle(x, y, w, h):
    # take a screenshot of the window
    screenshot = np.array(pyautogui.screenshot(region=(x, y, w, h)))
    screenshot_rgb = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    # perform template matching to find the target images
    retry_result = cv2.matchTemplate(screenshot_rgb, retry_game_image, cv2.TM_CCOEFF_NORMED)
    buy_health_result = cv2.matchTemplate(screenshot_rgb, buy_health_image, cv2.TM_CCOEFF_NORMED)
    ad_gem_result = cv2.matchTemplate(screenshot_rgb, ad_gem_image, cv2.TM_CCOEFF_NORMED)
    start_game_result = cv2.matchTemplate(screenshot_rgb, start_game_image, cv2.TM_CCOEFF_NORMED)
    claim1_result = cv2.matchTemplate(screenshot_rgb, claim1_image, cv2.TM_CCOEFF_NORMED)
    tor_claim_result = cv2.matchTemplate(screenshot_rgb, tor_claim_image, cv2.TM_CCOEFF_NORMED)
    tor_end_result = cv2.matchTemplate(screenshot_rgb, tor_end_image, cv2.TM_CCOEFF_NORMED)
    tor_next_result = cv2.matchTemplate(screenshot_rgb, tor_next_image, cv2.TM_CCOEFF_NORMED)

    # get the positions of the best matches
    retry_min_val, retry_max_val, retry_min_loc, retry_max_loc = cv2.minMaxLoc(retry_result)
    buy_health_min_val, buy_health_max_val, buy_health_min_loc, buy_health_max_loc = cv2.minMaxLoc(buy_health_result)
    ad_gem_min_val, ad_gem_max_val, ad_gem_min_loc, ad_gem_max_loc = cv2.minMaxLoc(ad_gem_result)
    start_game_min_val, start_game_max_val, start_game_min_loc, start_game_max_loc = cv2.minMaxLoc(start_game_result)
    claim1_min_val, claim1_max_val, claim1_min_loc, claim1_max_loc = cv2.minMaxLoc(claim1_result)
    tor_claim_min_val, tor_claim_max_val, tor_claim_min_loc, tor_claim_max_loc = cv2.minMaxLoc(tor_claim_result)
    tor_end_min_val, tor_end_max_val, tor_end_min_loc, tor_end_max_loc = cv2.minMaxLoc(tor_end_result)
    tor_next_min_val, tor_next_max_val, tor_next_min_loc, tor_next_max_loc = cv2.minMaxLoc(tor_next_result)

    retry(retry_max_val, retry_max_loc, x, y)
    buy_health(buy_health_max_val, buy_health_max_loc, x, y)
    click_ad(ad_gem_max_val, ad_gem_max_loc, x, y)
    start_game(start_game_max_val, start_game_max_loc, x, y)
    claim1(start_game_max_val, start_game_max_loc, x, y)
    tor_claim(start_game_max_val, start_game_max_loc, x, y)
    tor_end(start_game_max_val, start_game_max_loc, x, y)
    tor_next(start_game_max_val, start_game_max_loc, x, y)

def click_image_center(img, loc, x, y):
    h, w = img.shape[::-1][:2]
    center_x = loc[0] + w // 2
    center_y = loc[1] + h // 2
    pyautogui.moveTo(x + center_x, y + center_y, duration=.1)
    pyautogui.click(clicks=1, interval=1)

def click_defence_icon():
        pyautogui.moveTo(x + 520, y + 960, duration = .1)
        pyautogui.click(clicks=1, interval=1)

def retry(retry_max_val, retry_max_loc, x, y):
    if retry_max_val >= threshold:
        click_image_center(retry_game_image, retry_max_loc, x, y)
        click_defence_icon()

def buy_health(buy_health_max_val, buy_health_max_loc, x, y):
    if buy_health_max_val >= threshold:
        click_image_center(buy_health_image, buy_health_max_loc, x + 130, y)

def click_ad(ad_gem_max_val, ad_gem_max_loc, x, y):
    if ad_gem_max_val >= threshold:
        click_image_center(ad_gem_image, ad_gem_max_loc, x, y)

def start_game(start_game_max_val, start_game_max_loc, x, y):
    if start_game_max_val >= threshold:
        click_image_center(start_game_image, start_game_max_loc, x, y)
        click_defence_icon()

def claim1(claim1_max_val, claim1_max_loc, x, y):
    if claim1_max_val >= threshold:
        click_image_center(claim1_image, claim1_max_loc, x, y)

def tor_claim(tor_claim_max_val, tor_claim_max_loc, x, y):
    if tor_claim_max_val >= threshold:
        click_image_center(tor_claim_image, tor_claim_max_loc, x, y)

def tor_end(tor_end_max_val, tor_end_max_loc, x, y):
    if tor_end_max_val >= threshold:
        click_image_center(tor_end_image, tor_end_max_loc, x, y)

def tor_next(tor_next_max_val, tor_next_max_loc, x, y):
    if tor_next_max_val >= threshold:
        click_image_center(tor_next_image, tor_next_max_loc, x, y)

while True:
    main_cycle(x, y, w, h)
    time.sleep(10)