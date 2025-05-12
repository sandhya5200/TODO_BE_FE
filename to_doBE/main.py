import psycopg2
from psycopg2.extras import RealDictCursor 
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="thrymr@123",  
    database="todo",  
    port="5432" 
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.post("/add_task")
def add_task(task: str = Form(...)):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todo (task) VALUES (%s)", (task,))
    conn.commit()
    cursor.close()  
    return {"message": "Added Successfully"}

@app.post("/delete_task")
def delete_task(id: int = Form(...)): 
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todo WHERE id=%s", (id,))
    conn.commit()
    cursor.close() 
    return {"message": "Deleted Successfully"}

@app.get("/get_task")
def get_task(id: int = None):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        if id is not None:
            cursor.execute("SELECT * FROM todo WHERE id = %s", (id,))
        else:
            cursor.execute("SELECT * FROM todo")
        records = cursor.fetchall()
        return records
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()


