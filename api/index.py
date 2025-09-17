from fastapi import FastAPI, Request
from api.functions import get_teachers, get_month_data
import httpx
import traceback
import sys

app = FastAPI()

# ===== Эндпоинт статистики =====
@app.get("/api/data")
async def get_data(request: Request, month: int):
    try:
        print(f"📅 Запрос данных за месяц: {month}")
        output = await get_month_data(month)
        print("✅ Успешно получили данные")
        return output
    except Exception as e:
        err_type, err_value, err_tb = sys.exc_info()
        err = "".join(traceback.format_exception(err_type, err_value, err_tb))
        print("❌ Полная ошибка в get_data:\n", err)
        return {"error": err}


# ===== Эндпоинт преподавателей =====
@app.get("/api/teachers")
async def get_teachers_list(request: Request):
    try:
        async with httpx.AsyncClient() as client:
            teachers = await get_teachers(client)
            teachers = list(map(lambda teacher: teacher["name"], teachers))
            return teachers
    except Exception as e:
        err_type, err_value, err_tb = sys.exc_info()
        err = "".join(traceback.format_exception(err_type, err_value, err_tb))
        print("❌ Полная ошибка в get_teachers:\n", err)
        return {"error": err}
