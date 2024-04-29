from flask import Flask, render_template, request, jsonify
import subprocess
import json
import spacy
import os

app = Flask(__name__)
detecting = False
process = None

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load class mapping from JSON file
with open('class_mapping.json') as file:
    class_mapping = json.load(file)

def lemmatize_class(class_name):
    doc = nlp(class_name)
    return doc[0].lemma_.lower() if doc else class_name.lower()

def start_detection(command, output_file):
    try:
        # Open a text file for writing
        with open(output_file, 'w') as f:
            # Run the command and redirect both stdout and stderr to the text file
            process = subprocess.Popen(command, shell=True, stdout=f, stderr=subprocess.STDOUT)
            # Wait for the process to finish
            process.wait()
    except Exception as e:
        print(f"Error starting detection process: {e}")


import re

def extract_class_count(output_string, classes):
    counts = {}

    for class_name in classes:
        # Search for the class name preceded by a number
        pattern = r'(\d+)\s+' + class_name
        match = re.search(pattern, output_string)
        
        if match:
            count = int(match.group(1))
            if class_name not in counts or count > counts[class_name]:
                counts[class_name] = count

    return counts

def process_file(file_path, classes):
    max_counts = {class_name: 0 for class_name in classes}

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            class_counts = extract_class_count(line, classes)
            for class_name, count in class_counts.items():
                if count > max_counts[class_name]:
                    max_counts[class_name] = count

    return max_counts

# Sample file path




def parse_count(count_str):
    try:
        # Attempt to parse the count string as an integer
        count = int(count_str)
        return count
    except ValueError:
        # If the count string cannot be parsed as an integer, return 0
        return 0

@app.route('/')
def index():
    return render_template('chat.html')


class_mapping1 = {
    0: "person",
    1: "bicycle",
    2: "car",
    3: "motorcycle",
    4: "airplane",
    5: "bus",
    6: "train",
    7: "truck",
    8: "boat",
    9: "traffic light",
    10: "fire hydrant",
    11: "stop sign",
    12: "parking meter",
    13: "bench",
    14: "bird",
    15: "cat",
    16: "dog",
    17: "horse",
    18: "sheep",
    19: "cow",
    20: "elephant",
    21: "bear",
    22: "zebra",
    23: "giraffe",
    24: "backpack",
    25: "umbrella",
    26: "handbag",
    27: "tie",
    28: "suitcase",
    29: "frisbee",
    30: "skis",
    31: "snowboard",
    32: "sports ball",
    33: "kite",
    34: "baseball bat",
    35: "baseball glove",
    36: "skateboard",
    37: "surfboard",
    38: "tennis racket",
    39: "bottle",
    40: "wine glass",
    41: "cup",
    42: "fork",
    43: "knife",
    44: "spoon",
    45: "bowl",
    46: "banana",
    47: "apple",
    48: "sandwich",
    49: "orange",
    50: "broccoli",
    51: "carrot",
    52: "hot dog",
    53: "pizza",
    54: "donut",
    55: "cake",
    56: "chair",
    57: "couch",
    58: "potted plant",
    59: "bed",
    60: "dining table",
    61: "toilet",
    62: "tv",
    63: "laptop",
    64: "mouse",
    65: "remote",
    66: "keyboard",
    67: "cell phone",
    68: "microwave",
    69: "oven",
    70: "toaster",
    71: "sink",
    72: "refrigerator",
    73: "book",
    74: "clock",
    75: "vase",
    76: "scissors",
    77: "teddy bear",
    78: "hair drier",
    79: "toothbrush"
}



@app.route('/output',methods=['POST','GET'])
def output():
    if request.method=="POST":
        
        user_input = request.form.get('user_input')



    # Extract keywords using spaCy
        doc = nlp(user_input)

    # Lemmatize words and map to class names
        user_classes = [lemmatize_class(token.text.strip()) for token in doc]
        class_indices = [class_mapping.get(class_name) for class_name in user_classes if class_name in class_mapping]


        file_path = "output_file.txt"

        # User-specified classes
        msg1=""
        classes_of_interest=[]
        for i in class_indices:
            msg1+=str(class_mapping1[i])
            classes_of_interest.append(class_mapping1[i])
        if classes_of_interest==[]:
            return "Sorry I am Not able to understand"   
        
        if "set alert" in user_input:
            return "Setting Alert For  "+msg1+ ", <spam class='font-semibold text-underline'>Provide me the conditions</spam> Deafult set is 3"

        # Find the maximum counts
        max_counts = process_file(file_path, classes_of_interest)

        # Print the maximum counts
        msg=""
        for class_name, count in max_counts.items():
            msg=msg+"  "+f"Maximum count of <span class='font-bold'>{class_name}</span>: <span class='font-bold '>{count}</span>"
            print(f"Maximum count of {class_name}: {count}")
        return msg

      
    return render_template("output.html")



