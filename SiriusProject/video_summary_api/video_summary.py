# video_summary_api.py
from fastapi import FastAPI
from pydantic import BaseModel
from video_downloader import download_from_yandex_disk
from moviepy.editor import VideoFileClip
from vosk import Model, KaldiRecognizer, SetLogLevel
from test_proxyAPI import AI
from pydub import AudioSegment
import json
import os

app = FastAPI()

class VideoURLRequest(BaseModel):
    video_url: str

@app.post("/transcribe/")
async def transcribe_video(request: VideoURLRequest):
    video_url = request.video_url
    model_path = "models/vosk-model-small-ru-0.22"

    video_path = 'video.mp4'
    audio_path = 'audio.wav'

    async def transcribe_audio_from_video(video_url, model_path, video_path='video.mp4', audio_path='audio.wav'):
        # Асинхронная загрузка видео
        await download_from_yandex_disk(video_url, video_path)

        # Извлекаем аудио из видео
        def extract_audio(video_path, audio_path):
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(audio_path, codec='pcm_s16le')
        extract_audio(video_path, audio_path)

        # Настройки модели и распознавания
        SetLogLevel(0)
        FRAME_RATE = 16000
        CHANNELS = 1

        if not os.path.exists(model_path):
            return {"error": "Model not found. Please download the model and unpack it."}
        model = Model(model_path)
        rec = KaldiRecognizer(model, FRAME_RATE)
        rec.SetWords(True)
        audio = AudioSegment.from_file(audio_path).set_channels(CHANNELS).set_frame_rate(FRAME_RATE)
        rec.AcceptWaveform(audio.raw_data)
        result = rec.Result()
        text = json.loads(result)["text"]

        return text
    extracted_text = await transcribe_audio_from_video(video_url, model_path)
    summary = await AI(extracted_text)
    return {"transcribed_text": extracted_text, "summary": summary}
