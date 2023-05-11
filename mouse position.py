import pygetwindow
import pyautogui
import time

# Find the Bluestacks window with a partial match on the application name
bluestacks_window = pygetwindow.getWindowsWithTitle("Bluestacks")[0]

# Get the size of the Bluestacks window
window_size = bluestacks_window.size

# Print the window size
print("Window size:", window_size)
time.sleep(5)

while True:
    # Get the current cursor position
    cursor_position = pyautogui.position()

    # Check if the cursor is within the bounds of the Bluestacks window
    if bluestacks_window.left <= cursor_position.x <= bluestacks_window.left + window_size.width and \
            bluestacks_window.top <= cursor_position.y <= bluestacks_window.top + window_size.height:
        # Print the cursor position relative to the Bluestacks window
        cursor_position_rel = (cursor_position.x - bluestacks_window.left, cursor_position.y - bluestacks_window.top)
        print("Cursor position relative to window:", cursor_position_rel)
        time.sleep(1)
    else:
        print("Cursor is not within the bounds of the window.")
        time.sleep(1)
