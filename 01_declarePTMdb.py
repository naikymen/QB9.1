from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Ptms(Base):
    __tablename__ = 'ptms'
    id = Column('id', Integer, primary_key=True)
    record_id = Column(String)
    type = Column(String)
    description = Column(String)
    evidence = Column(String)
    start_pos = Column(Integer)
    end_pos  = Column(Integer)
    start_res = Column(String(1))
    end_res  = Column(String(1))
    protein_id = Column(String)
    protein_name = Column(String)
    protein_tax = Column(String)


engine = create_engine('sqlite:///PTM.db')  # Core interface to the database

#engine.echo = False  # Do not print all of the executed SQL
#metadata = MetaData(engine)
#metadata.create_all(engine)

Base.metadata.create_all(engine)