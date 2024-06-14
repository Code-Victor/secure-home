# Secure Home

## Description

an object detection system that utilizes cameras placed at home entrances to detect and alert homeowners about human presence in a designated security zone.

## Features

- Real-time human detection using camera feeds
- Customizable security zones based on camera placement
- Instant notifications on intrusion
- Visual monitoring interface

## Installation

1. Clone the repository
2. Install the required dependencies. Note: this project uses [pdm](https://pdm-project.org/) for dependency management.

    ```bash
    pdm install
    ```

3. Run the application

    ```bash
    pdm run ./src/secure_home
    ```

## Usage

This project uses a CLI interface for now. You can interact with the system using the commands provided.

1. Initialize the system by running the `init` command. This will setup your configuration file.

    ```bash
    pdm run ./src/secure_home init
    ```

    > To reinitialize the system, you can run the `init` command with the `--reset` flag.
2. Start the surveillance system by running the `start` command.

    ```bash
    pdm run ./src/secure_home start
    ```
