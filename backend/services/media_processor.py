from openai import OpenAI

class ImageProcessor:
    def __init__(self, api_key: str, base_url: str):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = "gpt-4o-mini"  # Model for image processing

    def process_image(self, image_url: str) -> str:
        response = self.client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Что изображено на фото?"},
                    {"type": "image_url", "image_url": {
                        "url": image_url,
                        "detail": "auto"
                    }}
                ]
            }],
            model=self.model,
            max_tokens=50000
        )
        return response.choices[0].message

class AudioProcessor:
    def __init__(self, api_key: str, base_url: str):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = "audio-model"  # Replace with the actual model for audio processing

    def process_audio(self, audio_url: str) -> str:
        response = self.client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Что содержится в аудио?"},
                    {"type": "audio_url", "audio_url": {
                        "url": audio_url,
                        "detail": "auto"
                    }}
                ]
            }],
            model=self.model,
            max_tokens=50000
        )
        return response.choices[0].message