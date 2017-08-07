from sqlalchemy import MetaData, create_engine, Table, text, func, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///PTM.db')
metadata = MetaData(bind=engine)
Base.metadata = metadata
metadata.reflect()
Ptms = Table('ptms', metadata, autoload=True, autoload_with=engine)


file = open('output.csv', 'w')


# Query
Session = sessionmaker(bind=engine)
session = Session()


print('\n')


# Select all
query = session.query(Ptms).limit(5)
columns = [x.name for x in Ptms.columns]
print("{: >5} {: >20} {: >20} {: >100} {: >10} {: >10} {: >10} {: >10} {: >10} {: >15} {: >20} {: >20} ".format(*columns))
for i in query:
    print("{: >5} {: >20} {: >20} {: >100} {: >10} {: >10} {: >10} {: >10} {: >10} {: >15} {: >20} {: >20} ".format(*i))


print('\n')
file.write('\n')


# Count by type
types = session.query(func.count(Ptms.columns.type), Ptms.columns.type).group_by(Ptms.columns.type).all()
print("{: >20} {: <20}".format(*['Count', 'Type']))
for i in types:
    print("{: >20} {: <20}".format(*i))
    file.write('$'.join([str(x) for x in i])+'\n')

#"""
print('\n')
file.write('\n')


# Count crosslinks
crosslinks = session.query(
                    func.count(Ptms.columns.description).label('Count'),
                    Ptms.columns.description,
                    Ptms.columns.type).\
                filter(text("type='cross-link'")).\
                order_by(desc(text('Count'))).\
                group_by(Ptms.columns.description)

print("{: >20} {: <100} {: <100}".format(*['Count', 'Residue', 'Type']))
for i in crosslinks:
    print("{: >20} {: <100} {: <100}".format(*i))
    file.write('$'.join([str(x) for x in i]) + '\n')


print('\n')
file.write('\n')


# Count AA modifications
modifications = session.query(
                    func.count(Ptms.columns.description).label('Count'),
                    Ptms.columns.description,
                    Ptms.columns.type).\
                filter(text("type='modified residue'")).\
                order_by(desc(text('Count'))).\
                group_by(Ptms.columns.description)

print("{: >20} {: <100} {: <100}".format(*['Count', 'Residue', 'Type']))
for i in modifications:
    print("{: >20} {: <100} {: <100}".format(*i))
    file.write('$'.join([str(x) for x in i]) + '\n')


print('\n')
file.write('\n')


# Count AA Glycosylations by Residue
glycosylations = session.query(
    func.count(Ptms.columns.description).label('Count'),
    Ptms.columns.start_res,
    Ptms.columns.type). \
    filter(text("type='glycosylation site'")). \
    order_by(desc(text('Count'))). \
    group_by(Ptms.columns.start_res)

print("{: >20} {: <100} {: <100}".format(*['Count', 'Description', 'Type']))
for i in glycosylations:
    print("{: >20} {: <100} {: <100}".format(*i))
    file.write('$'.join([str(x) for x in i]) + '\n')


print('\n')
file.write('\n')


# Count AA Glycosylations
glycosylations = session.query(
    func.count(Ptms.columns.id).label('Count'),
    Ptms.columns.description,
    Ptms.columns.start_res,
    Ptms.columns.type). \
    filter(text("type='glycosylation site'")). \
    order_by(desc(text('Count'))). \
    group_by(Ptms.columns.description)

print("{: >20} {: <75} {: <10} {: <10}".format(*['Count', 'Description', 'Resiude', 'Type']))
for i in glycosylations:
    print("{: >20} {: <75} {: <10} {: <10}".format(*i))
    file.write('$'.join([str(x) for x in i]) + '\n')


print('\n')
file.write('\n')


# Count disulfide bonds
disulfides = session.query(
                    func.count(Ptms.columns.description).label('Count'),
                    Ptms.columns.description,
                    Ptms.columns.type).\
                filter(text("type='disulfide bond'")).\
                order_by(desc(text('Count'))).\
                group_by(Ptms.columns.description)

print("{: >20} {: <100} {: <100}".format(*['Count', 'Residue', 'Type']))
for i in disulfides:
    print("{: >20} {: <100} {: <100}".format(*i))
    file.write('$'.join([str(x) for x in i])+'\n')


print('\n')
file.write('\n')


# Count lipidations
lipidations = session.query(
                    func.count(Ptms.columns.description).label('Count'),
                    Ptms.columns.description,
                    Ptms.columns.type,
                    Ptms.columns.start_res).\
                filter(text("type='lipid moiety-binding region'")).\
                order_by(desc(text('Count'))).\
                group_by(Ptms.columns.description)

print("{: >20} {: <70} {: <30} {: <30}".format(*['Count', 'Description', 'Res', 'Type']))
for i in lipidations:
    print("{: >20} {: <70} {: <30} {: <30}".format(*i))
    file.write('$'.join([str(x) for x in i]) + '\n')


file.close()
#hola