from sqlalchemy.orm import Session
from models import User, Encyclopedia, Collection, Element, Tag
from schemas import UserCreate, EncyclopediaCreate, CollectionCreate, ElementCreate, TagCreate

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        password=user.password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_encyclopedia(db: Session, data: EncyclopediaCreate):
    user = db.query(User).filter(User.id == data.created_by).first()
    if not user:
        return None

    encyclopedia = Encyclopedia(
        name=data.name,
        description=data.description,
        created_by=data.created_by
    )

    db.add(encyclopedia)
    db.commit()
    db.refresh(encyclopedia)
    return encyclopedia

def create_collection(db: Session, data: CollectionCreate):
    encyclopedia = db.query(Encyclopedia).filter(Encyclopedia.id == data.encyclopedia_id).first()
    if not encyclopedia:
        return None

    collection = Collection(
        name=data.name,
        description=data.description,
        encyclopedia_id=data.encyclopedia_id,
        configuration=data.configuration
    )

    db.add(collection)
    db.commit()
    db.refresh(collection)
    return collection

def create_element(db: Session, data: ElementCreate):
    collection = db.query(Collection).filter(Collection.id == data.collection_id).first()
    if not collection:
        return None

    element = Element(
        name=data.name,
        description=data.description,
        data=data.data,
        collection_id=data.collection_id,
    )

    db.add(element)
    db.commit()
    db.refresh(element)
    return element

def create_tag(db: Session, data: TagCreate):
    tag = Tag(
        name=data.name,
        description=data.description,
    )

    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

def delete_element(db: Session, element_id: int):
    element = db.query(Element).filter(Element.id == element_id).first()

    if not element:
        return None
    
    db.delete(element)
    db.commit()
    return element
