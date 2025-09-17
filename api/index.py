from fastapi import FastAPI, Request
from api.functions import get_teachers, get_month_data
import httpx

app = FastAPI()

# ===== Эндпоинт статистики =====
@app.get("/api/data")
async def get_data(request: Request, month: int):
    try:
        output = await get_month_data(month)
        return output   # ✅ возвращаем словарь с данными
    except Exception as e:
        print("❌ Ошибка в get_data:", e)
        return {"error": str(e)}   # ✅ возвращаем текст ошибки в JSON

# ===== Эндпоинт преподавателей =====
@app.get("/api/teachers")
async def get_teachers_list(request: Request):
    try:
        async with httpx.AsyncClient() as client:
            teachers = await get_teachers(client)
            teachers = list(map(lambda teacher: teacher["name"], teachers))
            return teachers
    except Exception as e:
        print("❌ Ошибка в get_teachers:", e)
        return {"error": str(e)}
