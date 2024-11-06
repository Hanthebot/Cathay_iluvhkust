const toggleButton = document.getElementById('toggle');
const context = canvas.getContext('2d');
const video = document.querySelector('video');

let stream;

toggleButton.addEventListener('click', () => {
    if (video.srcObject) {
        // Turn off the camera
        video.srcObject.getTracks().forEach(track => track.stop());
        video.srcObject = null;
        toggleButton.innerText = 'Turn on Camera';
    } else {
        // Turn on the camera
        toggleButton.innerText = 'Turn off Camera';
        navigator.mediaDevices.getUserMedia({ video: true })
        .then(newStream => {
            stream = newStream;
            video.srcObject = stream;
        })
        .catch(err => {
            console.error("Error accessing the camera: " + err);
        });
        new Promise(r => setTimeout(r, 200));
    }
});