from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.routers import riders, drivers, rides

app = FastAPI(
    title="Ride-Sharing Platform API",
    description="API for the Ride-Sharing Platform with SOLID principles and design patterns",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(riders.router, prefix="/api/riders", tags=["riders"])
app.include_router(drivers.router, prefix="/api/drivers", tags=["drivers"])
app.include_router(rides.router, prefix="/api/rides", tags=["rides"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Ride-Sharing Platform API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True) 