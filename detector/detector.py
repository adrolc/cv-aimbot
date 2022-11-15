import torch
import cv2
import numpy as np
from mss import mss
import config

class Detector:
    def __init__(self):
        self.cfg = config.Config("detector.cfg")
        self.model = torch.hub.load(
            repo_or_dir=self.cfg['repo_or_dir'],
            model=self.cfg['model'],
            path=self.cfg['path'],
            source=self.cfg['source']
        )
    
        print("CUDA available: ", torch.cuda.is_available())
    
    def detect_img(self, img_path, save=False):
        obj = self.model(img_path)
        obj.show()
        if save:
            obj.save()


    def run_irt(self):
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
                    xmin = int(df.iloc[0, 0])
                    ymin = int(df.iloc[0, 1])
                    xmax = int(df.iloc[0, 2])
                    ymax = int(df.iloc[0, 3])
                    obj_class = df.iloc[0, 5]

                    color = (255, 0, 0) if obj_class == 0 else (0, 0, 255)

                    cv2.rectangle(screenshot, (xmin, ymin), (xmax, ymax), color, 2)
                except:
                    pass

                cv2.imshow("frame", screenshot)
                if cv2.waitKey(1) == ord('q'):
                    cv2.destroyAllWindows()
                    break


if __name__ == "__main__":
    detector = Detector()
    # gm.run_irt()
    detector.detect_img("3.jpg")