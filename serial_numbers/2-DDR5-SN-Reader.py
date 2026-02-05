import cv2
import numpy as np
import pytesseract
import os

# Set path for Tesseract executable (adjust for your own system)
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Update accordingly

# Set up directories for saving serial numbers
output_dir = './'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def capture_image(video_source=0):
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print("Error: Camera not accessible!")
        return None
    
    # Use cv2.CAP_PROP_FRAME_WIDTH or the number 3
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    # Use cv2.CAP_PROP_FRAME_HEIGHT or the number 4
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    ret, frame = cap.read()
    cap.release()  # Release the camera
    return frame if ret else None

#def process_image(image):
#    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#    blur = cv2.GaussianBlur(gray, (5, 5), 0)
#    # Apply Otsu's thresholding
#    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#    dilated = cv2.dilate(thresh, None, iterations=1)  # Dilation helps enhance text
#    return dilated

def adjust_contrast_brightness(image, alpha=1.5, beta=0):
    # alpha: contrast control (1.0-3.0)
    # beta: brightness control (0-100)
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def sharpen_image(image):
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

def process_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    # Adjust contrast and brightness (tweak alpha and beta as needed)
    adjusted = adjust_contrast_brightness(gray, alpha=1.0, beta=0)

    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(adjusted, 255, 
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 
                                   11, 2)

    dilated = cv2.dilate(thresh, None, iterations=1)  # Further enhance text
    normalize = cv2.normalize(dilated, None, alpha=0, beta=255, 
                                norm_type=cv2.NORM_MINMAX, 
                                dtype=cv2.CV_8U)

    return normalize   


def read_serial_number(image):
    custom_config = r'--oem 3 --psm 6'  # Use suitable PSM value
    text = pytesseract.image_to_string(image, config=custom_config)
    print("Detected Text:", text)  # Debugging: log the detected text

    # Use regex to find the serial number pattern
    import re
    match = re.search(r'SN:\s*([A-Za-z0-9-]+)', text)
    match = re.search(r'802C0F.*', text)
    if match:
        serial_number = match.group(2)  # Extract the serial number
        return serial_number.strip()  # Return the cleaned serial number
    return None  # Return None if no match is found


def main():
    for i in range(10):  # Capture multiple images; adjust as needed
        print("Capturing Image... Press 'Enter' to capture.")
        input()  # Wait for user to press Enter
        image = capture_image()

        if image is None:
            print("Failed to capture image.")
            continue

        # Save and inspect the captured image
        cv2.imwrite('captured_image.png', image)  # Save the captured image
        processed_image = process_image(image)
        cv2.imwrite('processed_image.png', processed_image)  # Save the processed image for inspection
        serial_number = read_serial_number(processed_image)

        if serial_number:
            print(f"Detected Serial Number: {serial_number}")
            with open(os.path.join(output_dir, f'serial_{i}.txt'), 'a') as f:
                f.write(serial_number)
        else:
            print("No serial number detected.")

if __name__ == "__main__":
    main()
