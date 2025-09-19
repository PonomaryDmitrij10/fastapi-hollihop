from fastapi import FastAPI, Request
from api.functions import get_month_data
import traceback
import sys

app = FastAPI()

# ===== Эндпоинт статистики =====
@app.get("/api/data")
async def get_data(request: Request, month: int, year: int):
    try:
        print(f"📅 Запрос данных за {month}/{year}")
        output = await get_month_data(month, year)
        print("✅ Успешно получили данные")
        return output
    except Exception as e:
        err_type, err_value, err_tb = sys.exc_info()
        err = "".join(traceback.format_exception(err_type, err_value, err_tb))
        print("❌ Полная ошибка в get_data:\n", err)
        return {"error": err}
