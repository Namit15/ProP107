import cv2
import time
import math

p1 = 530  # X-coordinate of the goal point
p2 = 300  # Y-coordinate of the goal point

xs = []  # List to store ball's X-coordinates across frames
ys = []  # List to store ball's Y-coordinates across frames

video = cv2.VideoCapture("footvolleyball.mp4")
# Load tracker (replace with a more robust tracker if needed)
tracker = cv2.TrackerCSRT_create()

# Read the first frame of the video
success, img = video.read()

# Select the bounding box around the ball on the first frame
bbox = cv2.selectROI("tracking", img, False)

# Initialize the tracker on the first frame and the bounding box
tracker.init(img, bbox)


def goal_track(img, bbox):
  """Tracks the ball, calculates distance to goal point, and detects goal."""
  x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])

  # Mark the ball's center with a blue circle
  center_x = x + int(w / 2)
  center_y = y + int(h / 2)
  cv2.circle(img, (center_x, center_y), 2, (0, 0, 255), 5)

  # Mark the goal point with a green circle
  cv2.circle(img, (int(p1), int(p2)), 2, (0, 255, 0), 3)

  # Calculate the Euclidean distance between the ball's center and the goal point
  distance = math.sqrt(((center_x - p1) ** 2) + ((center_y - p2) ** 2))
  print(distance)

  # Display "Goal" text if the distance is less than or equal to 20 pixels
  if distance <= 20:
    cv2.putText(img, "Goal", (300, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

  # Append ball's center coordinates to respective lists
  xs.append(center_x)
  ys.append(center_y)

  # Draw a trajectory line for the ball's movement (optional)
  for i in range(len(xs) - 1):
    cv2.line(img, (xs[i], ys[i]), (xs[-1], ys[-1]), (0, 0, 255), 2)


def draw_bounding_box(img, bbox):
  """Draws a red rectangle around the tracked object (ball)."""
  x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
  cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)
  cv2.putText(img, "Tracking", (75, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


while True:
  # Read the next frame from the video
  success, img = video.read()

  # Check if frame is read correctly
  if not success:
    print("Error: Could not read frame")
    break

  # Update tracker based on the previous frame and bounding box
  success, bbox = tracker.update(img)

  # Check if tracking is successful
  if success:
    # Call functions to track the ball, draw bounding box, and detect goal
    goal_track(img.copy(), bbox)  # Pass a copy of the frame to avoid modification
    draw_bounding_box(img, bbox)
  else:
    print("Tracking failed")

  # Display the frame with tracking information
  cv2.imshow("Foot Volleyball Tracking", img)

  # Exit if 'q' key is pressed
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break