from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Text,
    TIMESTAMP,
    ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from database import Base




class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    encyclopedias = relationship(
        "Encyclopedia",
        back_populates="creator",
        cascade="all, delete-orphan"
    )


class Encyclopedia(Base):
    __tablename__ = "encyclopedias"

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)

    created_by = Column(
        BigInteger,
        ForeignKey("user.id"),
        nullable=False,
        index=True
    )

    created_at = Column(TIMESTAMP, server_default=func.now())

    creator = relationship(
        "User",
        back_populates="encyclopedias"
    )

    collections = relationship(
        "Collection",
        back_populates="encyclopedia",
        cascade="all, delete-orphan"
    )


class Collection(Base):
    __tablename__ = "collection"

    id = Column(BigInteger, primary_key=True)
    

    encyclopedia_id = Column(
        BigInteger,
        ForeignKey("encyclopedias.id"),
        nullable=False,
        index=True
    )

    name = Column(String, nullable=False)
    description = Column(Text)
    configuration = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    encyclopedia = relationship(
        "Encyclopedia",
        back_populates="collections"
    )

    elements = relationship(
        "Element",
        back_populates="collection",
        cascade="all, delete-orphan"
    )

class Element(Base):
    __tablename__ = "element"

    id = Column(BigInteger, primary_key=True, index = True)

    name = Column(String, nullable=False)
    description = Column(Text)    
    data = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    collection_id = Column(
        BigInteger,
        ForeignKey("collection.id"),
        nullable=False,
        index=True
    )


    collection = relationship(
        "Collection",
        back_populates="elements"
        )


class Tag(Base):
    __tablename__ = "tag"

    id = Column(BigInteger, primary_key=True, index = True)
    name = Column(String, nullable=False)
    description = Column(Text)  
    created_at = Column(TIMESTAMP, server_default=func.now())

