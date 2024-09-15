import cv2

def extract_frames(video_file, output_file, frame_interval=30):
    # Open the video file
    cap = cv2.VideoCapture(video_file)

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)  # Frames per second of the original video

    # Define codec and create VideoWriter object to save output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps // frame_interval, (frame_width, frame_height))

    frame_count = 0
    saved_frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break  # Break the loop when video is done

        # Only process every 'frame_interval' frame (i.e., 1 out of every 30 frames)
        if frame_count % frame_interval == 0:
            out.write(frame)  # Save this frame
            saved_frame_count += 1

        frame_count += 1

    # Release everything when job is finished
    cap.release()
    out.release()

    print(f"Total frames processed: {frame_count}")
    print(f"Total frames saved: {saved_frame_count}")

# Call the function to process your video
extract_frames('/home/emuch/Documents/Forget-Me-Not-Capstone/CV-Algs/IMG_1302.MOV', '/home/emuch/Documents/Forget-Me-Not-Capstone/CV-Algs/output_video.MOV', frame_interval=30)
