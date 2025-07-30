from fastapi import FastAPI, Request
#from tgbot.main import tgbot
from api.functions import get_teachers
from urllib.parse import unquote, urlparse

app = FastAPI()


@app.get('/api/teachers')
async def teachers(request: Request):
    try:
        await get_teachers()
    except Exception as e:
        print(e)

