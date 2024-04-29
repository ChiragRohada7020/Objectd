import cv2
import torch
from gtts import gTTS
import os

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    # Perform inference
    results = model(frame)
    
    # Extract detected objects and their confidence scores
    labels = results.names
    scores = results.pred[0][:, 4].cpu().numpy()  # Access predictions for the first image in the batch
    
    detected_objects = []

    for label, score in zip(labels, scores):
        if score > 0.5:  # Filter detections based on confidence score
            detected_objects.append(str(label))  # Convert label to string
    
    # Convert detected objects list to text
    text = ', '.join(detected_objects)
    
    # Create voice output
    if detected_objects:
        tts = gTTS(text='I see ' + text, lang='en')
        tts.save("temp.mp3")
        os.system("mpg321 temp.mp3")
    
    # Render results
    cv2.imshow('YOLOv5 Object Detection', results.render()[0])
    
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
