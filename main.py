from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
from ObjectDectection import Detection

class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")

        img = Detection(img)

        return img

webrtc_streamer(key="example", video_processor_factory=VideoTransformer)