import cv2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

def detect_face():
    cap = cv2.VideoCapture(0)
    found = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            found = True

            # παίρνουμε το πρώτο πρόσωπο
            (x, y, w, h) = faces[0]

            # κέντρο προσώπου
            cx = x + w//2

            # απλό following logic
            frame_center = frame.shape[1] // 2

            if cx < frame_center - 50:
                direction = "left"
            elif cx > frame_center + 50:
                direction = "right"
            else:
                direction = "center"

            cap.release()
            return True, direction

        # ESC για έξοδο
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    return False, None
