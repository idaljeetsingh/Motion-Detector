"""
    Title: Motion Detector
    Author: Daljeet Singh Chhabra
    Language: Python
    Date Created: 03-01-2019
    Date Modified: 03-01-2019
"""

import cv2

first_frame = None
video = cv2.VideoCapture(0)

while True:

    check, frame = video.read()

    frame = cv2.flip(frame, 1, 0)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if first_frame is None:
        first_frame = gray
        continue

    delta_frame = cv2.absdiff(first_frame, gray)

    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (_, cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 5)

    cv2.imshow("LIVE", gray)
    cv2.imshow("DELTA FRAME", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
