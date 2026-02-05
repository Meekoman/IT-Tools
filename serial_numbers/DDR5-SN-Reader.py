import cv2
import numpy as np
import pytesseract
import os
print(np.__version__)
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Set up directories
output_dir = './'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def capture_image(video_source=0):
    # Start webcam capture
    cap = cv2.VideoCapture(video_source)
    ret, frame = cap.read()
    cap.release()  # Release the camera
    return frame if ret else None

def process_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Use thresholding to preprocess the image
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return thresh

def read_serial_number(image):
    # Use Tesseract to extract text
    custom_config = r'--oem 3 --psm 6'  # Specify the OCR Engine and Page Segmentation Mode
    text = pytesseract.image_to_string(image, config=custom_config)
    return text.strip()

def main():
    for i in range(10):  # Capture 10 images; adjust as needed
        print("Capturing Image... Press 'Enter' to capture.")
        input()  # Wait for user to press Enter
        image = capture_image()

        if image is None:
            print("Failed to capture image.")
            continue

        processed_image = process_image(image)
        serial_number = read_serial_number(processed_image)

        if serial_number:
            print(f"Detected Serial Number: {serial_number}")
            with open(os.path.join(output_dir, f'serial_{i}.txt'), 'w') as f:
                f.write(serial_number)
        else:
            print("No serial number detected.")

if __name__ == "__main__":
    main()
