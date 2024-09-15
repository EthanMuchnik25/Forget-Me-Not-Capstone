import cv2

def detect_movement(video_file, movement_threshold=5000):
    # Open video file
    cap = cv2.VideoCapture(video_file)

    # Initialize variables to hold previous frame
    ret, previous_frame = cap.read()
    
    if not ret:
        print("Error: Couldn't read the video file")
        return
    
    # Convert the previous frame to grayscale
    previous_frame = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)

    # Loop over video frames
    while cap.isOpened():
        ret, current_frame = cap.read()

        if not ret:
            break  # End of video

        # Convert current frame to grayscale
        current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

        # Compute the absolute difference between the current and previous frame
        frame_diff = cv2.absdiff(previous_frame, current_frame_gray)

        # Apply threshold to ignore small differences (noise)
        _, thresh = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)

        # Count the number of white pixels (significant differences)
        movement_pixels = cv2.countNonZero(thresh)

        # Check if the number of differing pixels is above the movement threshold
        if movement_pixels > movement_threshold:
            print("Movement detected!")

        # Update the previous frame
        previous_frame = current_frame_gray

        # Optional: Show the thresholded difference for visualization
        cv2.imshow('Frame Difference', thresh)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    # Release the video capture object and close windows
    cap.release()
    cv2.destroyAllWindows()

# Call the function with your video file
detect_movement("your_video_file.mp4", movement_threshold=5000)
