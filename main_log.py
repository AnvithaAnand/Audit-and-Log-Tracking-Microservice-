import time
import sqlalchemy.exc
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models, database, routes

# Function to try database connection with retries
def connect_with_retry(retries=5, delay=5):
    for attempt in range(retries):
        try:
            print(f"Attempting database connection... (attempt {attempt+1}/{retries})")
            # Check connection by creating tables
            models.Base.metadata.create_all(bind=database.engine)
            print("Database connection successful!")
            return True
        except sqlalchemy.exc.OperationalError as e:
            if attempt < retries - 1:
                print(f"Database connection failed: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"Database connection failed after {retries} attempts: {e}")
                # Continue with application startup even if DB connection fails
                # We'll handle connection errors at the route level
                return False

# Try to connect to the database with retries
connect_with_retry()

app = FastAPI(title="Log Microservice")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"message": "Log Microservice API"}

@app.get("/health")
def health_check():
    try:
        # Try a simple database query to check connectivity
        with database.SessionLocal() as db:
            db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}