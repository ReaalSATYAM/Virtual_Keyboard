import cv2
import pyautogui
from cvzone.HandTrackingModule import HandDetector
from screeninfo import get_monitors
import time
import pygame

pygame.mixer.init()

click_sound = pygame.mixer.Sound("clickSound.mp3")

# ==== Helper Function: Draw Rounded Rectangle ====
def draw_rounded_rect(img, top_left, bottom_right, radius=20, color=(0, 0, 0), thickness=-1):
    x1, y1 = top_left
    x2, y2 = bottom_right
    overlay = img.copy()

    cv2.rectangle(overlay, (x1 + radius, y1), (x2 - radius, y2), color, thickness)
    cv2.rectangle(overlay, (x1, y1 + radius), (x2, y2 - radius), color, thickness)

    cv2.circle(overlay, (x1 + radius, y1 + radius), radius, color, thickness)
    cv2.circle(overlay, (x2 - radius, y1 + radius), radius, color, thickness)
    cv2.circle(overlay, (x1 + radius, y2 - radius), radius, color, thickness)
    cv2.circle(overlay, (x2 - radius, y2 - radius), radius, color, thickness)

    cv2.addWeighted(overlay, 0.8, img, 0.2, 0, img)

# ==== Draw Each Key Button with Rounded Corners and Centered Text ====
def draw(pos, text, highlight=False):
    x, y = pos
    w, h = 90, 90
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    text_color = (255, 255, 255)
    thickness = 4

    key_color = (0, 255, 0) if highlight else (0, 0, 0)
    draw_rounded_rect(img, (x, y), (x + w, y + h), radius=20, color=key_color, thickness=-1)

    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = x + (w - text_size[0]) // 2
    text_y = y + (h + text_size[1]) // 2
    cv2.putText(img, text, (text_x, text_y), font, font_scale, text_color, thickness)

# ==== Screen Info ====
monitors = get_monitors()
screen_width, screen_height = monitors[0].width, monitors[0].height

# ==== Keyboard Layout ====
symbols = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '<-'],
           ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
           ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
           ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '__']]

keys = []
key_width, key_height = 90, 90
gap = 20
start_x, start_y = 50, 100

for row_index, row in enumerate(symbols):
    row_start_x = start_x + row_index * 40
    y = start_y + row_index * (key_width + gap)
    for col_index, key in enumerate(row):
        x = row_start_x + col_index * (key_width + gap)
        keys.append((x, y, key_width, key_height, key))

# ==== Webcam Setup ====
cap = cv2.VideoCapture(1) 
cap.set(3, screen_width * 0.85)
cap.set(4, screen_height * 0.75)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# ==== Initialization ====
detector = HandDetector(detectionCon=0.8)
last_click_time = 0
click_delay = 0.5
typed_text = ""
key_flash = {}
exit = False

while not exit:
    success, img = cap.read()
    if not success:
        print("Failed to capture image")
        break

    hands, img = detector.findHands(img, draw=False)
    current_time = time.time()
    clickRegistered = False

    if hands:
        for hand in hands:
            lmList = hand['lmList']
            bbox = hand['bbox']
            x, y, w, h = bbox
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

            thumb_tip = lmList[4]
            index_tip = lmList[8]
            dist_thumb_index = ((thumb_tip[0] - index_tip[0]) ** 2 + (thumb_tip[1] - index_tip[1]) ** 2) ** 0.5

            # ==== LEFT HAND ====
            if hand['type'] == "Left":
                if dist_thumb_index < 40 and (current_time - last_click_time) > click_delay:
                    clickRegistered = True
                    last_click_time = current_time

                middle_tip = lmList[12]
                dist_thumb_middle = ((thumb_tip[0] - middle_tip[0]) ** 2 + (thumb_tip[1] - middle_tip[1]) ** 2) ** 0.5
                if dist_thumb_middle < 40:
                    exit = True
                    cv2.waitKey(200)
                    break

            # ==== RIGHT HAND ====
            if hand["type"] == "Right":
                tip_x, tip_y = index_tip[0], index_tip[1]
                for x, y, w, h, label in keys:
                    if x < tip_x < x + w and y < tip_y < y + h:
                        draw_rounded_rect(img, (x, y), (x + w, y + h), radius=20, color=(0, 255, 0), thickness=4)
                        if clickRegistered:
                            click_sound.play()# click sound
                            if label == '__':  # Space
                                pyautogui.press('space')
                                typed_text += ' '
                            elif label == '<-':  # Backspace
                                pyautogui.press('backspace')
                                if len(typed_text) > 0:
                                    typed_text = typed_text[:-1]
                            else:  # Regular character
                                pyautogui.press(label.lower())
                                typed_text += label

                            key_flash[label] = current_time
                            clickRegistered = False  # Reset after click

    # ==== Draw Preview Box ====
    draw_rounded_rect(img, (50, 20), (screen_width - 710, 80), radius=20, color=(50, 50, 50), thickness=-1)
    cv2.putText(img, typed_text[-60:], (60, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255, 255, 255), 3)

    # ==== Draw Keyboard ====
    for x, y, _, _, key in keys:
        is_flashing = key in key_flash and current_time - key_flash[key] < 0.3
        draw((x, y), key, highlight=is_flashing)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
