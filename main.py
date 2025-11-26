from fastapi import FastAPI, Depends, HTTPException
from schemas import Todo as TodoSchema,TodoCreate
from sqlalchemy.orm import Session
from database import sessionLocal, Base , engine
from models import Todo
Base.metadata.create_all(bind =engine) 

app = FastAPI()
# Dependency for DB Session
def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()



#POST - Create Todo
@app.post("/todos", response_model=TodoSchema)
def create(todo: TodoCreate, db:Session = Depends(get_db)):

    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo



#GET-ALL Todos
@app.get("/todos", response_model=list[TodoSchema])

def getAll(db: Session = Depends(get_db)):
        return db.query(Todo).all()



#GET - Get Single Data
@app.get("/todos/{todo_id}",response_model=TodoSchema)

def getById(todo_id: int , db:Session =Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id==todo_id).first()
    if not todo:
         raise HTTPException(status_code=404, detail="Id Not Found")
    return todo



#PUT - Update Todo
@app.put("/todos/{todo_id}", response_model=TodoSchema)

def update(todo_id:int , updated: TodoCreate, db:Session = Depends(get_db)):
    todo= db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
         raise HTTPException(status_code=404 , detail="Todo Id Not Found")
    for key, value in updated.dict().items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo


#DELETE - Delete Todo
@app.delete("/todos/{todo_id}")

def deleteById(todo_id:int , db:Session=Depends(get_db)):
     
    delObj= db.query(Todo).filter(Todo.id == todo_id).first()
    if not delObj:
          raise HTTPException(status_code=404 , detail="Todo Id Not Found")
    
    db.delete(delObj)
    db.commit()
    return {"Message" : "Data Deleted..."}