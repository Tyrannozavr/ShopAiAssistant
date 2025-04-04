from openai import OpenAI

client = OpenAI(
    api_key="sk-aitunnel-ImlpEVcxw17ks2gGUnLUuP28ueQS2YZz", # Ключ из нашего сервиса
    base_url="https://api.aitunnel.ru/v1/",
)

# chat_result = client.chat.completions.create(
#     messages=[{"role": "user", "content": "Скажи интересный факт"}],
#     model="deepseek-r1",
#     max_tokens=50000, # Старайтесь указывать для более точного расчёта цены
# )
# print(chat_result.choices[0].message)

# Распознать фото
photo_result = client.chat.completions.create(
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Что изображено на фото?"},
            {"type": "image_url", "image_url": {
                "url": "https://img.freepik.com/free-photo/red-white-cat-i-white-studio_155003-13189.jpg",
                "detail": "auto"
            }}
        ]
    }],
    model="gpt-4o-mini",

    max_tokens=50000, # Старайтесь указывать для более точного расчёта цены
)
print(photo_result.choices[0].message)