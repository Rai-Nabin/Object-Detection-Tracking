import os
from collections import Counter


def calculate_class_weights(labels_dir, num_classes):
    """
    Calculates class weights based on the frequency of each class in YOLO-format label files.
    YOLO Format: class_id x_center y_center width height

    Args:
        labels_dir (str): Path to the directory containing YOLO-format label files (.txt).
        num_classes (int): The total number of classes in the dataset.

    Returns:
        list: A list of class weights, where each element corresponds to the weight of a class.
    """

    class_counts = Counter()  # Initialize a Counter to store class frequencies

    # Iterate through all files in the labels directory
    for label_file in os.listdir(labels_dir):
        # Process only .txt label files
        if label_file.endswith(".txt"):
            label_path = os.path.join(
                labels_dir, label_file
            )  # Construct the full file path
            try:
                with open(label_path, "r") as f:
                    # Read each line in the label file
                    for line in f:
                        # Extract the class ID from the line
                        class_id = int(line.split()[0])
                        class_counts[class_id] += 1  # Increment the count for the class
            except FileNotFoundError:
                print(f"File not found: {label_path}")
            except ValueError:
                print(f"Incorrect file format in {label_path}")

    total = sum(class_counts.values())  # Calculate the total number of objects

    # Calculate class weights: total_objects / (num_classes * objects_in_class)
    # If a class is not present, assign a weight of 1.0
    weights = [
        total / (num_classes * class_counts[i]) if i in class_counts else 1.0
        for i in range(num_classes)
    ]

    return weights


labels_directory = "data/train/labels"  # Replace with your labels directory
number_of_classes = 4  # Replace with the number of classes in your dataset

class_weights = calculate_class_weights(labels_directory, number_of_classes)
print("Class weights:", class_weights)
