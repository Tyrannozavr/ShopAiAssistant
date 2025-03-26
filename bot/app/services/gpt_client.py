import aiohttp

async def get_gpt_response(question):
    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.openai.com/v1/engines/davinci-codex/completions", json={"prompt": question}) as response:
            return await response.text()