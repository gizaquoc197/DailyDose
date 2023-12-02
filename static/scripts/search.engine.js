const voiceCommandButton = document.getElementById('voice-command-button');

if ('webkitSpeechRecognition' in window) {
    const recognition = new webkitSpeechRecognition();

    recognition.continuous = true;
    recognition.interimResults = true;


    recognition.onresult = function (event) {
        const result = event.results[0][0].transcript.trim();
        document.getElementById('search_query').value = result;
    };

    voiceCommandButton.addEventListener('click', function () {
        recognition.start();
    });

} else {
    voiceCommandButton.disabled = true;
    console.log('Web Speech API is not supported in this browser.');
}