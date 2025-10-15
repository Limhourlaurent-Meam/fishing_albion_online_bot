import cv2
import time
import pyautogui
from PIL import ImageGrab
import numpy as np

def now():
    return time.time() * 1000.0

def recordScreenBoxFromPoint(x, y, width, height):
    """Take screenshot centered at point (x, y)"""
    left = x - width / 2
    top = y - height / 2
    right = x + width / 2
    bottom = y + height / 2
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    return np.array(screenshot)

def imageProcessing(image):
    """Convert image to grayscale"""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def play_fishing_minigame(windowWidth, windowHeigth, barArea, template, threshold, minigameBarWidth, w, h):
    """
    Play the fishing minigame
    
    Args:
        windowWidth: Width of the game window
        windowHeigth: Height of the game window  
        barArea: Percentage of screen for minigame bar (0.1 = 10%)
        template: Template image for bobber detection
        threshold: Match threshold for template matching
        minigameBarWidth: Width of the minigame bar
        w, h: Width and height of the template
    """
    print("Starting fishing minigame...")
    
    # Calculate minigame area based on window size
    minigame_width = int(windowWidth * barArea)
    minigame_height = int(windowHeigth * barArea)
    
    # Create minigame window
    cv2.namedWindow("Fishing Minigame", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Fishing Minigame", 600, 400)
    
    time_last = now()
    while (now() - time_last <= 5000):  # 5 second minigame duration (extended for testing)
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break
            
        # Capture minigame bar area (centered in window)
        img = recordScreenBoxFromPoint(
            windowWidth / 2, 
            windowHeigth / 2 + 60, 
            minigame_width, 
            minigame_height
        )
        img_gray = imageProcessing(img)
        
        # Find bobber position using template matching
        result = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        
        bobber_found = False
        for pt in zip(*loc[::-1]):
            bobber_found = True
            time_last = now()  # Reset timer when bobber is found
            
            # Draw rectangle around detected bobber
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            
            # Calculate bobber position as percentage of bar width
            bobber_position = pt[0] / minigameBarWidth
            
            # Draw minigame bar and safe zone
            cv2.rectangle(img, (0, 0), (minigameBarWidth, img.shape[0]), (255, 255, 255), 1)
            safe_zone_boundary = int(0.65 * minigameBarWidth)
            cv2.line(img, (safe_zone_boundary, 0), (safe_zone_boundary, img.shape[0]), (0, 255, 0), 2)
            
            # Add position info
            cv2.putText(img, f"Position: {bobber_position:.2f}", (10, 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Control mouse based on bobber position
            if bobber_position < 0.65:  # Bobber in left 65% of bar (safe zone)
                pyautogui.mouseDown(button='left')
                cv2.putText(img, "HOLDING", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            else:  # Bobber in right 35% of bar (danger zone)
                pyautogui.mouseUp(button='left')
                cv2.putText(img, "RELEASED", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        if not bobber_found:
            pyautogui.mouseUp(button='left')
            cv2.putText(img, "BOBBER NOT FOUND", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        # Resize for better display
        display_img = cv2.resize(img, (600, 400), interpolation=cv2.INTER_NEAREST)
        cv2.imshow("Fishing Minigame", display_img)
        time.sleep(0.02)
    
    print("Finished minigame")
    pyautogui.mouseUp(button='left')  # Ensure mouse is released
    cv2.destroyWindow("Fishing Minigame")