from cyberchipped.utilities.openai import get_client
from openai._types import FileTypes


async def ai_listen(
    file: FileTypes,
    response_format: str = "text",
):
    client = get_client()
    response = await client.audio.transcriptions.create(
        file=file,
        model="whisper-1",
        response_format=response_format,
    )
    return response
