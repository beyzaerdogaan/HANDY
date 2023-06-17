import cv2
import numpy as np
import HandDetector as htm
import time
import autopy
from pynput.mouse import Button, Controller
import pyautogui
from hand import Hand
from database_config import connect_to_database, insert_dictionary, delete_first_row, fetch_dictionaries

##########################
wCam, hCam = 700, 500
frameR = 100  # Frame Reduction
smoothening = 7
#########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.HandDetector(max_hands=1)
wScr, hScr = autopy.screen.size()

connection = connect_to_database("handy_schema")
functions_dict = fetch_dictionaries(connection)

gestures = {
    "moving": Hand("moving", [0, 1, 0, 0, 0], 0, 0, "Right"),
    "right_wolf": Hand("click", [0, 1, 0, 0, 1], 0, 0, "Right"),
    "right_metal": Hand("double_click", [1, 1, 0, 0, 1], 0, 0, "Right"),
    "right_gun_finger": Hand("right_click", [0, 1, 1, 0, 0], 0, 40, "Right"),
    "right_scout": Hand("scroll", [0, 1, 1, 1, 0], 0, 0, "Right"),
    "right_thumbs_up": Hand("", [1, 0, 0, 0, 0], 0, 0, "Right"),
    "right_ok": Hand("drag_and_drop", [1, 1, 0, 0, 0], 0, 65, "Right"),
    "left_wolf": Hand("paste", [0, 1, 0, 0, 1], 0, 0, "Left"),
    "left_gun_finger": Hand("copy", [0, 1, 1, 0, 0], 0, 50, "Left"),
    "left_scissors": Hand("cut", [0, 1, 1, 0, 0], 50, 1000, "Left"),
    "left_metal": Hand("", [1, 1, 0, 0, 1], 0, 0, "Left"),
    "left_scout": Hand("", [0, 1, 1, 1, 0], 0, 0, "Left"),
    "left_thumbs_up": Hand("exit_handy", [1, 0, 0, 0, 0], 0, 0, "Left")
}

cooldown_duration = 2  # Specify the cooldown duration in seconds
last_action_time_cut = 0  # Variable to store the timestamp of the last action
last_action_time_copy = 0
last_action_time_paste = 0

while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.find_hands(img)
    lmList, bbox = detector.find_position(img)

    label = ""
    if len(lmList) != 0:
        label = detector.find_hand_label(img)
        print(label)

    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

    # 3. Check which fingers are up
    fingers = detector.fingers_up(label)

    print(fingers)

    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                  (255, 0, 255), 2)

    # 4. Only Index Finger : Moving Mode
    hand = gestures.get("moving")
    if fingers == hand.fingers and label == hand.label:
        # 5. Convert Coordinates
        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
        # 6. Smoothen Values
        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening

        # 7. Move Mouse
        autopy.mouse.move(wScr - clocX, clocY)
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        plocX, plocY = clocX, clocY

    # 8. Both Index and pinky fingers are up : Clicking Mode
    movement = functions_dict.get("Left Click")
    hand = gestures.get(movement)
    if fingers == hand.fingers and label == hand.label:
        # 9. Find distance between fingers
        length, img, lineInfo = detector.find_distance(8, 12, img)
        print(length)

        cv2.circle(img, (lineInfo[4], lineInfo[5]),
                       15, (0, 255, 0), cv2.FILLED)
        autopy.mouse.click()
        time.sleep(0.3)

    # 10. Thumb, Index and pinky fingers are up : Double Clicking Mode
    movement = functions_dict.get("Double Click")
    hand = gestures.get(movement)
    if fingers == hand.fingers and label == hand.label:
        pyautogui.doubleClick()
        time.sleep(0.3)

    movement = functions_dict.get("Right Click")
    hand = gestures.get(movement)
    if fingers == hand.fingers and label == hand.label:
        # 13. Find distance between fingers
        length, img, lineInfo = detector.find_distance(8, 12, img)
        print(length)
        # 13. Click mouse if distance short
        if length < hand.distance_max:
            cv2.circle(img, (lineInfo[4], lineInfo[5]),
                       15, (0, 255, 0), cv2.FILLED)
            autopy.mouse.click(autopy.mouse.Button.RIGHT)

    hand = gestures.get("right_ok")
    if fingers == hand.fingers and label == hand.label:
        length, img, lineInfo = detector.find_distance(4, 8, img)
        print("LENGTH: ", length)
        if length < hand.distance_max:
            autopy.mouse.toggle(down=True)
        else:
            autopy.mouse.toggle(down=False)

    movement = functions_dict.get("Scroll")
    hand = gestures.get(movement)
    if fingers == hand.fingers and label == hand.label:
        mouse = Controller()
        mouse.scroll(0, -1)

    # Paste
    movement = functions_dict.get("Paste")
    hand = gestures.get(movement)
    if fingers == hand.fingers and label == hand.label:
        current_time = time.time()
        time_since_last_action = current_time - last_action_time_paste
        if time_since_last_action >= cooldown_duration:
            pyautogui.hotkey('ctrl', 'v')
            last_action_time_paste = current_time

    # Cut
    movement = functions_dict.get("Cut")
    hand = gestures.get(movement)
    if fingers == hand.fingers and label == hand.label:
        current_time = time.time()
        time_since_last_action = current_time - last_action_time_cut
        if time_since_last_action >= cooldown_duration:
            length, img, lineInfo = detector.find_distance(8, 12, img)
            print(length)
            if length > hand.distance_min:
                pyautogui.hotkey('ctrl', 'x')
                last_action_time_cut = current_time

    # Copy
    movement = functions_dict.get("Copy")
    hand = gestures.get(movement)
    if fingers == hand.fingers and label == hand.label:
        current_time = time.time()
        time_since_last_action = current_time - last_action_time_copy
        if time_since_last_action >= cooldown_duration:
            pyautogui.hotkey('ctrl', 'c')
            last_action_time_copy = current_time

    # Exit
    hand = gestures.get("left_metal")
    if fingers == hand.fingers and label == hand.label:
        break

    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)

cv2.destroyAllWindows()
cap.release()