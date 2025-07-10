from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from models.database import engine, Base
from routes import venues, events, tickets, bookings


# Create the database tables
Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI()

# Handle CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Mount the static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include the routes
app.include_router(venues.router)
app.include_router(events.router)
app.include_router(tickets.router)
app.include_router(bookings.router)

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

