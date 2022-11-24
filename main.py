# Library includes 
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
from ObjectDectection import Detection
import matplotlib.pyplot as plt
import numpy as np
import cv2
import streamlit as st

# Class deleclartion for Video Transformer 
class VideoTransformer(VideoTransformerBase):

    # Variable initialization 
    CarCountArray = []

    global DetectionIndex
    global email
    global notification
    
    # Display main image to Streamlit page 
    st.image('Main.png')

    # Selection box to Streamlit page 
    DetectionIndex = st.radio(
        "Select Object to be Detected:",
        ('Person', 'Car'))

    if DetectionIndex == 'Person':
        DetectionIndex = 0
    if DetectionIndex == 'Car':
        DetectionIndex = 2
    
    # Selection box 2 to Streamlit page 
    notification = st.radio(
        "Turn on notification system:",
        ('Yes', 'No'))

    if notification == 'Yes':
        notification = True

        email = st.text_input('Enter your email: ')

    if notification == 'No':
        notification = False

        email = ""

    # Function to apply Object dection over web-cam frames 
    def transform(self, frame):
        
        # Convert Images to Arrat
        img = frame.to_ndarray(format="bgr24")
        
        # Apply Object detection 
        img, Carcount = Detection(img, DetectionIndex, email, notification)
        
        # Write detected image
        cv2.imwrite('Detection.png', img)
        
        # --- Real Time Visualization of Car Count ---
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
        
        #----------------------------------------------
        
        # Join graph and detected images together 
        img1 = cv2.imread('Detection.png')
        img2 = cv2.imread('Graph.png')
        img = np.concatenate((img1, img2), axis=1)

        st.radio(
            "Detection Index",
            ('Person', 'Car'))
        
        # Return image containing object detection overlay and live graph 
        return img
 
webrtc_streamer(key="example", video_processor_factory=VideoTransformer, rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    })

