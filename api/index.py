from fastapi import FastAPI, Request
from api.functions import get_month_data, get_teachers
import traceback, sys, httpx

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "🚀 FastAPI работает!"}


@app.get("/ping")
async def ping():
    return {"status": "ok"}


@app.get("/api/data")
async def get_data(month: int, year: int):
    try:
        output = await get_month_data(month, year)
        return output
    except Exception as e:
        err_type, err_value, err_tb = sys.exc_info()
        err = "".join(traceback.format_exception(err_type, err_value, err_tb))
        return {"error": str(e), "trace": err}


@app.get("/api/teachers")
async def get_teachers_list(request: Request):
    try:
        async with httpx.AsyncClient() as client:
            teachers = await get_teachers(client)
            teachers = [t["name"] for t in teachers]
            return teachers
    except Exception as e:
        err_type, err_value, err_tb = sys.exc_info()
        err = "".join(traceback.format_exception(err_type, err_value, err_tb))
        return {"error": str(e), "trace": err}
