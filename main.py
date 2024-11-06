from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import pytesseract
from PIL import Image
import re

from preprocess import preprocess_img

app = Flask(__name__, static_url_path='/static')
pytesseract.pytesseract.tesseract_cmd = <YOUR_TESSERACT_DIR>

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return render_template('error.html', msg = "No file part")

    file = request.files['file']
    if file.filename == '':
        return render_template('error.html', msg = "No selected file")

    if file:
        image = Image.open(file.stream)
        preprocessed = preprocess_img(image)
        ocr_result = pytesseract.image_to_string(preprocessed, lang='eng')

        return render_template('ocr_rst.html', ocr_result = ocr_result)

    return render_template('error.html', msg = "no file")

def extract_11_digit_number(text):
    """Extracts an 11-digit number ending with 0-6 from the given text, considering possible separators."""
    pattern = r'\b(?:\d[\s.,-]*){10}[0-6]\b'
    match = re.search(pattern, text)
    if match:
        return re.sub(r'[\s.,-]', '', match.group())
    return None

@app.route('/')
def root():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, debut=True)
