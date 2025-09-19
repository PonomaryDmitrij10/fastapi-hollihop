from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "🚀 FastAPI работает!"}

@app.get("/ping")
async def ping():
    return {"status": "ok"}
