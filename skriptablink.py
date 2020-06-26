import django
django.setup()

import cv2
import numpy as np
import dlib
from math import hypot
import time
import sys
from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from blog.models import RezultatiTreptanja



from PIL import Image


def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)



def get_blinking_ratio(frame,eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
    ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)

    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    ratio = hor_line_lenght / ver_line_lenght
    return ratio

def startAnalysis():
    user = sys.argv[1]

    font = cv2.FONT_HERSHEY_PLAIN
    total_counter = 0
    cap = cv2.VideoCapture(0)

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detector(gray)
        for face in faces:
            #x, y = face.left(), face.top()
            #x1, y1 = face.right(), face.bottom()
            #cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)

            landmarks = predictor(gray, face)

            left_eye_ratio = get_blinking_ratio(frame,[36, 37, 38, 39, 40, 41], landmarks)
            right_eye_ratio = get_blinking_ratio(frame,[42, 43, 44, 45, 46, 47], landmarks)
            blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2
            #print(blinking_ratio)

            if blinking_ratio > 5.7:
                total_counter = total_counter + 1
                cv2.putText(frame, str(total_counter), (50, 150), font, 7, (255, 0, 0))
                time.sleep(0.5)
                print(total_counter)
                #pil_image = Image.fromarray(gray)
                #pil_image.save(f'aa.jpg')


        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    a = RezultatiTreptanja.objects.all()

    usr = User.objects.get(username = user)
    print('User: ', usr)
    a = RezultatiTreptanja.objects.create(user = usr, number_of_blinks = total_counter)
    a.save()
    print(a)




startAnalysis()