def extract_class_count2(output_string, classes):
    counts = {}

    for class_name in classes:
        # Search for the class name preceded by a number
        pattern = r'(\d+)\s+' + class_name
        match = re.search(pattern, output_string)
        
        if match:
            count = int(match.group(1))
            if class_name not in counts or count > counts[class_name]:
                counts[class_name] = count

    return counts

from gtts import gTTS
def process_file2(file_path, classes, start_line):
    max_counts = {class_name: 0 for class_name in classes}
    alert_triggered = False  # Initialize the alert flag

    with open(file_path, 'r') as file:
        line_number = 1
        for line in file:
            if line_number >= start_line:
                line = line.strip()
                class_counts = extract_class_count2(line, classes)
                for class_name, count in class_counts.items():
                    if count > max_counts[class_name]:
                        max_counts[class_name] = count
                        if count > 3:  # Trigger an alert if count exceeds 3 for any class
                            alert_message = f"The maximum count of {class_name}s ({count}) exceeds 3."
                            trigger_alert(alert_message)
                            alert_triggered = True  # Set the alert flag
            line_number += 1

    if alert_triggered:
        return trigger_alert(alert_message)  # Return 1 if an alert was triggered
    else:
        return 0 # Return 0 if no alert was triggered

def trigger_alert(message):
    # Function to trigger an alert
    # This could be a function to send an email, SMS, or any other form of notification

    print("ALERT:", message)
    x="ALERT:"+message
    return x


@app.route('/set_alert', methods=['POST'])
def set_alert():
    if request.method=="POST":
        
        user_input = request.form.get('user_input')
        if "set alert " in user_input:
            file_path = "output_file.txt" 
             # Update with your file path




    # Extract keywords using spaCy
            doc = nlp(user_input)

    # Lemmatize words and map to class names
            user_classes = [lemmatize_class(token.text.strip()) for token in doc]
            classes_of_interest=[]

            class_indices = [class_mapping.get(class_name) for class_name in user_classes if class_name in class_mapping]
            for i in class_indices:
                classes_of_interest.append(class_mapping1[i])
            with open(file_path, 'r') as file:
                start_line = sum(1 for _ in file)
            while True:

                result = process_file2(file_path, classes_of_interest,start_line)
                if result:  # Assuming process_file2 returns 1 when an alert is triggered
                    break  # Exit the loop if an alert is triggered
            return result
        else:
            return "Not Done "


            



@app.route('/detect', methods=['POST'])
def detect():
    global detecting, process

    # Stop any ongoing detection

    detecting = True

    # Get user-entered classes
    user_input = request.form.get('user_input')

    # Extract keywords using spaCy
    doc = nlp(user_input)

    # Lemmatize words and map to class names
    user_classes = [lemmatize_class(token.text.strip()) for token in doc]

    # Get class indices from the class mapping
    class_indices = [class_mapping.get(class_name) for class_name in user_classes if class_name in class_mapping]

    print(class_indices)

    if 'image' in request.files:
        image = request.files['image']
        image_path = "temp_image.jpg"
        image.save(image_path)

        # Construct the command based on class indices
        command = f"python detect.py --weights yolov5s.pt --source {image_path} --classes {' '.join(map(str, class_indices))}"
    else:
        # Construct the command without image source
        command = f"python detect.py --weights yolov5s.pt --source 0 --classes {' '.join(map(str, class_indices))}"
    
    output_file = "output_file.txt"
    start_detection(command, output_file)
    return  "Detection Completed"  




     # Start detection and capture output

    
    
if __name__ == '__main__':
    app.run(debug=True)
