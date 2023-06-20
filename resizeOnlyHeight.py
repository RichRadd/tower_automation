import pygetwindow as gw

def resize_window_height(window, height):
    window.resizeTo(window.width, height)

def find_and_resize_window(partial_title, height):
    windows = gw.getWindowsWithTitle(partial_title)

    if len(windows) == 0:
        print("No window found with the given title.")
    elif len(windows) > 1:
        print("Multiple windows found with the given title.")
    else:
        window = windows[0]
        original_size = (window.width, window.height)
        resize_window_height(window, height)
        resized_size = (window.width, window.height)

        if resized_size[1] == height:
            print("Window height adjusted successfully.")
        else:
            print("Failed to adjust the window height.")

            # Revert the window size back to the original
            window.resizeTo(original_size[0], original_size[1])

# Specify the partial title of the window and the desired height
partial_title = "BlueStacks"
height = 990

find_and_resize_window(partial_title, height)
