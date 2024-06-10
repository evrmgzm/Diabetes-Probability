import csv
import math
import tkinter as tk
from tkinter import messagebox

def normalize(value, min_val, max_val):
    # Normalize a value between 0 and 1
    return (value - min_val) / (max_val - min_val)

def euclidean_distance(vector1, vector2):
    # Calculate the Euclidean distance between two vectors
    squared_difference = sum((float(x) - float(y)) ** 2 for x, y in zip(vector1, vector2))
    return math.sqrt(squared_difference)

def find_min_max(filepath):
    # Find the minimum and maximum values for each column in the dataset
    min_values = [float('inf')] * 8
    max_values = [float('-inf')] * 8

    with open(filepath, 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            for i, value in enumerate(map(float, row[:-1])):
                min_values[i] = min(min_values[i], value)
                max_values[i] = max(max_values[i], value)

    return min_values, max_values

def preprocess_data(input_vector, min_values, max_values):
    # Normalize the input vector using the min-max values
    normalized_input = [normalize(float(value), min_val, max_val) for value, min_val, max_val in
                        zip(input_vector, min_values, max_values)]
    return [round(value, 3) for value in normalized_input]

def find_closest_points(input_vector, preprocessed_filepath, k):
    # Find the k closest points to the input vector
    closest_points = []
    with open(preprocessed_filepath, 'r') as file, open(diabetes_csv_path, 'r') as file2:
        csv_reader = csv.reader(file, delimiter=',')
        csv_reader2 = csv.reader(file2, delimiter=',')
        next(csv_reader)  # Skip header row
        next(csv_reader2)  # Skip header row
        for row, row2 in zip(csv_reader, csv_reader2):
            if row and row2:
                numeric_row = list(map(float, row[:-1]))  # Exclude the last column (target)
                distance = euclidean_distance(input_vector, numeric_row)
                closest_points.append((distance, row2))
               
    # Sort the closest points by distance
    closest_points.sort(key=lambda x: x[0])
    # Calculate diabetes probability from closest points
    probabilities = [float(row[-1]) for _, row in closest_points[:k]]
    diabetes_probability = sum(probabilities) / k * 100
    return closest_points[:k], diabetes_probability

def check_input(input_data, max_values, min_values):
    # Check if the input values are within the valid range
    for i in input_data:
        if i == 'empty':
            return 3
    for i, ma, mi in zip(input_data, max_values, min_values):
        if i > ma or i < mi:
            return 2
    return True

def update_results(results,k):
    # Clear the screen if there are results on the screen
    for i, result in enumerate(results):
        if i >= k:
            result.config(text="")
        else:
            result_labels[i].config(text=result)

def process_input():
    # Process the input values and display the results
    input_data = [float(entry.get()) if entry.get() else 'empty' for entry in entry_fields]
    if input_data[8] == 'empty':
        input_data[8] = 5
        k = 5
    else:
        k = int(input_data[8])
        
    validation = check_input(input_data, max_values, min_values) # Check if the input values are valid

    if validation == 2:
        messagebox.showerror("Error", "Input values are out of bounds!")
        return
    elif validation == 3:
        messagebox.showerror("Error", "Inputs cannot be empty.")
        return

    if rownumber < k or k < 1:
        messagebox.showerror("Error", "Closest Records Number cannot be greater than the number of records in the dataset.")
        return
    
    update_results(result_labels,k)
    
    preprocessed_input = preprocess_data(input_data, min_values, max_values)
    closest_points, diabetes_probability = find_closest_points(preprocessed_input, preprocessed_csv_path,k)
    # Update the label text with diabetes probability
    probability_label.config(text=f"Diabetes Probability: {diabetes_probability:.2f}%")
    for i, (distance, row) in enumerate(closest_points):
        result_labels[i].config(text=f"Point {i+1}: {row}, Distance: {distance}")

diabetes_csv_path = "diabetes.csv"
preprocessed_csv_path = "diabetes_preprocessed.csv"

min_values, max_values = find_min_max(diabetes_csv_path)

# Save preprocessed data to a new file
rownumber = 0
with open(diabetes_csv_path, 'r') as file:
    csv_reader = csv.reader(file, delimiter=',')
    with open(preprocessed_csv_path, 'w', newline='') as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow(next(csv_reader))  # Write header row
        for row in csv_reader:
            rownumber += 1
            preprocessed_row = preprocess_data(row[:-1], min_values, max_values)
            preprocessed_row.append(row[-1])  # Append the target value
            csv_writer.writerow(preprocessed_row)

root = tk.Tk()
root.title("Diabetes Predictor")
root.configure(bg="#f0f0f0")

labels = [
    "Pregnancies: ({}-{})".format(min_values[0], max_values[0]),
    "Glucose: ({}-{})".format(min_values[1], max_values[1]),
    "Blood Pressure: ({}-{})".format(min_values[2], max_values[2]),
    "Skin Thickness: ({}-{})".format(min_values[3], max_values[3]),
    "Insulin: ({}-{})".format(min_values[4], max_values[4]),
    "BMI: ({}-{})".format(min_values[5], max_values[5]),
    "Diabetes Pedigree Function: ({}-{})".format(min_values[6], max_values[6]),
    "Age: ({}-{})".format(min_values[7], max_values[7]),
    "Number of Closest Records (1-{}):".format(rownumber),
]
entry_fields = []
for i, label_text in enumerate(labels):
    label = tk.Label(root, text=label_text, bg="#f0f0f0", font=("Arial", 10))
    label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
    entry = tk.Entry(root)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entry_fields.append(entry)

process_button = tk.Button(root, text="Process", command=process_input, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
process_button.grid(row=len(labels), columnspan=2, pady=10)

result_frame = tk.Frame(root, bg="#f0f0f0")
result_frame.grid(row=len(labels)+1, columnspan=2, pady=10)

result_canvas = tk.Canvas(result_frame, bg="#f0f0f0", width=700)
result_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(result_frame, orient="vertical", command=result_canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_canvas.configure(yscrollcommand=scrollbar.set)
result_canvas.bind("<Configure>", lambda e: result_canvas.configure(scrollregion=result_canvas.bbox("all")))

result_inner_frame = tk.Frame(result_canvas, bg="#f0f0f0", width=700)
result_inner_frame.bind("<Configure>", lambda e: result_canvas.configure(scrollregion=result_canvas.bbox("all")))
result_canvas.create_window((0, 0), window=result_inner_frame, anchor="nw")

result_labels = []
for i in range(rownumber):
    result_label = tk.Label(result_inner_frame, text="", bg="#f0f0f0", font=("Arial", 10))
    result_label.pack(anchor="w", padx=10, pady=2)
    result_labels.append(result_label)

# Add label to show diabetes probability
probability_label = tk.Label(root, text="", bg="#f0f0f0", font=("Arial", 12, "bold"))
probability_label.grid(row=len(labels)+2, columnspan=2, pady=10)

root.mainloop()