import os
import ffmpeg
import wave
import json
import csv
from vosk import Model, KaldiRecognizer
from config import WORKING_DIR, LANGUAGE_MODEL_PATHS

def convert_to_wav(input_path, output_path):
    try:
        (
            ffmpeg
            .input(input_path)
            .output(output_path, format='wav', acodec='pcm_s16le', ac=1, ar=16000)
            .run(quiet=True)
        )
        print(f"Converted to WAV: {output_path}")
    except Exception as e:
        print(f"Error converting {input_path}: {e}")

def transcribe_audio(audio_path, model_path):
    model = Model(model_path)
    wf = wave.open(audio_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000, 32000, 44100, 48000]:
        raise ValueError("Audio file must be WAV format mono PCM.")
    
    rec = KaldiRecognizer(model, wf.getframerate())
    transcription = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            transcription += result['text'] + " "
    transcription += json.loads(rec.FinalResult())['text']
    return transcription

def transcribe_videos(csv_file):
    rows = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for row in rows:
        if row['Status'] != 'downloaded':
            continue
        filename = row['Filename']
        video_path = os.path.join(WORKING_DIR, filename)
        if not os.path.isfile(video_path):
            print(f"Video not found: {filename}")
            continue
        
        wav_path = video_path.rsplit('.', 1)[0] + ".wav"
        convert_to_wav(video_path, wav_path)
        language = row['Language'].lower()
        model_path = LANGUAGE_MODEL_PATHS.get(language)
        if not model_path:
            print(f"No model for language '{language}'")
            row['Transcription'] = ''
            row['Status'] = 'transcribed'
        else:
            row['Transcription'] = transcribe_audio(wav_path, model_path)
            row['Status'] = 'transcribed'
            print(f"Transcribed: {filename}")
        os.remove(wav_path)

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
