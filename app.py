from flask import Flask, request, render_template
import os
from pyzbar.pyzbar import decode
from PIL import Image

app = Flask(__name__)

# Create the upload directory if it doesn't exist
UPLOAD_FOLDER = r'C:\Users\ngdavian\Documents\cathay\Cathay_iluvhkust\uploadpics'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def BarcodeReader(image_path):
    image = Image.open(image_path)
    decoded_objects = decode(image)
    output_results = []
    if decoded_objects:
        for obj in decoded_objects:
            output_results.append(f"Data: {obj.data.decode('utf-8')}, Type: {obj.type}")
    else:
        output_results.append("No barcode detected in the image.")
    return output_results

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file:
            # Save the file to the uploadpics directory
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)  # Save the file to the specified path
            results = BarcodeReader(file_path)  # Use the correct file path for decoding
            if results[0] == "No barcode detected in the image.":
                return render_template('result.html', no_barcode=True)
            else:
                return render_template('result.html', results=results)
    return render_template('upload.html')

if __name__ == "__main__":
    app.run(debug=True)