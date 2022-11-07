from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
from ObjectDectection import Detection
import matplotlib.pyplot as plt
import numpy as np
import cv2


class VideoTransformer(VideoTransformerBase):

    CarCountArray = []

    def transform(self, frame):

        img = frame.to_ndarray(format="bgr24")

        img, Carcount = Detection(img)

        cv2.imwrite('Detection.png', img)

        if len(self.CarCountArray) < 10:
            self.CarCountArray.append(Carcount)
        if len(self.CarCountArray) == 10:
            self.CarCountArray.remove(self.CarCountArray[0])

        x = self.CarCountArray
        print(x)
        y = np.sort(self.CarCountArray)

        plt.title("Detection Count")
        plt.plot(x, y, color="red")
        plt.savefig('Graph.png')
        plt.clf()

        img1 = cv2.imread('Detection.png')
        img2 = cv2.imread('Graph.png')
        img = np.concatenate((img1, img2), axis=1)

        return img

webrtc_streamer(key="example", video_processor_factory=VideoTransformer, rtc_configuration={  # Add this line
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    })

