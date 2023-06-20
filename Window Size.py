import pygetwindow
import time

while True:
    # Find the Bluestacks window with a partial match on the application name
    bluestacks_window = pygetwindow.getWindowsWithTitle("Bluestacks")[0]

    # Get the size of the Bluestacks window
    window_size = bluestacks_window.size

    # Print the window size
    print("Window size:", window_size)
    time.sleep(0.5)

