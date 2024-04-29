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
                    if class_name == "car" and count > 3:
                        # Trigger an alert
                        alert_message = f"The maximum count of cars ({count}) exceeds 4."
                        trigger_alert(alert_message)
    return max_counts

def trigger_alert(message):
    # Function to trigger an alert
    # This could be a function to send an email, SMS, or any other form of notification
    print("ALERT:", message)

# Example usage:
file_path = "output_file.txt"  # Update with your file path
classes = ["car", "person", "bus"]  # Update with your list of classes
while True:
    process_file(file_path, classes)
