# Your Python code (app.py)
import asyncio
import logging
from flask import Flask, render_template, request, jsonify
from shazamio import Shazam

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

@app.route('/', methods=['GET'])
def shazam():
    return render_template('shazam.html')

@app.route('/recognize_music', methods=['POST'])
async def recognize_music_from_frontend():
    logging.info("Received a POST request")

    audio_data = request.files.get('audio_data')

    if audio_data:
        audio_path = 'temp_audio.ogg'
        audio_data.save(audio_path)

        try:
            result = await recognize_music(audio_path)
            logging.info(f"Recognition result: {result}")
            return jsonify({'result': result})
        except Exception as e:
            logging.error(f"Recognition error: {e}")
            return jsonify({'error': str(e)})

    logging.warning("No audio data received")
    return jsonify({'error': 'No audio data received'})


async def recognize_music(file_path):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        shazam = Shazam()
        out = await shazam.recognize_song(file_path)
        print(out)
        return out
    finally:
        loop.close()

if __name__ == '__main__':
    app.run(debug=True)
