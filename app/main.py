from fastapi import FastAPI;
from app.routes import auth;
from app.db.database import create_users_table
app = FastAPI();

@app.get("/")
def read_root():
    return {"Health Check", "Ok"}

create_users_table()
app.include_router(auth.router, prefix="/auth")
