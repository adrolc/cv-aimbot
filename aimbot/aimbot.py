import torch
import cv2
import numpy as np
from mss import mss
import config
import keyboard
import serial
import time

class Aimbot:
    def __init__(self):
        self.cfg = config.Config("aimbot.cfg")
        self.load_model()
        self.setup_serial_connection()
        print("CUDA available: ", torch.cuda.is_available())
    
    def load_model(self):
        """Load the model based on configuration parameters"""
        self.model = torch.hub.load(
            repo_or_dir=self.cfg['repo_or_dir'],
            model=self.cfg['model'],
            path=self.cfg['path'],
            source=self.cfg['source']
        )

    def setup_serial_connection(self):
        """Setup the serial connection for arduino"""
        self.arduino = serial.Serial(self.cfg['arduino_port'],
                                self.cfg['arduino_baudrate'],
                                timeout=0.1)

    def calculate_distance(self, head_center):
        distance = (self.cfg['width'] // 2 - head_center[0], self.cfg['height'] // 2 - head_center[1])
        # 5 is a step. This value must be the same in the Mouse.move function on the arduino.
        # for example: if the distance on the x-axis is 100, then we take a step of 5 units 20 times
        distance = tuple(-(i//5) for i in distance) # reverse sign
        return distance
    
    def send_message(self, distance):
        serial_message = f"{distance[0]},{distance[1]}\n"
        self.arduino.write(str.encode(serial_message))

    def extract_bounding_box(self, df):
        """Extract bounding box and class details from DataFrame"""
        xmin = int(df.iloc[0, 0])
        ymin = int(df.iloc[0, 1])
        xmax = int(df.iloc[0, 2])
        ymax = int(df.iloc[0, 3])
        obj_class = df.iloc[0, 5]

        return xmin, ymin, xmax, ymax, obj_class

    def draw_on_image(self, screenshot, head_center, bounding_box, obj_class):
        """Draw the detected object on the image"""
        xmin, ymin, xmax, ymax = bounding_box
        color = (255, 0, 0) if obj_class == 0 else (0, 0, 255)
        cv2.circle(screenshot, head_center, 5, (0, 255, 0), thickness = -1)
        cv2.rectangle(screenshot, (xmin, ymin), (xmax, ymax), color, 2)
        return screenshot

    def run(self):
        monitor = {
            "top": self.cfg['top'],
            "left": self.cfg['left'],
            "width": self.cfg['width'],
            "height": self.cfg['height'] 
        }
        with mss() as sct:
            while True:
                screenshot = np.array(sct.grab(monitor))
                result = self.model(screenshot)
                df = result.pandas().xyxy[0]
                try:
                    xmin, ymin, xmax, ymax, obj_class = self.extract_bounding_box(df)
                    head_center = (xmin + (xmax-xmin) // 2, ymin + (ymax - ymin) // 2)

                    screenshot = self.draw_on_image(screenshot, head_center, (xmin, ymin, xmax, ymax), obj_class)

                    if keyboard.is_pressed('v'):
                        self.send_message(self.calculate_distance(head_center))
                        time.sleep(0.135)

                except Exception as e:
                    pass
                    # print(e)

                cv2.imshow("frame", screenshot)
                if cv2.waitKey(1) == ord('q'):
                    cv2.destroyAllWindows()
                    break


if __name__ == "__main__":
    aimbot = Aimbot()
    aimbot.run()