from utils.screen_resolution import find_window_by_title, get_window_rect
import win32gui
from utils.templates_loading import loadTemplates
from utils.preprocessing import imageProcessing
import numpy as np
from PIL import ImageGrab, Image
from utils.minigame import recordScreenBoxFromPoint, play_fishing_minigame
from utils.casting import set_cast_position, cast_from_center, set_target_window, send_virtual_click
import time
import cv2
import random
import pyautogui

# Example usage
if __name__ == "__main__":

    window = "Downloads - File Explorer"
    # e.g. look for Windows Explorer with "Downloads" in the title
    hwnd = find_window_by_title(window)

    if hwnd:
        l, t, r, b = get_window_rect(hwnd)

        print(f"Found window: '{win32gui.GetWindowText(hwnd)}'")
        print(f"Position: ({l}, {t})  Size: {r - l}x{b - t}")

    else:
        print("Window not found.")

    # Set the target window name before anything else
    set_target_window(window)  # Set the window name here

    # Load templates for minigame
    templates = loadTemplates("./app/data/bobber", scale=0.8)
    # Assuming loadTemplates returns a list, take the first template
    template = templates[0] if isinstance(templates, list) else templates
    w, h = template.shape[::-1] if hasattr(template, 'shape') else (50, 50)  # Default size

    windowWidth = r - l
    windowHeigth = b - t
    barArea = 0.1
    threshold = 0.8

    minigameBar = imageProcessing(recordScreenBoxFromPoint(
        windowWidth / 2, windowHeigth / 2, windowWidth * barArea, windowHeigth * barArea))
    print(minigameBar.shape[::-1])
    minigameBarWidth = minigameBar.shape[::-1][0]
    print(minigameBarWidth)

    # Set cast position once at the beginning
    print("Setting up fishing bot...")
    cast_position = set_cast_position()
    
    time.sleep(2)

    """ MAIN """
    while (True):
        """ Quit if pressed Q key """
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break
        
        """ Starting fishing with distance-based casting """
        cast_from_center(windowWidth, windowHeigth)
        
        """ Fish bite detection """
        print("Waiting for fish bite...")
        count = 0
        sum_val = 0
        average = 0
        lastAverageImg = 0

        # Use the cast_position for detection
        detection_x, detection_y = cast_position[0], cast_position[1]

        # Create a larger window that stays open
        cv2.namedWindow("Bite Detection", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Bite Detection", 400, 400)
        cv2.moveWindow("Bite Detection", 100, 100)

        bite_detected = False
        while True:
            # Use the cast position for detection
            img = recordScreenBoxFromPoint(detection_x, detection_y, 70, 70)
            img = imageProcessing(img)
            img = cv2.Canny(img, threshold1=60, threshold2=80)
            averageImg = np.average(img)
            count = count + 1
            sum_val = sum_val + averageImg
            average = sum_val / count
            
            # Resize the image to make it bigger for display
            display_img = cv2.resize(img, (400, 400), interpolation=cv2.INTER_NEAREST)
            
            # Add detection info on the image
            cv2.putText(display_img, f"Frame: {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(display_img, f"Intensity: {averageImg:.1f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            if count >= 15:
                ratio = np.abs(averageImg/average)/np.abs(lastAverageImg/average)
                cv2.putText(display_img, f"Ratio: {ratio:.2f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                print(f"Detection ratio: {ratio:.2f}")
                
                if ratio >= 1.3:
                    cv2.putText(display_img, "BITE DETECTED!", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    print("Fish bite detected! Hooking fish...")
                    cv2.imshow("Bite Detection", display_img)
                    cv2.waitKey(1)
                    time.sleep(0.1 + random.random())
                    # Use virtual click to hook the fish
                    send_virtual_click(detection_x, detection_y, hold_time=0.01)
                    bite_detected = True
                    break
            
            cv2.imshow("Bite Detection", display_img)
            cv2.waitKey(1)
            
            lastAverageImg = averageImg
            
            # Check for quit during detection
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
                
            time.sleep(0.05)

        # Close bite detection window
        cv2.destroyWindow("Bite Detection")
        
        if bite_detected:
            """ Fishing minigame """
            play_fishing_minigame(
                windowWidth=windowWidth,
                windowHeigth=windowHeigth,
                barArea=barArea,
                template=template,
                threshold=threshold,
                minigameBarWidth=minigameBarWidth,
                w=w,
                h=h
            )
        
        print("Waiting before next cast...")
        time.sleep(2)  # Wait before next fishing attempt

cv2.destroyAllWindows()