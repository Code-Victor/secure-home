import os
import json
import cv2
from typing import Literal, TypedDict
from colorama import Fore, Back, Style, init
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
# Initialize colorama for Windows support
init(autoreset=True)

client = Client(TWILIO_SID, TWILIIO_AUTH_TOKEN)


class Config(TypedDict):
    camera_id: int
    image_path: str
    alert_phone_number: str  # The phone number to send alerts to
    alert_cooldown: (
        int  # Time in seconds before sending another alert (e.g., 5 minutes)
    )
    unknown_threshold: (
        int  # Number of consecutive unknown detections before sending an alert
    )


def hex2Scalar(hex: str):
    """Converts a hex string to a scalar value.

    Args:
        hex (str): The hex string to convert.

    Returns:
        tuple(int,int,int): The scalar value of color.
    """
    return tuple(int(hex[i : i + 2], 16) for i in (1, 3, 5))


def list_camera_ports():
    """
    Test the ports and returns a list of available camera.
    """
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            arr.append(index)
        cap.release()
        index += 1
    return arr


def check_camera_port(port: int):
    """
    Check if the camera port is available
    """
    cap = cv2.VideoCapture(port)
    if cap.read()[0]:
        cap.release()
        return True
    return False


def record_face(name: str, camera_id: int):
    """
    OPen camera with the name,and camera id. If a face is found or spacebar is pressed, the face is recorded and saved to ./image/{name} directory.
    """
    cap = cv2.VideoCapture(camera_id)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord(" "):
            cv2.imwrite(f"./image/{name}.png", frame)
            break
    cap.release()
    cv2.destroyAllWindows()


CENTER_SPACING = 60


def message(
    msg: str,
    type: Literal[
        "title", "regular", "info", "error", "success", "warning", "divider"
    ] = "regular",
):
    """
    Display a message to the user in a well-formatted and colorful way.
    """

    spaced_msg = msg.center(CENTER_SPACING, " ")
    if type == "title":
        print(f"\n{Back.BLUE}{Fore.WHITE} {spaced_msg} {Style.RESET_ALL}")
        print(f"{Fore.BLUE}{'-' * (CENTER_SPACING)}{Style.RESET_ALL}\n")
    if type == "regular":
        print(f"{Fore.WHITE}{msg}{Style.RESET_ALL}")
    elif type == "info":
        print(f"{Fore.CYAN}ℹ  {msg}{Style.RESET_ALL}")
    elif type == "error":
        print(f"{Fore.RED}✖  Error: {msg}{Style.RESET_ALL}")
    elif type == "success":
        print(f"{Fore.GREEN}✔  Success: {msg}{Style.RESET_ALL}")
    elif type == "warning":
        print(f"{Fore.YELLOW}⚠  Warning: {msg}{Style.RESET_ALL}")
    elif type == "divider":
        print(f"{Fore.BLUE}{'-' * (CENTER_SPACING)}{Style.RESET_ALL}\n")


def save_config(config: Config):
    """
    Save the configuration to a file.
    """
    with open("config.json", "w") as f:
        f.write(json.dumps(config, indent=4))


def load_config() -> Config | None:
    """
    Load the configuration from a file.
    """
    try:
        with open("config.json", "r") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return None


def send_intruder_alert(user_number: str):
    try:
        m = client.messages.create(
            body="Intruder Alert! Someone is trying to break into your house.",
            from_=TWILIO_PHONE_NUMBER,
            to=user_number,
        )
        return m.status
    except Exception as e:
        message(f"Failed to send alert: {e}", "error")
        return "Failed"
