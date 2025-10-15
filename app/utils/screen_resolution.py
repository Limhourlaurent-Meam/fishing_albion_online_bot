import win32gui

def find_window_by_title(title_substring: str):
    """Find the first top-level window containing title_substring."""
    title_substring = title_substring.lower()
    hwnd_found = None

    def callback(hwnd, extra):
        nonlocal hwnd_found
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title_substring in title.lower():
                hwnd_found = hwnd
                return False  # stop enumeration

    win32gui.EnumWindows(callback, None)
    return hwnd_found

def get_window_rect(hwnd):
    """Return (left, top, right, bottom)."""
    return win32gui.GetWindowRect(hwnd)



# Example usage
if __name__ == "__main__":
    # e.g. look for Windows Explorer with “Downloads” in the title
    hwnd = find_window_by_title("downloads")

    if hwnd:
        l, t, r, b = get_window_rect(hwnd)
        print(f"Found window: '{win32gui.GetWindowText(hwnd)}'")
        print(f"Position: ({l}, {t})  Size: {r - l}x{b - t}")
    else:
        print("Window not found.")
