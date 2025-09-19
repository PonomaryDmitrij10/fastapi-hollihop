from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "🚀 FastAPI работает!"}

@app.get("/ping")
async def ping():
    return {"status": "ok"}

@app.get("/api/data")
async def get_data(month: int = 1, year: int = 2025):
    return {"month": month, "year": year, "data": "тестовые данные"}
