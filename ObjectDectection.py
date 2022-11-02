# Import necessary libraries
import cv2
import csv
import collections
import numpy as np
import math
import time
import matplotlib.pyplot as plt

# Store Coco Names in a list

classesFile = "coco.names"
classNames = open(classesFile).read().strip().split('\n')

# Detection confidence threshold
confThreshold = 0.1
nmsThreshold = 0.2

# Initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(classNames), 3),
	dtype="uint8")

# Configure the network model
net = cv2.dnn.readNetFromDarknet('yolov4-tiny.cfg', 'yolov4-tiny.weights')

# Configure the network backend
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Define random colour for each classs
np.random.seed(42)
colors = np.random.randint(0, 255, size=(len(classNames), 3), dtype='uint8')

# Function definition to perform detection place bounding boxes over input images & print the number of cars detected
def Detection(img):

  # Load our input image and grab its spatial dimensions
  (Height, Width) = img.shape[:2]
  
  # Determine only the *output* layer names that we need from YOLO
  ln = net.getLayerNames()
  ln = [ln[i-1] for i in net.getUnconnectedOutLayers()]
  
  # Construct a blob from the input image and then perform a forward pass of the YOLO object detector, giving us our bounding boxes and associated probabilities
  blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416),
    swapRB=True, crop=False)
  net.setInput(blob)
  start = time.time()
  layerOutputs = net.forward(ln)
  end = time.time()

  # Initialize our lists of detected bounding boxes, confidences, and class IDs, respectively
  boxes = []
  confidences = []
  classIDs = []
  CarCount = 0 

  # Loop over each of the layer outputs
  for output in layerOutputs:
    # Loop over each of the detections
    for detection in output:
      # Extract the class ID and confidence (i.e., probability) of the current object detection
      scores = detection[5:]
      classID = np.argmax(scores)
      confidence = scores[classID]
  
      # Filter out weak predictions by ensuring the detected probability is greater than the minimum probability
      if confidence > confThreshold:
        # Scale the bounding box coordinates back relative to the
        # size of the image, keeping in mind that YOLO actually
        # returns the center (x, y)-coordinates of the bounding
        # box followed by the boxes' width and height
        box = detection[0:4] * np.array([Width, Height, Width, Height])
        (centerX, centerY, width, height) = box.astype("int")
  
        # Use the center (x, y)-coordinates to derive the top and left corner of the bounding box
        x = int(centerX - (width / 2))
        y = int(centerY - (height / 2))
  
        # Update our list of bounding box coordinates, confidences, and class IDs
        boxes.append([x, y, int(width), int(height)])
        confidences.append(float(confidence))

        classIDs.append(classID)
  
  # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
  idxs = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
  
  # Ensure at least one detection exists
  if len(idxs) > 0:
    # Loop over the indexes we are keeping
    for i in idxs.flatten():
    
      # Extract the bounding box coordinates
      (x, y) = (boxes[i][0], boxes[i][1])
      (w, h) = (boxes[i][2], boxes[i][3])
  
      # Draw a bounding box rectangle and label on the image
      color = [int(c) for c in COLORS[classIDs[i]]]
      cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
      text = "{}: {:.4f}".format(classNames[classIDs[i]], confidences[i])
      cv2.putText(img, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
        0.5, color, 2)

      # Count the number of cars detected in the photo
      if classIDs[i] == 2: 
        CarCount = CarCount + 1

  # Print the number of cars detected in the photo
  # print("The Car Count is: ", CarCount)

  # text
  text = 'Count: ' + str(CarCount)

  # font
  font = cv2.FONT_HERSHEY_SIMPLEX

  # org
  org = (500, 50)

  # fontScale
  fontScale = 0.5

  # Red color in BGR
  color = (0, 0, 0)

  # Line thickness of 2 px
  thickness = 2

  # Using cv2.putText() method
  img = cv2.putText(img, text, org, font, fontScale,
                      color, thickness, cv2.LINE_AA, False)

  return img