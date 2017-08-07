from sqlalchemy import MetaData, create_engine, Table, text, func, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///PTM.db')
metadata = MetaData(bind=engine)
Base.metadata = metadata
metadata.reflect()
Ptms = Table('ptms', metadata, autoload=True, autoload_with=engine)

Session = sessionmaker(bind=engine)
session = Session()

query = session.query(Ptms.columns.id, Ptms.columns.description).\
    filter(text("type='disulfide bond' or type='cross-link'")).\
    order_by(Ptms.columns.id)


print("{: <40} {: <40} {: <40}".format(*['Clean', 'Raw', 'Id\n']))

n = 0
j = 0

for row in query:
    if 'interchain' in row[1]:
        clean = row[1][0:row[1].find('interchain')-2]
        update_statement = Ptms.update().where(Ptms.columns.id == row[0]).values(description=clean)
        session.execute(update_statement)
        print("{: <40} {: <40} {: <40}".format(*[clean, row[1], row[0]]))
    #else: print("{: <40} {: <40} {: <40}".format(*[row[1], row[1], row[0]]))

    n += 1

    if n/1000 >= j:
        j += 1
        print(n)
        session.commit()

session.commit()