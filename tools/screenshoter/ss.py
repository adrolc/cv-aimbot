from PIL import ImageGrab
import cv2
import numpy as np
import keyboard
import time
from pathlib import Path
import config

class Screenshoter:
    def __init__(self, img_size: tuple, window_size: tuple):
        if img_size[0] > window_size[0] or img_size[1] > window_size[1]:
            raise ValueError("Image size cannot be larger than window")

        self.cfg = config.Config("screenshoter.cfg")
        self._img_width, self._img_height = img_size
        self._window_width, self._window_height = window_size
        self.set_position(position="center")

        Path(self.cfg['path']).mkdir(exist_ok=True)

    def valid_size(self, img_size=None, window_size=None):
        window_width, window_height = window_size if window_size else self._window_width, self._window_height
        img_width, img_height = img_size if img_size else self._img_width, self._img_height
        if img_width > window_width or img_height > window_height:
            raise ValueError("Image size cannot be larger than window")
        return True

    @property
    def img_size(self):
        return (self._img_width, self._img_height)
    
    @property
    def window_size(self):
        return (self._window_width, self._window_height)
    
    @img_size.setter
    def img_size(self, size):
        self.valid_size(img_size=size)
        self._img_width, self._img_height = size

    @window_size.setter
    def window_size(self, size):
        self.valid_size(window_size=size)
        self._window_width, self._window_height = size

    @property
    def position(self):
        return self._position
    
    def set_position(self, position: str):
        match position:
            case "center":
                left_x = int((self._window_width - self._img_width) / 2)
                right_x = int(left_x + self._img_width)
                top_y = int((self._window_height - self._img_height) / 2)
                bottom_y = int(top_y + self._img_height)
            
            case "top_left":
                left_x, top_y, right_x, bottom_y = (0, 0, self._img_width, self._img_height)

            case "top_right":
                left_x = self._window_width - self._img_width
                top_y = 0
                right_x = self._window_width
                bottom_y = self._img_height

            case "bottom_left":
                left_x = 0
                top_y = self._window_height - self._img_height
                right_x = self._img_width
                bottom_y = self._window_height

            case "bottom_right":
                left_x = self._window_width - self._img_width
                top_y = self._window_height - self._img_height
                right_x = self._window_width
                bottom_y = self._window_height

            case _:
                raise ValueError(f"Position '{position}' does not exist")
        
        self._position = (left_x, top_y, right_x, bottom_y)

    @property
    def last_image_number(self):
        path = Path(self.cfg['path']).glob("*")
        files = sorted([x for x in path if x.is_file()], key=lambda path: int(path.stem))
        n = int(files[-1].stem) if files else 0
        return n
    
    def align(self):
        path = Path(self.cfg['path']).glob("*")
        files = sorted([x for x in path if x.is_file()], key=lambda path: int(path.stem))
        for n, file in enumerate(files):
            new_name = file.with_name(str(n)).with_suffix(self.cfg['ext'])
            file.rename(new_name)

    def shot(self, filename: str):
        ss = np.array(ImageGrab.grab(bbox=self.position))
        ss = cv2.cvtColor(ss, cv2.COLOR_BGR2RGB)
        filename = filename + self.cfg['ext']
        filename = str(Path(self.cfg['path']) / filename)
        cv2.imwrite(filename, ss)
        print(f"{filename} - saved successfully")
    
    def run(self):
        n = self.last_image_number + 1
        while True:
            if keyboard.is_pressed(self.cfg['bind.shot']):
                self.shot(str(n))
                n += 1
                time.sleep(0.1)
            if keyboard.is_pressed(self.cfg['bind.quit']):
                break
            time.sleep(0.01)


if __name__ == "__main__":
    ss = Screenshoter((640, 640), (1024, 768))
    ss.align()
    print(f"Window: {ss.window_size}")
    print(f"Image: {ss.img_size}")
    print(f"Position: {ss.position}")
    print(f"Image directory: {ss.cfg['path']}")
    print(f"File extension: {ss.cfg['ext']}")
    print(f"\nBinds:\nScreenshot: '{ss.cfg['bind.shot']}'\nQuit: '{ss.cfg['bind.quit']}'")
    ss.run()