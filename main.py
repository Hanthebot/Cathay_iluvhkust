from flask import Flask, request, render_template
import pytesseract
from PIL import Image

from preprocess import preprocess_img
from postprocess import extract_11_digit_number, make_dash_separated, validate
from qr import generate_qr

app = Flask(__name__, static_url_path='/static')
pytesseract.pytesseract.tesseract_cmd = r'static/tesseract/tesseract.exe'
OPTIONS = "-c tessedit_char_whitelist=0123456789"

def render_error(msg: str, attempt: str = ""):
    return render_template('error.html', msg = msg, attempt = attempt)

@app.route('/scanned', methods=['POST'])
def scan_handle():
    """ after scan """
    waybill = request.form['barcode']
    print(waybill)
    if waybill == "":
        return render_error("No data received")
    result = {
        "type": "Scan",
        "waybill": make_dash_separated(waybill),
        "src": generate_qr(waybill)
    }
    return render_template('ocr_rst.html', result = result)

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
                    "type": "OCR",
                    "waybill": make_dash_separated(waybill),
                    "src": generate_qr(waybill)
                }
                return render_template('ocr_rst.html', result = result)
            return render_error("failed validation", waybill)
        return render_error(f"failed to detect", ocr_result)
    return render_error("no file")

@app.route('/redirect', methods=['GET'])
def redirect():
    return render_error("failed validation", request.form['number'])

@app.route('/register', methods=['POST'])
def register():
    waybill = request.form['number']
    if validate(waybill):
        result = {
            "type": "Correction",
            "waybill": make_dash_separated(waybill),
            "src": generate_qr(waybill)
        }
        return render_template('ocr_rst.html', result = result)
    return render_error("failed validation", waybill)

@app.route('/scanned', methods=['GET'])
@app.route('/ocr', methods=['GET'])
@app.route('/')
def root():
    """ root """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
