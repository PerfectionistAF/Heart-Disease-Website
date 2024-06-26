# echo libraries
import cv2
import numpy as np
from keras.models import load_model
import joblib



# Define paths
video_path = r"D:\MyData\Salma\uni\years\Senior-2\Spring 2024\CSE492 Graduation Project (2)\draft for model\ES000147_4CH_2.avi"

model_path = r"D:\MyData\Salma\uni\years\Senior-2\Spring 2024\CSE492 Graduation Project (2)\django\integration demo 2\Heart-Disease-Website\integration_demo\backend\core\users\machine learning models\laddernet_model.keras"

classification_model_path = r"D:\MyData\Salma\uni\years\Senior-2\Spring 2024\CSE492 Graduation Project (2)\django\integration demo 2\Heart-Disease-Website\integration_demo\backend\core\users\machine learning models\best_logistic_regression_model.joblib"

try:
    model = load_model(model_path)
    classification_model = joblib.load(classification_model_path)
except Exception as e:
    print(f"Error loading models: {e}")
    exit(1)

# Open the video file
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit(1)

# Initialize variables to store the points of the first frame and maximum mean displacements
initial_segments = []
max_mean_displacements = {"Segment 1": 0, "Segment 2": 0, "Segment 3": 0, "Segment 7": 0, "Segment 6": 0, "Segment 5": 0}

# Function to calculate Manhattan distance
def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

# Function to get N equally spaced points in a segment
def get_N_points(inner_boundary, bottom_point, apex_x, N, length, is_left=True):
    points = []
    for i in range(N):
        point = next((p for p in inner_boundary if (p[0] < apex_x if is_left else p[0] > apex_x) and p[1] == (bottom_point[1] - ((i + 1) * length))), None)
        points.append(point)
    return points

# Process each frame
frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_count += 1

    try:
        # Resize the frame
        frame = cv2.resize(frame, (224, 224))
        frame = frame / 255.0  # Normalize frame to range 0-1
        frame = np.expand_dims(frame, axis=0)
        
        prediction = model.predict(frame)
        pred_mask = np.argmax(prediction, axis=-1)[0]

        binary_image = pred_mask > 0
        height, width = binary_image.shape
        
        # Identify bottom-most pixels and apex
        left_half = binary_image[:, :width//2]
        bottom_left_y, bottom_left_x = np.argwhere(left_half)[-1]
        right_half = binary_image[:, width//2:]
        bottom_right_y, bottom_right_x = np.argwhere(right_half)[-1]
        bottom_right_x += width // 2

        bottom_border_trace = [(x, np.argwhere(binary_image[:, x])[-1, 0]) for x in range(bottom_left_x, bottom_right_x + 1) if np.argwhere(binary_image[:, x]).size > 0]
        bottom_border_trace = np.array(bottom_border_trace)
        apex_index = np.argmin(bottom_border_trace[:, 1])
        apex = bottom_border_trace[apex_index]
        apex_x = apex[0]

        left_half_pixels = [(row[-1, 0], y) for y in range(height) if (row := np.argwhere(binary_image[y, :apex_x])).size > 0]
        right_half_pixels = [(row[0, 0] + apex_x, y) for y in range(height) if (row := np.argwhere(binary_image[y, apex_x:])).size > 0]
        inner_boundary = left_half_pixels + right_half_pixels + [(apex[0], apex[1]), (bottom_left_x, bottom_left_y), (bottom_right_x, bottom_right_y)]

        R = bottom_right_y - apex[1]
        L = bottom_left_y - apex[1]

        N = 10
        left_length = (2 * L // 7) // N
        right_length = (2 * R // 7) // N

        segments = [
            get_N_points(inner_boundary, (bottom_left_x, bottom_left_y), apex_x, N, left_length, is_left=True),
            get_N_points(inner_boundary, next((p for p in inner_boundary if p[0] < apex_x and p[1] == bottom_left_y - 2 * L // 7), None), apex_x, N, left_length, is_left=True),
            get_N_points(inner_boundary, next((p for p in inner_boundary if p[0] < apex_x and p[1] == bottom_left_y - 4 * L // 7), None), apex_x, N, left_length, is_left=True),
            get_N_points(inner_boundary, (bottom_right_x, bottom_right_y), apex_x, N, right_length, is_left=False),
            get_N_points(inner_boundary, next((p for p in inner_boundary if p[0] > apex_x and p[1] == bottom_right_y - 2 * R // 7), None), apex_x, N, right_length, is_left=False),
            get_N_points(inner_boundary, next((p for p in inner_boundary if p[0] > apex_x and p[1] == bottom_right_y - 4 * R // 7), None), apex_x, N, right_length, is_left=False)
        ]
        
        if frame_count == 1:
            initial_segments = segments
        else:
            segment_names = ["Segment 1", "Segment 2", "Segment 3", "Segment 7", "Segment 6", "Segment 5"]
            for i, (segment, name) in enumerate(zip(segments, segment_names)):
                displacements = [manhattan_distance(initial_segments[i][j], segment[j]) for j in range(N)]
                mean_displacement = np.mean(displacements)
                if mean_displacement > max_mean_displacements[name]:
                    max_mean_displacements[name] = mean_displacement
                #print(f"Frame {frame_count}, {name} mean displacement:", mean_displacement)
    except Exception as e:
        print(f"Error processing frame {frame_count}: {e}")
        continue

cap.release()

try:
    displacement_vector = [
        max_mean_displacements["Segment 1"],
        max_mean_displacements["Segment 2"],
        max_mean_displacements["Segment 3"],
        max_mean_displacements["Segment 5"],
        max_mean_displacements["Segment 6"],
        max_mean_displacements["Segment 7"]
    ]

    # Convert the vector to a numpy array and reshape it for the model
    displacement_vector = np.array(displacement_vector).reshape(1, -1)

    output = classification_model.predict(displacement_vector)

    print("\nOutput of the model:", output[0]) # 1: MI , 0: Non-MI
except Exception as e:
    print(f"Error in classification: {e}")