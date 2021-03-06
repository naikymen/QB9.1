from collections import Counter
from Bio import SeqIO
import gzip
import time

start_time = time.time()
print('Start: ', int(start_time))


# Abrir el archivo de SwissProt
gzHandle = gzip.open("data/uniprot_sprot.xml.gz", 'rt')
output_file = 'output/outputCount2.txt'
records = SeqIO.parse(gzHandle,"uniprot-xml")
i, n, j = 0, 1000000, 0  # limit parsing to n entries
# total does not exceed 555000 in this SwissProt version (circa 2017)
# In 2020 the database lists 563,972 entries

#abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#abc_dict = dict()
#for letter in abc:
#    abc_dict[letter] = 0
#print(abc_dict)


c = Counter()
print('Initial: ', c)

# """
# Parsear SwissProt
for record in records:
    sequence = record.seq
    #for letter in abc:
    #    abc_dict[letter] += str(sequence).count(letter)

    c.update(sequence)

    i += 1
    # Print progress every 500 lines
    if int(i/500) >= j:
        j += 1
        print(j*500, int(time.time()-start_time))
        print(c)
    # Break if max iterations are reached
    if i >= n:
        print("Max entries exceeded")
        break

print('Final count: ', c)

# Old run result:
# abc_dict = {'X': 7996, 'G': 14068022, 'B': 285, 'R': 10998296, 'I': 11787308, 'S': 13131755, 'U': 331, 'D': 10851700, 'H': 4518314, 'J': 0, 'V': 13646109, 'P': 9385239, 'K': 11571660, 'O': 29, 'N': 8065800, 'W': 2174806, 'M': 4800523, 'Z': 251, 'C': 2737625, 'T': 10629877, 'Y': 5801954, 'E': 13390010, 'Q': 7811531, 'F': 7676952, 'A': 16412725, 'L': 19180055}

with open(output_file, 'w') as output:
    output.write(''.join([ "key", '\t', 'value', '\n' ]))
    for key in c.keys():
        output.write(''.join([ key, '\t', str(c[key]), '\n' ]))

print(str('Lesto: ', int(time.time()-start_time)))

#"""
