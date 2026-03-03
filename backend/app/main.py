from fastapi import FastAPI

app = FastAPI(title="Clash of Code API")

@app.get("/")
async def root():
    return {"message": "Clash of Code Backend Running 🚀"}