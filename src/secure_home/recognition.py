import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime, timedelta

from utils import Config, hex2Scalar,message,send_intruder_alert


def begin(config: Config):
    message("","divider")
    message("Starting surveillance...", "info")
    image_paths = os.listdir(config["image_path"])
    images = []
    user_names = []

    if not image_paths:
        message("No images found in the specified directory. Please add some images and try again.", "error")
        return
    for image_path in image_paths:
        curr_image = cv2.imread(f"{config['image_path']}/{image_path}")
        if curr_image is None:
            message(f"Failed to load image: {image_path}. Skipping...", "warning")
            continue
        images.append(curr_image)
        name, _ext = os.path.splitext(image_path)
        user_names.append(name)
    message(f"Loaded {len(images)} images for recognition.", "info")
    usersEncodings = get_encodings(images)
    video_cap = cv2.VideoCapture(config["camera_id"])
    if not video_cap.isOpened():
        message(f"Failed to open camera (ID: {config['camera_id']}). Please check your camera connection.", "error")
        return

    message("Surveillance is active. Press 'q' to quit.", "info")

    last_alert_time = datetime.min  # Initialize to a time in the past
    unknown_count = 0
    last_detected_name = None

    while True:
        success, img = video_cap.read()
        if not success:
            message("Failed to grab frame from camera. Retrying...", "warning")
            continue
        small_img = scale_down(img)
        # Face location in current frame
        face_locations = face_recognition.face_locations(small_img)
        face_encodings = face_recognition.face_encodings(small_img, face_locations)
        current_detected_names = []
        for location, encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(usersEncodings, encoding)
            face_distances = face_recognition.face_distance(usersEncodings, encoding)
            match_idx = np.argmin(face_distances)
            if matches[match_idx]:
                user_name = user_names[match_idx].capitalize()
                log_detection(user_name)
                unknown_count = 0  # Reset unknown count when a known face is detected
            else:
                user_name = "Unknown"
                unknown_count += 1
                log_detection(user_name)
            current_detected_names.append(user_name)
            location = tuple(map(lambda x: x * 4, location))
            show_bounding_box(img, location, user_name, recognized=(user_name != "Unknown"))
            log_detection(user_name)
            # Check if we should send an alert
            if "Unknown" in current_detected_names:
                if unknown_count >= config[
                    "unknown_threshold"
                ] and datetime.now() - last_alert_time > timedelta(
                    seconds=config["alert_cooldown"]
                ):
                    message("Sending intruder alert...", "warning")
                    alert_status = send_intruder_alert(config["alert_phone_number"])
                    message(f"Alert sent. Status: {alert_status}", "info")
                    last_alert_time = datetime.now()
                    unknown_count = 0  # Reset the count after sending an alert
            # If no faces are detected, or all detected faces are known, reset the unknown count
            if not current_detected_names or "Unknown" not in current_detected_names:
                unknown_count = 0

        cv2.imshow("Surveillance", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    video_cap.release()
    cv2.destroyAllWindows()
    message("Surveillance ended.", "info")

    pass


def get_encodings(images: list):
    message("Encoding known faces...", "info")
    encodeList = []
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(image)[0]
        encodeList.append(encode)
    message("Encoding successfull","success")
    return encodeList


def scale_down(img):
    # Resize to 1/4 of the original size
    return cv2.cvtColor(cv2.resize(img, (0, 0), None, 0.25, 0.25), cv2.COLOR_BGR2RGB)


def scale_up(img):
    pass


def show_bounding_box(img, location: tuple, name: str, recognized: bool = True):
    y1, x2, y2, x1 = location
    color = hex2Scalar("#00FF00") if recognized else hex2Scalar("#FF0000")
    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), color, cv2.FILLED)
    cv2.putText(
        img,
        name,
        (x1 + 6, y2 - 6),
        cv2.FONT_HERSHEY_COMPLEX,
        0.8,
        hex2Scalar("#FFFFFF"),
        2,
    )


def log_detection(name: str):
    with open("detections.log", "a") as log_file:
        log_file.write(f"{datetime.now()} - Detected: {name}\n")
