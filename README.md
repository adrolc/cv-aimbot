## Description

Aimbot using computer vision for object detection on the screen and Arduino Leonardo for mouse emulation.

### Built with

* Python3
* YOLOv5
* Arduino Leonardo

## Preview

![alt text](docs/aim_ard.gif "")
![alt text](docs/aim.gif "") 

## Installation

1. Clone the repo:
   ```sh
   git clone https://github.com/adrolc/cv-aimbot.git
   ```
2. Create a venv inside the project and activate it:
    ```sh
    python -m venv .venv
    ```
    ```sh
    .venv\script\activate
    ```
3. Install [PyTorch](https://pytorch.org/get-started/locally/)
4. Download [YOLOv5](https://github.com/ultralytics/yolov5/archive/refs/heads/master.zip), extract in the project and rename the folder to yolov5
5. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
    ```sh
    pip install -r yolov5\requirements.txt
    ```

## Usage

1. Upload `mouse/mouse.ino` to arduino leonardo
2. Set the port and baudrate in `aimbot/aimbot.cfg`
3. Connect arduino leonardo via usb to pc
4. Run aimbot:
    ```sh
    py aimbot.py
    ```
5. Press `v` to calculate the distance of the detected target and shoot