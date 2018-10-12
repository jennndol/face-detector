import cv2
import numpy as np
import sqlite3
import os
from datetime import datetime

connection = sqlite3.connect('database.db')
if not os.path.exists('./dataset'):
    os.makedirs('./dataset')

query = connection.cursor()
face_cascade = cv2.CascadeClassifier('module/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
name = input("Name: ")
query.execute('SELECT * FROM users WHERE name = (?)', (name,))
result = query.fetchall()

if(len(result) > 0):
    uid = result[len(result)-1][0]
else:
    query.execute('INSERT INTO users (name) VALUES (?)', (name,))
    uid = query.lastrowid

counter = 0
while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        counter = counter+1
        cv2.imwrite("dataset/User."+str(uid)+"."+str(datetime.now())+".jpg", gray[y:y+h, x:x+w])
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.waitKey(100)
    cv2.imshow('img', img)
    cv2.waitKey(1)
    if counter > 4:
        break

cap.release()
connection.commit()
connection.close()
cv2.destroyAllWindows()
