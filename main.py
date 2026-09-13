from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List

app = FastAPI(title="Clinical Triage API")
DB_FILE = "triage.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS patients
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       name
                       TEXT
                       NOT
                       NULL,
                       age
                       INTEGER
                       NOT
                       NULL,
                       urgency_score
                       INTEGER
                       NOT
                       NULL,
                       notes
                       TEXT
                   )
                   """)
    conn.commit()
    conn.close()


init_db()

class PatientInput(BaseModel):
    name: str
    age: int
    pain_level: int  # 1 to 10
    notes: str


class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    urgency_score: int
    notes: str

def calculate_urgency(age: int, pain_level: int) -> int:
    score = pain_level * 10
    if age > 65 or age < 5:
        score += 20
    return min(score, 100)

@app.post("/patients", response_model=PatientResponse, status_code=201)
def create_patient(patient: PatientInput):
    urgency = calculate_urgency(patient.age, patient.pain_level)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO patients (name, age, urgency_score, notes) VALUES (?, ?, ?, ?)",
        (patient.name, patient.age, urgency, patient.notes)
    )
    conn.commit()
    patient_id = cursor.lastrowid
    conn.close()

    return PatientResponse(
        id=patient_id,
        name=patient.name,
        age=patient.age,
        urgency_score=urgency,
        notes=patient.notes
    )


@app.get("/patients", response_model=List[PatientResponse])
def get_patients():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age, urgency_score, notes FROM patients ORDER BY urgency_score DESC")
    rows = cursor.fetchall()
    conn.close()

    return [
        PatientResponse(id=r[0], name=r[1], age=r[2], urgency_score=r[3], notes=r[4])
        for r in rows
    ]


@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"status": "success", "message": f"Patient {patient_id} removed"}
