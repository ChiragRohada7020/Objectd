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
file_path = "output_file.txt"

# User-specified classes
classes_of_interest = ["person", "car"]

# Find the maximum counts
max_counts = process_file(file_path, classes_of_interest)

# Print the maximum counts
for class_name, count in max_counts.items():
    print(f"Maximum count of {class_name}: {count}")
