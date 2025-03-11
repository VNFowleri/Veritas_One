from fastapi import FastAPI
from app.routers import fax, ifax  # Now we have both fax and ifax routers

app = FastAPI()

# Include the routers
app.include_router(fax.router)
app.include_router(ifax.router)  # This line registers the iFax endpoints

@app.get("/")
def root():
    return {"message": "Veritas One API is running!"}