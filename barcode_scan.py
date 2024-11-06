from flask import Flask, request, render_template
import cv2
from pyzbar.pyzbar import decode
import numpy as np

app = Flask(__name__)

def BarcodeReader(image_path):
    # Read the image
    img = cv2.imread(image_path)

    # Decode the QR codes/barcodes
    detectedBarcodes = decode(img)

    # Check if any barcodes were detected
    if not detectedBarcodes:
        return "QR Code Not Detected or the QR Code is blank/corrupted!"

    # Prepare a list to collect results
    results = []

    for barcode in detectedBarcodes:
        # Draw a rectangle around the detected QR code
        (x, y, w, h) = barcode.rect
        cv2.rectangle(img, (x-10, y-10), (x + w+10, y + h+10), (255, 0, 0), 2)

        # Extract the barcode data
        if barcode.data:
            results.append(f"QR Code data: {barcode.data.decode('utf-8')}\nQR Code type: {barcode.type}")

    # Optionally save the annotated image (for debugging)
    cv2.imwrite('annotated_image.jpg', img)

    # Return results as a single string
    return "\n".join(results)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded image
        image = request.files['image']
        image_path = 'uploaded_image.jpg'
        image.save(image_path)

        # Read the barcode from the image
        result = BarcodeReader(image_path)

        # Render the result in the result template
        return render_template('result.html', result=result)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)