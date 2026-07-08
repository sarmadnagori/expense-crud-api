from fastapi import FastAPI
from pydantic import BaseModel
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
    description:str
    amount:int


   

class ExpenseUpdate(BaseModel):    # for UPDATING — needs id
    id: int
    amount: int

class ExpenseDelete(BaseModel):
    id: int



@app.get ("/expenses")
def get_expenses():

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    
    rows=cursor.fetchall()
    expenses = []
    for row in rows:
        expenses.append({"id": row[0], "description": row[1], "amount": row[2]})
       
    conn.close()
    return {"expenses": expenses}



@app.post("/expenses")
def add_expense(expense: Expense):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (description, amount) VALUES (%s, %s)",
        (expense.description, expense.amount)
    )
    conn.commit()      # save the INSERT
    conn.close()
    return {"message": "Expense added"}

@app.put("/expenses/{id}")

def update_expenses(id:int,expense:ExpenseUpdate):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST)
    cursor= conn.cursor()
    cursor.execute("UPDATE expenses SET amount=%s WHERE id=%s ",(expense.amount,id))
    if cursor.rowcount == 0: 
        conn.close()                   # nothing was deleted → didn't exist
        raise HTTPException(status_code=404, detail="Expense not found")
    conn.commit()
    conn.close()
    return {"message":"updated expenses"}

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
  
    

