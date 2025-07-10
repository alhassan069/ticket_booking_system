from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, Float, Date, String, func
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional
from datetime import date as dt_date, timedelta
from pydantic import BaseModel

# Database Configuration

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)

# Pydantic models for request/response
class ExpenseCreate(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None
    expense_date: dt_date = dt_date.today()

class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    date: Optional[dt_date] = None
    category: Optional[str] = None
    description: Optional[str] = None

Base.metadata.create_all(bind=engine)

# Add sample data if database is empty
def add_sample_data():
    db = SessionLocal()
    try:
        # Check if expenses table is empty
        expense_count = db.query(Expense).count()
        if expense_count == 0:
            
            sample_expenses = [
                Expense(amount=25.50, date=dt_date.today() - timedelta(days=1), category="Food", description="Lunch at restaurant"),
                Expense(amount=45.00, date=dt_date.today() - timedelta(days=2), category="Transport", description="Gas station"),
                Expense(amount=120.00, date=dt_date.today() - timedelta(days=3), category="Bills", description="Electricity bill"),
                Expense(amount=15.99, date=dt_date.today() - timedelta(days=4), category="Entertainment", description="Movie ticket"),
                Expense(amount=89.99, date=dt_date.today() - timedelta(days=5), category="Shopping", description="New clothes"),
                Expense(amount=12.50, date=dt_date.today(), category="Food", description="Coffee and breakfast"),
            ]
            
            for expense in sample_expenses:
                db.add(expense)
            
            db.commit()
            print("Sample data added to database")
    except Exception as e:
        print(f"Error adding sample data: {e}")
    finally:
        db.close()

# Add sample data on startup
add_sample_data()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return FileResponse("static/index.html")



@app.get("/expenses")
def get_expenses(
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    '''
    Fetch all expenses with optional date range filtering
    '''
    query = db.query(Expense)
    
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)
    
    expenses = query.all()
    return expenses

@app.post("/expenses")
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    '''
    Create a new expense with amount, category, and description. If no date is provided, it will default to today's date.
    '''
    new_expense = Expense(amount=expense.amount, date=expense.expense_date, category=expense.category, description=expense.description)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: ExpenseUpdate, db: Session = Depends(get_db)):
    '''
    Update an existing expense
    '''
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    # Update only provided fields
    if expense.amount is not None:
        db_expense.amount = expense.amount
    if expense.date is not None:
        db_expense.date = expense.date
    if expense.category is not None:
        db_expense.category = expense.category
    if expense.description is not None:
        db_expense.description = expense.description
    
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    '''
    Delete an expense
    '''
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(db_expense)
    db.commit()
    return {"message": "Expense deleted successfully"}

@app.get("/expenses/category/{category}")
def get_expenses_by_category(category: str, db: Session = Depends(get_db)):
    '''
    Filter expenses by category
    '''
    expenses = db.query(Expense).filter(Expense.category == category).all()
    return expenses

@app.get("/expenses/total")
def get_total_expenses(db: Session = Depends(get_db)):
    '''
    Get total expenses
    '''
    total = db.query(func.sum(Expense.amount)).scalar()
    return {"total": total}
