import pygetwindow as gw

def resize_window(window, width, height):
    window.resizeTo(width, height)

def find_and_resize_window(partial_title, width, height):
    windows = gw.getWindowsWithTitle(partial_title)

    if len(windows) == 0:
        print("No window found with the given title.")
    elif len(windows) > 1:
        print("Multiple windows found with the given title.")
    else:
        window = windows[0]
        original_size = (window.width, window.height)
        resize_window(window, width, height)
        resized_size = (window.width, window.height)

        if resized_size == (width, height):
            print("Window resized successfully.")
        else:
            print("Failed to resize the window.")

            # Revert the window size back to the original
            resize_window(window, original_size[0], original_size[1])

# Specify the partial title of the window and the desired size
partial_title = "BlueStacks"
width = 890
height = 990

find_and_resize_window(partial_title, width, height)
