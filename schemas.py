from typing import Optional
from pydantic import BaseModel

class Student(BaseModel):
    id:int 
    name:str 
    age:int 
    major:str 
    gpa:float 

class UpdateStudent(BaseModel):
    name:Optional[str] = None 
    age:Optional[int] = None 
    major:Optional[str] = None
    gpa:Optional[float] = None