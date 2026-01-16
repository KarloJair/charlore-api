from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
import models, schemas, crud
from database import SessionLocal, engine
import auth
from auth import get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service")
app.include_router(auth.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/", status_code=status.HTTP_200_OK)
async def user(
    user: user_dependency, 
    db: db_dependency
    ):
    return {"User": user}


@app.post("/encyclopedias", response_model=schemas.EncyclopediaResponse)
def create_encyclopedia(
    encyclopedia: schemas.EncyclopediaCreate,
    db: db_dependency,
    user: user_dependency
):
    result = crud.create_encyclopedia(db, encyclopedia)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return result

@app.post("/collections", response_model=schemas.CollectionResponse)
def create_collection(
    collection: schemas.CollectionCreate,
    db: db_dependency,
    user: user_dependency
):
    result = crud.create_collection(db, collection)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Enciclopedia no encontrada"
        )

    return result

@app.post("/elements", response_model=schemas.ElementResponse)
def create_element(
    element: schemas.ElementCreate,
    db: db_dependency,
    user: user_dependency
):
    result = crud.create_element(db, element)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Enciclopedia no encontrada"
        )

    return result

@app.post("/tags", response_model=schemas.TagResponse)
def create_tag(
    tag: schemas.TagCreate,
    db: db_dependency,
    user: user_dependency
):
    result = crud.create_tag(db, tag)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="La tag no se ha podido crear"
        )

    return result

@app.get("/encyclopedias/{user_id}", response_model=list[schemas.EncyclopediaResponse])
def read_encyclopedias(
    user_id: int, 
    db: db_dependency,
    user: user_dependency
    ):

    result = db.query(models.Encyclopedia).filter(models.Encyclopedia.created_by == user_id).all()
    if not result:
        raise HTTPException(status_code=404, detail='Enciclopedia no encontrada')
    return result

@app.get("/collections/{encyclopedia_id}", response_model=list[schemas.CollectionResponse])
def read_collections(
    encyclopedia_id: int, 
    db: db_dependency,
    user: user_dependency
    ):

    result = db.query(models.Collection).filter(models.Collection.encyclopedia_id == encyclopedia_id).all()
    if not result:
        raise HTTPException(status_code=404, detail='Coleccion no encontrada')
    return result

@app.get("/elements/{collection_id}", response_model=list[schemas.ElementsResponse])
def read_elements(
    collection_id: int, 
    db: db_dependency,
    user: user_dependency
    ):

    result = db.query(models.Element).filter(models.Element.collection_id == collection_id).all()
    if not result:
        raise HTTPException(status_code=404, detail='Elementos no encontrado')
    return result

@app.get("/element/{element_id}", response_model=schemas.ElementResponse)
def read_element(
    element_id: int, 
    db: db_dependency,
    user: user_dependency
    ):

    result = db.query(models.Element).filter(models.Element.id == element_id).first()
    if not result:
        raise HTTPException(status_code=404, detail='Elemento no encontrado')
    return result


@app.patch("/element/{element_id}", response_model=schemas.ElementResponse)
def update_element(
    element_id: int,
    element: schemas.ElementUpdate,
    db: db_dependency,
    user: user_dependency    
):
    db_element = db.query(models.Element).filter(
        models.Element.id == element_id
    ).first()

    if not db_element:
        raise HTTPException(status_code=404, detail="Elemento no encontrado")

    # Actualizar solo los campos enviados
    update_data = element.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_element, key, value)

    db.commit()
    db.refresh(db_element)

    return db_element
    
@app.delete("/element_delete/{element_id}", status_code=204)
def delete_element(
    element_id: int,
    db: db_dependency,
    user: user_dependency
):
    element = crud.delete_element(db, element_id)

    if not element:
        raise HTTPException(status_code=404,detail="Elemento no encontrado")