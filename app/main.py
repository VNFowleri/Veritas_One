from fastapi import FastAPI
from app.routers import patient

app = FastAPI()

# Include the patient router
app.include_router(patient.router)

@app.get("/")
def health_check():
    return {"message": "✅ FastAPI server is running!"}