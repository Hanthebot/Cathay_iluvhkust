from flask import Flask, request, render_template
import pytesseract
from PIL import Image

from preprocess import preprocess_img
from postprocess import extract_11_digit_number, make_dash_separated, validate
from qr import generate_qr

app = Flask(__name__, static_url_path='/static')
pytesseract.pytesseract.tesseract_cmd = <YOUR_TESSERACT_DIR>
OPTIONS = "-c tessedit_char_whitelist=0123456789,."

def render_error(msg: str):
    return render_template('error.html', msg = msg)

@app.route('/ocr', methods=['POST'])
def ocr():
    """ OCR """
    if 'file' not in request.files:
        return render_error("No file part")

    file = request.files['file']
    if file.filename == '':
        return render_error("No selected file")

    if file:
        image = Image.open(file.stream)
        preprocessed = preprocess_img(image)
        ocr_result = pytesseract.image_to_string(preprocessed, lang='eng', config=OPTIONS)
        waybill = extract_11_digit_number(ocr_result)
        if waybill:
            if validate(waybill):
                result = {
                    "waybill": make_dash_separated(waybill),
                    "src": generate_qr(waybill)
                }
                return render_template('ocr_rst.html', result = result)
            return render_error(f"failed validation: {waybill}")
        return render_error(f"failed to detect from: {ocr_result}")
    return render_error("no file")

@app.route('/')
def root():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, debut=True)
