import cv2
import keyboard

from cvzone.HandTrackingModule import HandDetector

from button import Button

BUTTON_SIZE = 75
X_OFFSET = 700
Y_OFFSET = 150

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height
detector = HandDetector(detectionCon=0.5, maxHands=1)

# Creating button
button_values_list = [
    ['7', '8', '9', 'x'],
    ['4', '5', '6', '-'],
    ['1', '2', '3', '+'],
    ['0', '/', '.', '='],
]
button_list = []
for x_distance in range(4):  # Since we have 4 x 4 grid
    for y_distance in range(4):
        x_position = x_distance * BUTTON_SIZE + X_OFFSET
        y_position = y_distance * BUTTON_SIZE + Y_OFFSET
        button_list.append(Button(position=(x_position, y_position), width=BUTTON_SIZE, height=BUTTON_SIZE,
                                  value=button_values_list[y_distance][x_distance]))

# Variables
EQUATION = ''
DELAY_COUNTER = 0

# Loop
while True:
    # Get image from webcam
    success, img = cap.read()
    img = cv2.flip(src=img, flipCode=1)

    # Hand detection
    hands, img = detector.findHands(img=img, flipType=False)

    # Draw result
    cv2.rectangle(img=img, pt1=(X_OFFSET, BUTTON_SIZE), pt2=(X_OFFSET + BUTTON_SIZE * 4, Y_OFFSET + BUTTON_SIZE),
                  color=(0, 149, 255), thickness=cv2.FILLED)
    cv2.rectangle(img=img, pt1=(X_OFFSET, BUTTON_SIZE), pt2=(X_OFFSET + BUTTON_SIZE * 4, Y_OFFSET + BUTTON_SIZE),
                  color=(50, 50, 50), thickness=3)

    # Draw all buttons
    for button in button_list:
        button.draw_button(img=img)

    # Check for hand
    if hands:
        lm_list = hands[0]['lmList']  # landmark list
        length, _, img = detector.findDistance(p1=lm_list[8][0:2], p2=lm_list[12][0:2],
                                               img=img)  # 8 - index finger tip, 12 - middle finger tip
        x, y = lm_list[8][0:2]
        if length < 50:
            for i, button in enumerate(button_list):
                if button.check_click(x=x, y=y, img=img) and DELAY_COUNTER == 0:
                    current_value = button_values_list[int(i % 4)][int(i / 4)]
                    if current_value == '=':
                        EQUATION = str(round(eval(EQUATION.replace('x', '*')), 3))
                    else:
                        EQUATION += current_value
                    DELAY_COUNTER = 1

    # Avoid duplicates
    if DELAY_COUNTER != 0:
        DELAY_COUNTER += 1
        if DELAY_COUNTER > 10:
            DELAY_COUNTER = 0

    # Processing

    # Display the Equation/Result
    text_size = cv2.getTextSize(text=EQUATION, fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1.2, thickness=2)
    text_y = int(Y_OFFSET - BUTTON_SIZE / 2 + text_size[1])
    cv2.putText(img=img, text=EQUATION, org=(X_OFFSET + 10, text_y), fontFace=cv2.FONT_HERSHEY_DUPLEX,
                fontScale=1.2, color=(50, 50, 50), thickness=2)

    # Display image
    cv2.imshow(winname='Image', mat=img)
    key = cv2.waitKey(1)
    if key == ord('c'):  # Clear display
        EQUATION = ''

    # Exit
    if keyboard.is_pressed('esc'):
        break

cv2.destroyAllWindows()
