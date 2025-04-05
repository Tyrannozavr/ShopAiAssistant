import requests
from io import BytesIO
from pydub import AudioSegment
from core.Config import settings
from openai import OpenAI


class TelegramAudioTranscriber:
    def __init__(self, bot_token: str, api_key: str, base_url: str):
        self.bot_token = bot_token
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def download_file_by_id(self, file_id: str) -> bytes:
        # Получаем информацию о файле
        file_info_url = f"https://api.telegram.org/bot{self.bot_token}/getFile?file_id={file_id}"
        file_info = requests.get(file_info_url).json()

        if not file_info.get('ok'):
            raise Exception("File not found")

        file_path = file_info['result']['file_path']
        download_url = f"https://api.telegram.org/file/bot{self.bot_token}/{file_path}"

        # Скачиваем файл
        file_data = requests.get(download_url).content
        return file_data

    def convert_to_mp3(self, file_data: bytes) -> BytesIO:
        # Convert the audio file to mp3 format in memory
        audio = AudioSegment.from_file(BytesIO(file_data))
        mp3_buffer = BytesIO()
        audio.export(mp3_buffer, format="mp3")
        mp3_buffer.seek(0)  # Rewind the buffer to the beginning
        return mp3_buffer

    def transcribe_audio(self, file_data: bytes) -> str:
        # Convert the file to mp3 in memory
        mp3_buffer = self.convert_to_mp3(file_data)

        # Transcribe the audio directly from memory
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=("audio.mp3", mp3_buffer, "audio/mpeg")
        )

        return transcription.text

    def file_id_to_text(self, file_id: str) -> str:
        file_data = self.download_file_by_id(file_id)
        return self.transcribe_audio(file_data)


# Example usage
transcriber = TelegramAudioTranscriber(
    bot_token=settings.bot_token,
    api_key=settings.openai_key,
    base_url=settings.openai_url
)

file_id = "AwACAgIAAxkBAAONZ_D6ctr-ioX4OqCHoUhzgU_wOv8AAnxvAAKquolLTrmcVXlGvB42BA"
transcription_text = transcriber.file_id_to_text(file_id)
print("Text is ", transcription_text)