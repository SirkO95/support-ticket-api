from fastapi import FastAPI
from .database import engine, Base
from .routers import tickets

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Support Ticket API",
    description="Simple Support Ticket System ",
    version="1.0.0"
)

app.include_router(tickets.router)

@app.get("/")
def root():
    return {"message": "Support Ticket API is running"}