// Capture photo
snap.addEventListener('click', () => {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(blob => {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/ocr';
        form.enctype = 'multipart/form-data';

        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.name = 'file';
        const file = new File([blob], 'photo.png', { type: 'image/png' });
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;

        form.appendChild(fileInput);
        document.body.appendChild(form);
        form.submit();
    }, 'image/png');
});

// Capture photo using space key
document.addEventListener('keydown', function(event) {
    if (event.code === 'Space') {
        snap.click();
    }
});

function validate(digits) {
    // check digit validity
    if (digits.length < 11 || isNaN(digits)) {
        return false;
    }
    return parseInt(digits.slice(3, 10)) % 7 === parseInt(digits[digits.length - 1]);
}


document.getElementById('clear').addEventListener('click', function() {
    document.getElementById('barcode').textContent = 'Waiting...';
});