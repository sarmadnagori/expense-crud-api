from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3



app = FastAPI()

class Expense(BaseModel):
    description:str
    amount:int





# --- create the table once , when the app starts--


conn = sqlite3.connect("expenses.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY,
    description TEXT,
    amount INTEGER 

)

""") 


conn.commit()
conn.close()

@app.get ("/expenses")
def get_expenses():

    conn= sqlite3.connect("expenses.db")
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
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (description, amount) VALUES (?, ?)",
        (expense.description, expense.amount)
    )
    conn.commit()      # save the INSERT
    conn.close()
    return {"message": "Expense added"}

@app.put("/expenses")

def update_expenses(expense:Expense):
    conn = sqlite3.connect("expenses.db")
    cursor= conn.cursor()
    cursor.execute("UPDATE expenses SET amount=? WHERE description=? ",(expense.amount,expense.description))
    conn.commit()
    conn.close()
    return {"message":"updated expenses"}

@app.delete("/expenses")
def del_expenses(expense:Expense):
    conn=sqlite3.connect("expenses.db")
    cursor=conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE description=?",(expense.description,))
    conn.commit()
    conn.close()
    return {"message": "expense deleted"}