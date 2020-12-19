# QB9.1

QB9.1 PTMs

This repo contains the scripts I made to extract PTMs from a `.xml.gz` SwissProt-Uniprot database file, and put them into a sqlite DB.

Obtain such file from, for example, one of the following sites:

* ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/
* https://www.uniprot.org/downloads

They use SQLalchemy to create and clean the database, stored in SQLite format.

Execute in order, starting by the `declarePTMdb.py` script.

Disclaimer: it may not be pretty, nor well documented :)

## Dependencies

    sqlalchemy
    Bio

## What "is" a PTM?

PTMs are defined at https://www.uniprot.org/help/sequence_annotation as "Amino acid modifications".

We count:

* 'modified residue'
* 'cross-link'
* 'disulfide bond'
* 'lipid moiety-binding region'
* 'glycosylation site'

We skip:

* Non-standard residue
