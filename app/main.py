from fastapi import FastAPI
from app.routers import fhir  # Import the new router

app = FastAPI()

# ✅ Register Routers
app.include_router(fhir.router)

@app.get("/")
def health_check():
    return {"message": "✅ FastAPI server is running!"}