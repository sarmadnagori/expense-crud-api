from fastapi import FastAPI
from pydantic import BaseModel,Field
from fastapi import HTTPException

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()      # reads the .env file into the environment

# now read each value
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")




conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id SERIAL PRIMARY KEY,
    description TEXT,
    amount INTEGER
)
""")

conn.commit()
conn.close()




app = FastAPI()

class Expense(BaseModel):
    description:str = Field(min_length=1)
    amount:int = Field(gt=0)


   

class ExpenseUpdate(BaseModel):    # for UPDATING — needs id
    
    amount: int

class ExpenseDelete(BaseModel):
    id: int



@app.get("/expenses/{id}")
def get_expense(id: int):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST)
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, amount FROM expenses WHERE id=%s", (id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"id": row[0], "description": row[1], "amount": row[2]}



@app.post("/expenses", status_code=201)
def add_expense(expense: Expense):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (description, amount) VALUES (%s, %s) RETURNING id",
        (expense.description, expense.amount)
    )
    new_id = cursor.fetchone()[0]        # grab the id the database generated
    conn.commit()
    conn.close()
    return {"id": new_id, "description": expense.description, "amount": expense.amount}


@app.put("/expenses/{id}")
def update_expenses(id: int, expense: ExpenseUpdate):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE expenses SET amount=%s WHERE id=%s RETURNING id, description, amount",
        (expense.amount, id)
    )
    row = cursor.fetchone()          # the actual updated row from the DB
    if row is None:                  # nothing matched → didn't exist
        conn.close()
        raise HTTPException(status_code=404, detail="Expense not found")
    conn.commit()
    conn.close()
    return {"id": row[0], "description": row[1], "amount": row[2]}

@app.delete("/expenses/{id}", status_code=204)
def del_expense(id: int):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=%s", (id,))
    if cursor.rowcount == 0:  
        conn.close()                  # nothing was deleted → didn't exist
        raise HTTPException(status_code=404, detail="Expense not found")
    conn.commit()
    conn.close()
  
    

