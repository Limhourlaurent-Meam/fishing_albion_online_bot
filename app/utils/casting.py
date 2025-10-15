import math
import time
import pyautogui
import cv2
import ctypes
import ctypes.wintypes
import win32gui
import win32con

# Global variables
cast_position = None
target_window_name = "Downloads"  # Default window name

def set_cast_position():
    """Let user set the cast position by clicking"""
    global cast_position
    print("Click on the screen where you want to cast the fishing rod...")
    input("Press ENTER after clicking...")
    
    cast_position = pyautogui.position()
    print(f"Cast position set to: ({cast_position[0]}, {cast_position[1]})")
    return cast_position

def set_target_window(window_name):
    """Set the target window name - call this from main.py"""
    global target_window_name
    target_window_name = window_name
    print(f"Target window set to: {target_window_name}")

def calculate_cast_time(distance, min_time=0.3, max_time=1.2, max_distance=500):
    """Faster casting with exponential curve"""
    distance = max(distance, 1.0)
    normalized_distance = min(distance / max_distance, 1.0)
    hold_time = min_time + (max_time - min_time) * (normalized_distance ** 0.5)
    return min(hold_time, max_time)

def send_virtual_click(x, y, hold_time=0.01):
    """Send virtual mouse click to specific position without moving physical cursor"""
    global target_window_name
    
    # Try to find the window by title directly
    hwnd = win32gui.FindWindow(None, target_window_name)
    if not hwnd:
        print(f"'{target_window_name}' window not found! Trying alternative method...")
        # Get the foreground window (active window)
        hwnd = win32gui.GetForegroundWindow()
        if not hwnd:
            print("No active window found!")
            return False
    
    # Bring window to foreground
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.1)
        
        # Get window position
        rect = win32gui.GetWindowRect(hwnd)
        window_x, window_y = rect[0], rect[1]
        
        # Calculate relative position within window
        rel_x = x - window_x
        rel_y = y - window_y
        
        # Prepare the coordinates for Windows message
        lParam = rel_y << 16 | rel_x
        
        # Send mouse down event
        ctypes.windll.user32.PostMessageW(hwnd, 0x201, 0x0001, lParam)  # WM_LBUTTONDOWN
        time.sleep(hold_time)
        # Send mouse up event
        ctypes.windll.user32.PostMessageW(hwnd, 0x202, 0x0000, lParam)  # WM_LBUTTONUP
        
        print(f"Virtual click sent to ({x}, {y}) - holding for {hold_time:.2f}s")
        return True
    except Exception as e:
        print(f"Error sending virtual click: {e}")
        return False

def cast_from_center(windowWidth, windowHeigth):
    """Cast fishing rod using virtual cursor - doesn't move physical cursor"""
    global cast_position
    
    if cast_position is None:
        print("No cast position set. Setting cast position...")
        set_cast_position()
    
    # Center position
    center_x = windowWidth / 2
    center_y = windowHeigth / 2
    
    # Use the user-set cast position
    target_x, target_y = cast_position
    
    # Calculate distance and hold time
    distance = math.sqrt((target_x - center_x)**2 + (target_y - center_y)**2)
    hold_time = calculate_cast_time(distance)
    
    print(f"Virtual casting to: ({target_x:.0f}, {target_y:.0f}) | Hold: {hold_time:.2f}s")
    
    # Cast using virtual cursor (no physical cursor movement)
    success = send_virtual_click(target_x, target_y, hold_time)
    
    if success:
        print("Virtual cast completed successfully!")
    else:
        print("Virtual cast failed! Falling back to physical cursor...")
        # Fallback to physical method
        original_pos = pyautogui.position()
        pyautogui.moveTo(target_x, target_y)
        time.sleep(0.05)
        pyautogui.mouseDown(button='left')
        time.sleep(hold_time)
        pyautogui.mouseUp(button='left')
        pyautogui.moveTo(original_pos)
        print("Physical cast completed!")