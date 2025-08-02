from fastapi import FastAPI, Request
#from tgbot.main import tgbot
from api.functions import get_teachers, main
from urllib.parse import unquote, urlparse

app = FastAPI()


@app.get('/api/teachers')
async def get_handler(request: Request):
    try:
        await main()
    except Exception as e:
        print(e)

