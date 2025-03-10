from fastapi import FastAPI
from app.routers import fax

app = FastAPI()

# Include the fax router
app.include_router(fax.router)

@app.get("/")
def root():
    return {"message": "Veritas One API is running!"}