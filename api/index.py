from fastapi import FastAPI, Request
#from tgbot.main import tgbot
from api.functions import get_teachers, get_month_data, main
from urllib.parse import unquote, urlparse
#from pydantic import BaseMode
import httpx

app = FastAPI()


    
@app.get('/api/data')
async def get_data(request: Request, month: int):
    try:
        output = await get_month_data(month)
        return output
    except Exception as e:
        print(e)
        return e

@app.get('/api/teachers')
async def get_data(request: Request):
    try:
        async with httpx.AsyncClient() as client:
          teachers = await get_teachers(client)
          teachers = list(map(lambda teacher: teacher["name"], teachers))
          return teachers 
    except Exception as e:
        print(e)
        return e
