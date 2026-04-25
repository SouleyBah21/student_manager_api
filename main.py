from fastapi import FastAPI
from schemas import Student,UpdateStudent
from database import init_db
from routers import students
init_db()
    
app = FastAPI()

app.include_router(students.router)