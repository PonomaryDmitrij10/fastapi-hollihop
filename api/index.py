from fastapi import FastAPI, Request
from api.functions import get_month_data
import traceback
import sys

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "🚀 FastAPI работает!"}

@app.get("/ping")
async def ping():
    return {"status": "ok"}

@app.get("/api/data")
async def get_data(request: Request, month: int, year: int = 2025):
    try:
        # передаём и month, и year
        output = await get_month_data(month, year)
        if not output or len(output) == 1:  # только заголовки, данных нет
            return {"error": f"Нет данных за {month}/{year}"}
        return {"data": output}
    except Exception as e:
        err_type, err_value, err_tb = sys.exc_info()
        err = "".join(traceback.format_exception(err_type, err_value, err_tb))
        return {"error": str(e), "traceback": err}
