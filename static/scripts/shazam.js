document.addEventListener('DOMContentLoaded', function () {
    const startRecordingButton = document.getElementById('startRecording');
    const stopRecordingButton = document.getElementById('stopRecording');
    const resultContainer = document.getElementById('resultContainer');

    let mediaRecorder;
    let audioChunks = [];

    startRecordingButton.addEventListener('click', startRecording);
    stopRecordingButton.addEventListener('click', stopRecording);

    async function startRecording() {
        // Check if there's an active recording, stop it before starting a new one
        stopRecording();

        const stream = await navigator.mediaDevices.getUserMedia({
            audio: true
        });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = event => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, {
                type: 'audio/ogg'
            });
            const formData = new FormData();
            formData.append('audio_data', audioBlob, 'recording.ogg');

            fetch('/recognize_music', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(result => {
                    console.log('Shazam Result:', result);
                    // Display the "share" node in a preformatted block
                    resultContainer.innerHTML = `
                                    <h2>Recognition Result:</h2>
                                    <pre>${JSON.stringify(result.result.track.share.subject, null, 2)}</pre>
                                `;

                    // Allow the user to start a new loop
                    startRecordingButton.disabled = false;
                })
                .catch(error => {
                    console.error('Error:', error);
                    // Allow the user to start a new loop even if an error occurs
                    startRecordingButton.disabled = false;
                });
        };

        mediaRecorder.start();
        startRecordingButton.disabled = true;
        stopRecordingButton.disabled = false;
    }

    function stopRecording() {
        if (mediaRecorder) {
            if (mediaRecorder.state === 'recording') {
                mediaRecorder.stop();
            }
            // Reset the audio chunks for a new recording
            audioChunks = [];
            startRecordingButton.disabled = false;
            stopRecordingButton.disabled = true;
        }
    }
});