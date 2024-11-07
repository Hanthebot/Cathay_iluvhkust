# Cathay_iluvhkust
Project for Cathay Hackathon 2024, team iluvhkust

### File structure
```
.
├── templates         # web page templates
├── static
│   ├── img/qr        # stores QR codes (temporarily)
│   ├── js            # scripts for functional web page / live scanning
│   ├── tesseract     # OCR module directory
│   └── styles.js     # JS for formatting the page
├── app.py            # backend for the server
├── *.py              # helper functions for backend
└── requirements.txt  # Python dependencies
```

### Usage
- To install dependencies:
  ```cmd
  pip install -r requirements.txt
  ```
- To run
  ```cmd
  flask run --host=0.0.0.0
  ```

### Remarks
  - Tesseract attached works for Windows environment 