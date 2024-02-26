import cv2
import numpy as np
import picamera2
import time
from circle_detection_test import take_pic, convert_pic

name = "testpic"

def capture_image():
    with picamera2.Picamera2() as camera:
        # Set camera resolution
        camera.resolution = (640, 480)

        # Allow time for the camera to warm up
        time.sleep(2)

        capture_config = camera.create_still_configuration()

#         yuv420 = camera.capture_array()
#         rgb =cv2.cvtColor(yuv420, cv2.COLOR_YUV420p2RGB)
#         return rgb
        print('capturing array...')
        array = camera.capture_array("main")
        print('finished capturing array')
        return array

#         # Capture image to a NumPy array
#         with picamera2.array.PiRGBArray(camera) as output:
#             camera.capture(output, format='bgr')
#             return output.array

def main():
    while True:
        # Capture an image from the Pi Camera
        take_pic(name)
        (img_rgb, img_grey) = convert_pic(name)
        # frame = capture_image()
        
        # ranges for HSV
        lower_color = np.array([100, 100, 100])
        upper_color = np.array([140,255,255])
        
        # Convert the frame to grayscale
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # gray = img_grey
        hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
        hsv = cv2.inRange(hsv, lower_color, upper_color)
        # Get the V component
        # gray = hsv[:][:][2]

        # Apply GaussianBlur to reduce noise and help with detection
        blurred = cv2.GaussianBlur(hsv, (5, 5), 0)

        # Use HoughCircles to detect circles in the image
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=20,
            param1=50,
            param2=30,
            minRadius=20,
            maxRadius=120
        )
        print(circles)
        # If circles are found, draw them on the frame
        if circles is not None:
            circles = np.uint16(np.around(circles))
            most_prominent_circle = circles[0][0]  # Select the first circle as the most prominent

            # Draw the circle on the frame
            cv2.circle(img_rgb, (most_prominent_circle[0], most_prominent_circle[1]), most_prominent_circle[2], (0, 255, 0), 2)

        # Display the frame
        cv2.imshow("Blob Detection", img_rgb)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close OpenCV windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
