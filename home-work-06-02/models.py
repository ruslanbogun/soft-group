from sqlalchemy import Column, ForeignKey, Integer, String, Text, Numeric, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    __table_args__ = (
        Index('idx_name', name),
    )


class Messages(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    url = Column(String(250), nullable=False)
    title = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text)
    price = Column(Numeric(10, 2))
    currency = Column(String(50))

    __table_args__ = (
        Index('idx_title_author_id', title, author_id),
    )


if __name__ == '__main__':
    # Create an engine that stores data in the local directory's
    # example.db file.
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)
