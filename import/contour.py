import cv2
import numpy as np

def height_test(height, closest_class):
    height_modifiers = {}

    height_modifiers[1] = {
        5: 3.0,
        20: 3.2,
        26: 3.2,
        32: 3.25,
        35: 3.43,
        60: 3.45,
        150: 3.5,
        float('inf'): 3.5,
    }

    height_modifiers[0] = {
        55: 10.7,
        60: 11.25,
        120: 11.27,
        150: 11.3,
        200: 11.5,
        300: 12.0,
        float('inf'): 12,
    }

    for threshold, modifier in height_modifiers[closest_class].items():
        if height <= threshold:
            modified_height = modifier
            break

    # Introduce an exponential factor that adjusts the height modifier
    # when the object is farther away (smaller bounding box)
    height_factor = max(0, .1 - (height / 90) ** 2)  # Adjust the constants as needed
    modified_height += height_factor

    return modified_height


def detect_head(frame, bbox, aim_point, enemy_class, y_offset_factors=None):
    if y_offset_factors is None:
        y_offset_factors = {
            0: 1,  # Default factor for class 0
            1: 1.02,  # Factor for class 1
            # Add more classes and factors as needed
        }

    y_offset_factor = y_offset_factors.get(enemy_class, 1.02)

    X, Y, width, height = map(float, bbox)
    head_height = height / 3

    # Define the lower and upper red color boundaries
    lower_red = np.array([0, 0, 200])
    upper_red = np.array([50, 50, 255])

    # Create a mask for the red color within the bounding box
    cropped_frame = frame[int(Y):int(Y + head_height), int(X):int(X + width)]
    red_mask = cv2.inRange(cropped_frame, lower_red, upper_red)

    # Find the contours in the red_mask
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours on the original frame
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

    # Find the center of the red outline
    red_points = np.argwhere(red_mask == 255)
    if red_points.size > 0:
        red_center = red_points.mean(axis=0)
        head_center_x = X + red_center[1]
        head_center_y = Y + red_center[0]

        # Apply the y_offset_factor to the head_center_y
        head_center_y = Y + (head_center_y - Y) * y_offset_factor
    else:
        head_center_x = X + width / 2
        head_center_y = Y + head_height / 2

        # Call height_test and use the returned value as the y-offset factor
        modified_height = height_test(height, enemy_class)

        # Apply the modified_height to the head_center_y
        head_center_y = Y + (head_center_y - Y) * modified_height

    dif_x = head_center_x - aim_point
    dif_y = head_center_y - aim_point

    # Draw a circle on the head center
    cv2.circle(frame, (int(head_center_x), int(head_center_y)), 5, (0, 0, 255), -1)

    return dif_x, dif_y, frame