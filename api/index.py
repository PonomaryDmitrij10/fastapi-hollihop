from fastapi import FastAPI, Request
from api.functions import get_teachers, get_month_data
import httpx
import traceback
import sys

app = FastAPI()

@app.get("/api/data")
async def get_data(request: Request, month: int, year: int):
    try:
        print(f"📅 Запрос данных за месяц: {month}, год: {year}")
        output = await get_month_data(month)
        return output
    except Exception as e:
        err_type, err_value, err_tb = sys.exc_info()
        err = "".join(traceback.format_exception(err_type, err_value, err_tb))
        return {"error": err}


@app.get("/api/teachers")
async def get_teachers_list(request: Request):
    try:
        async with httpx.AsyncClient() as client:
            teachers = await get_teachers(client)
            teachers = [teacher["name"] for teacher in teachers]
            return teachers
    except Exception as e:
        err_type, err_value, err_tb = sys.exc_info()
        err = "".join(traceback.format_exception(err_type, err_value, err_tb))
        return {"error": err}
