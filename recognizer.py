import cv2
import sqlite3
import os
import asyncio
import websockets
import base64

async def ___main___():
    async with websockets.connect(
            'ws://localhost:8000') as websocket:
        connection = sqlite3.connect('database.db')
        query = connection.cursor()
        dataset = "data/model.yml"
        if not os.path.isfile(dataset):
            print("run python trainer.py first")
            exit(0)

        frontal = cv2.CascadeClassifier('module/haarcascade_frontalface_default.xml')
        profile = cv2.CascadeClassifier('module/haarcascade_profileface.xml')

        cap = cv2.VideoCapture(1)
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(dataset)

        while True:
            ret, img = cap.read()
            img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = frontal.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
                query.execute("SELECT name FROM users WHERE id = (?);", (id,))
                result = query.fetchall()
                print(u'A person named ' + str(result[0][0]) + ' detected with confidence ' + str(round(confidence,2)) )
                name = ''

                try:
                    name = str(result[0][0]) + ' ' + str(round(confidence, 2))
                except IndexError:
                    name = 'Person'

                if confidence > 100:
                    name = 'Person'
                    cv2.putText(img, name, (x+2, y+h-5), cv2.FONT_HERSHEY_DUPLEX, 0.4, (0, 0, 255), 1)
                else:
                    cv2.putText(img, name, (x+2, y+h-5), cv2.FONT_HERSHEY_DUPLEX, 0.4, (150, 255, 0), 1)

            encoded, buffer = cv2.imencode('.jpg', img)
            jpg_as_text = base64.b64encode(buffer)
            await websocket.send(jpg_as_text)

            cv2.imshow('Face Recognizer', img)
            cv2.waitKey(30) & 0xff
        cap.release()
        cv2.destroyAllWindows()

asyncio.get_event_loop().run_until_complete(___main___())
asyncio.get_event_loop().run_forever()
