from sqlalchemy import MetaData, create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Bio import SeqIO
import gzip
import time

start_time = time.time()
print('Start: ', int(start_time))

from declarePTMdb import Base, Ptms  # PyCharm marca referencias sin resolver,
# pero Python si encuentra el script que está en esta misma carpeta y contiene las definiciones.

engine = create_engine('sqlite:///PTM.db')
engine.echo = False  # Do not print all of the executed SQL

Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()

#new_entry = Ptms(type='cross link', description='tan cerca y tan lejos')
#session.add(new_entry)
#session.commit()

# Abrir el archivo de SwissProt
gzHandle = gzip.open("../uniprot_sprot.xml.gz", 'rt')
records = SeqIO.parse(gzHandle,"uniprot-xml")
i, n, j = 0, 555000, 0  # limit parsing to n entries
# total does not exceed 555000 in this SwissProt version
entry = list()
types = set()
unique = set()

#"""
# Parsear SwissProt
for record in records:
    for feature in record.features:
        if feature.type in ['chain',
                            'signal peptide',
                            'transit peptide',
                            'initiator methionine',
                            #'modified residue',
                            'propeptide',
                            'mutagenesis site',
                            'helix',
                            'sequence conflict',
                            'site',
                            #'cross-link',
                            'unsure residue',
                            #'disulfide bond',
                            'domain',
                            'strand',
                            'turn',
                            'compositionally biased region',
                            'non-terminal residue',
                            'region of interest',
                            'peptide',
                            'transmembrane region',
                            'intramembrane region',
                            'repeat',
                            'topological domain',
                            'non-standard amino acid',
                            'sequence variant',
                            'calcium-binding region',
                            'zinc finger region',
                            'non-consecutive residues',
                            'short sequence motif',
                            #'lipid moiety-binding region',
                            'binding site',
                            'nucleotide phosphate-binding region',
                            'active site',
                            'coiled-coil region',
                            'splice variant',
                            'metal ion-binding site',
                            #'glycosylation site',
                            'DNA-binding region']: pass
        else:
            types.add(feature.type)

            if 'description' in feature.qualifiers.keys():
                desc = feature.qualifiers['description']
            else: desc = 'NULL'

            if 'evidence' in feature.qualifiers.keys():
                evid = feature.qualifiers['evidence']
            else: evid = 'NULL'

            start = str(feature.location.start)
            try:
                start_p = int(start) + 1
                start_r = record.seq[start_p - 1]
            except:start_p, start_r = ['NULL', 'NULL']

            end = str(feature.location.end)
            try:
                end_p = int(end)
                end_r = record.seq[end_p - 1]
            except:end_p, end_r = ['NULL', 'NULL']


            session.add(Ptms(
                record_id=feature.id,
                type=feature.type,
                #feature.extract,
                description=desc,
                evidence=evid,
                start_pos=start_p,
                end_pos=end_p,
                start_res=start_r,
                end_res=end_r,
                protein_id=record.id,
                protein_name=record.name,
                protein_tax=record.annotations['taxonomy'][0]
            ))

    i += 1
    if int(i/500) >= j:
        j += 1
        print(j*500, int(time.time()-start_time))
        session.commit()
    if i >= n:
        break

print('Lesto: ', int(time.time()-start_time))
#"""