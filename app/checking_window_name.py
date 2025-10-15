import win32gui

def list_all_windows():
    """List all visible windows to find the exact title"""
    windows = []
    
    def enum_windows_proc(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:  # Only include windows with titles
                windows.append((title, hwnd))
        return True
    
    win32gui.EnumWindows(enum_windows_proc, None)
    return windows

print("=== ALL WINDOW TITLES ===")
all_windows = list_all_windows()
for i, (title, hwnd) in enumerate(all_windows):
    print(f"{i+1}. '{title}'")
print("=========================")