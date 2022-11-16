from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
from ObjectDectection import Detection
import matplotlib.pyplot as plt
import numpy as np
import cv2
import streamlit as st

class VideoTransformer(VideoTransformerBase):

    CarCountArray = []
    #Detection_Index = 0

    global DetectionIndex
    global email
    global notification

    st.image('Main.png')

    DetectionIndex = st.radio(
        "Select Object to be Detected:",
        ('Person', 'Car'))

    if DetectionIndex == 'Person':
        DetectionIndex = 0
    if DetectionIndex == 'Car':
        DetectionIndex = 2

    notification = st.radio(
        "Turn on notification system:",
        ('Yes', 'No'))

    if notification == 'Yes':
        notification = True

        email = st.text_input('Enter your email: ')

    if notification == 'No':
        notification = False

        email = ""


    def transform(self, frame):

        img = frame.to_ndarray(format="bgr24")

        img, Carcount = Detection(img, DetectionIndex, email, notification)

        cv2.imwrite('Detection.png', img)

        if len(self.CarCountArray) < 10:
            self.CarCountArray.append(Carcount)
        if len(self.CarCountArray) == 10:
            self.CarCountArray.remove(self.CarCountArray[0])

        x = self.CarCountArray
        y = np.sort(self.CarCountArray)

        plt.title("Real Time Detection Count Visualization")
        plt.plot(x, y, color="red")
        plt.savefig('Graph.png')
        plt.clf()

        img1 = cv2.imread('Detection.png')
        img2 = cv2.imread('Graph.png')
        img = np.concatenate((img1, img2), axis=1)

        st.radio(
            "Detection Index",
            ('Person', 'Car'))

        return img

webrtc_streamer(key="example", video_processor_factory=VideoTransformer, rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    })

