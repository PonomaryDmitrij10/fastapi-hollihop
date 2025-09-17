from fastapi import FastAPI, Request
from api.functions import get_teachers, get_month_data
import httpx
import traceback

app = FastAPI()

# ===== Эндпоинт статистики =====
@app.get("/api/data")
async def get_data(request: Request, month: int):
    try:
        output = await get_month_data(month)
        return output   # ✅ возвращаем данные в виде массива массивов
    except Exception as e:
        err = traceback.format_exc()   # полный текст ошибки
        print("❌ Ошибка в get_data:", err)
        return {"error": err}          # ✅ вернём строку с ошибкой в JSON


# ===== Эндпоинт преподавателей =====
@app.get("/api/teachers")
async def get_teachers_list(request: Request):
    try:
        async with httpx.AsyncClient() as client:
            teachers = await get_teachers(client)
            teachers = list(map(lambda teacher: teacher["name"], teachers))
            return teachers
    except Exception as e:
        err = traceback.format_exc()
        print("❌ Ошибка в get_teachers:", err)
        return {"error": err}
