from fastapi import FastAPI, Request
from api.functions import get_month_data, get_teachers
import traceback, sys

app = FastAPI()

@app.get("/api/data")
async def get_data(month: int, year: int = None):
    try:
        output = await get_month_data(month)
        return output
    except Exception as e:
        err_type, err_value, err_tb = sys.exc_info()
        err = "".join(traceback.format_exception(err_type, err_value, err_tb))
        return {"error": err}

@app.get("/api/teachers")
async def get_teachers_list():
    try:
        teachers = await get_teachers(None)
        return teachers
    except Exception as e:
        err_type, err_value, err_tb = sys.exc_info()
        err = "".join(traceback.format_exception(err_type, err_value, err_tb))
        return {"error": err}
