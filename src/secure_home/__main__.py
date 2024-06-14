import click
from utils import (
    check_camera_port,
    message,
    load_config,
    save_config,
    Config,
)
import os
from recognition import begin

DEFAULT_CONFIG: Config = {
    "camera_id": 0,
    "image_path": "./images",
    "alert_phone_number": "",  
    "alert_cooldown": 300,  
    "unknown_threshold": 3,
}


@click.group()
def cli():
    pass


@cli.command()
@click.option("--reset", is_flag=True, help="Reset the existing configuration.")
def init(reset):

    message("Welcome to Secure Home!!!", "title")
    message(
        """an object detection system that utilizes cameras placed at home entrances 
to detect and alert homeowners about human presence in a designated security zone.
    """
    )

    message(
        """Key Features:\n
- Real-time human detection using camera feeds
- Customizable security zones
- Instant notifications on intrusion
- Visual monitoring interface
"""
    )
    try:
        message("Check for existing configuration...", "info")
        config = load_config()
        if config and not reset:
            message("Existing configuration found. Use --reset to start fresh.", "info")
            return
        config = DEFAULT_CONFIG.copy()
        message("No configuration found, create a new one...", "warning")
        # Getting capture device id
        message("", "divider")
        while True:
            message("Enter the camera ID (usually 0 for built-in webcam): ", "info")
            camera_id = click.prompt("Camera ID", type=int, default=config["camera_id"])

            message("Checking camera port availability...", "info")
            if check_camera_port(camera_id):
                message(f"Camera (ID: {camera_id}) is available!", "success")
                config["camera_id"] = camera_id
                break
            else:
                message(
                    f"Camera (ID: {camera_id}) is not available. Please try a different ID.",
                    "error",
                )

        # Input acceptable faces for recognition(directory)
        message("", "divider")
        while True:
            message("Enter the directory for storing acceptable faces: ", "info")
            acceptable_faces = click.prompt("Directory", default=config["image_path"])
            if not os.path.exists(acceptable_faces):
                create = click.confirm(
                    f"Directory '{acceptable_faces}' does not exist. Create it?",
                    default=True,
                )
                if create:
                    os.makedirs(acceptable_faces)
                    message(f"Created directory: {acceptable_faces}", "success")
                else:
                    continue

            if os.path.isdir(acceptable_faces):
                config["image_path"] = acceptable_faces
                message("Directory confirmed!", "success")
                break
            else:
                message("Invalid directory. Please try again.", "error")
        message("Enter the phone number to receive alerts (with country code, e.g., +1234567890): ", "info")
        config["alert_phone_number"] = click.prompt("Phone Number", default="")

        config["alert_cooldown"] = click.prompt("Alert cooldown (in seconds)", type=int, default=300)
        config["unknown_threshold"] = click.prompt("Number of consecutive unknown detections before alerting", type=int, default=3)
        message("Saving config...", "info")
        save_config(config)
        message("Configuration complete!", "success")

    except Exception as e:
        message(f"An error occurred: {e}", "error")


@cli.command()
def start():
    """Start the Secure Home system."""
    config = load_config()
    if not config:
        message("No configuration found. Please run 'init' first.", "error")
        return

    message("Starting Secure Home system...", "title")
    message(f"Using camera ID: {config['camera_id']}", "info")
    message(f"Acceptable faces directory: {config['image_path']}", "info")
    begin(config)


if __name__ == "__main__":
    cli()
