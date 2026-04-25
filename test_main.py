from fastapi.testclient import TestClient
from main import app
import sqlite3
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students")
    conn.commit()
    conn.close()
    yield

def test_add_student():
    response = client.post("/addstudent", json={
        "id": 1,
        "name": "John",
        "age": 20,
        "major": "Computer Science",
        "gpa": 3.5
    })
    assert response.status_code == 200

def test_get_all_students():
    response = client.get("/readstudents")
    assert response.status_code == 200

def test_get_student():
    client.post("/addstudent", json={"id": 1, "name": "John", "age": 20, "major": "CS", "gpa": 3.5})
    response = client.get("/students/1")
    assert response.status_code == 200

def test_get_student_not_found():
    response = client.get("/students/9999")
    assert response.status_code == 404

def test_delete_student():
    client.post("/addstudent", json={"id": 1, "name": "John", "age": 20, "major": "CS", "gpa": 3.5})
    response = client.delete("/deletestudent/1")
    assert response.status_code == 200