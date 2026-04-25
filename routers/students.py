from fastapi import APIRouter,HTTPException
from schemas import Student,UpdateStudent
import sqlite3

router = APIRouter()

@router.post("/addstudent")
def add_student(student:Student):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
    Insert into students (id,name,age,major,gpa)
    Values(?,?,?,?,?)

                   """,(student.id,student.name,student.age,student.major,student.gpa)
)
    conn.commit()
    conn.close()
    return {"message": "Student successfully added"}
@router.get("/readstudents")
def show_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("Select * From Students")
    rows = cursor.fetchall()
    conn.close()
    return{
         "students":rows
    }
    

@router.get("/students/{id}")
def student_search(id:int):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("Select * from students where id = ?",(id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404,detail="Student not found")
    return{
        "student":row
    }
    
    

@router.delete("/deletestudent/{id}")
def remove_student(id:int):
     conn = sqlite3.connect("students.db")
     cursor = conn.cursor()
     cursor.execute("DELETE FROM students WHERE id = ?", (id,))
     conn.commit()
     conn.close()
     return{
          "message":"Student successfully deleted"
     }
    
        
    
@router.patch("/updatestudent/{id}")
def update_student(id: int, student: UpdateStudent):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        raise HTTPException(status_code=404,detail="Student not found")

    updated_name = student.name if student.name is not None else row[1]
    updated_age = student.age if student.age is not None else row[2]
    updated_major = student.major if student.major is not None else row[3]
    updated_gpa = student.gpa if student.gpa is not None else row[4]

    cursor.execute("""
    UPDATE students
    SET name = ?, age = ?, major = ?, gpa = ?
    WHERE id = ?
    """, (updated_name, updated_age, updated_major, updated_gpa, id))

    conn.commit()
    conn.close()

    return {
        "message": "Student updated successfully",
        "student": {
            "id": id,
            "name": updated_name,
            "age": updated_age,
            "major": updated_major,
            "gpa": updated_gpa
        }
    }