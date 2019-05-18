import time
from urllib.request import urlopen
import datetime
from collections import Counter, defaultdict
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import bibtexparser
import arxivscraper
import feather
import datetime
import os
import fnmatch

cats = {
        'physics:hep-ph' : 'High Energy Physics - Phenomenology',
        'physics:hep-th' : 'High Energy Physics - Theory',
        'cs' : 'Computer Science',
        'econ' : 'Economics',
        'eess' : 'Electrical Engineering and Systems Science',
        'physics' : 'Physics',
        'physics:astro-ph' : 'Astrophysics',
        'physics:cond-mat' : 'Condensed Matter',
        'physics:gr-qc' : 'General Relativity and Quantum Cosmology',
        'physics:hep-ex' : 'High Energy Physics - Experiment',
        'physics:hep-lat' : 'High Energy Physics - Lattice',
        'physics:math-ph' : 'Mathematical Physics',
        'physics:nlin' : 'Nonlinear Sciences',
        'physics:nucl-ex' : 'Nuclear Experiment',
        'physics:nucl-th' : 'Nuclear Theory',
        'physics:physics' : 'Physics (Other)',
        'physics:quant-ph' : 'Quantum Physics',
        'math' : 'Mathematics',
        'stat' : 'Statistics',
        'q-bio' : 'Quantitative Biology',
        'q-fin' : 'Quantitative Finance',
        }

cols = ('id', 'title', 'categories', 'abstract', 'doi', 'created', 'updated', 'authors')

def get_cites(arxiv_id):
    cites = []
    base_url = "http://inspirehep.net/search?p=refersto:%s&of=hx&rg=250&jrec=%i"
    offset = 1
    
    while True:          
        # print(base_url%(arxiv_id, offset))
        response = urlopen(base_url%(arxiv_id, offset))
        xml = response.read()
        soup = BeautifulSoup(xml)

        refs = "\n".join(cite.get_text() for cite in soup.findAll("pre"))
        if len(refs) == 0:
            break
            
        bib_database = bibtexparser.loads(refs)
        if bib_database.entries:
            cites += bib_database.entries
            offset += 250
            
        else:
            break

    return cites

for categoria in cats:
    folder_path = 'datos/' + categoria.replace(':', '_') + '/'
    archivos = os.listdir(folder_path)
    anios = []
    
    try:
        for archivo in archivos:
            if fnmatch.fnmatch(archivo, '*.feather'):
                anios += [archivo.split(".")[0]]
    
    except:
        print("No se encontraron archivos para la categoria " + categoria)
        continue

    for anio in anios:
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(timestamp + '|' + ' Comenzando ' + categoria + ': archivo ' + anio + '.feather' + ' ...')
            df = feather.read_dataframe(folder_path + anio + '.feather')[['id']] \
                        .drop_duplicates()

            step = 1000
            pasos = df.shape[0]//1000
            print('Se tienen ' + str(df.shape[0]) + ' registros y se extraeran en ' + str(pasos + 1) + ' iteraciones.')
            for N in range(0, pasos + 1):
                lower_limit = N*step
                upper_limit = min((N+1)*step, df.shape[0])      
                cites = df['id'][lower_limit:upper_limit].map(get_cites)
                df.loc[lower_limit:upper_limit, 'cited_by'] = cites
                time.sleep(3)


            store = pd.HDFStore(folder_path + anio + '_citedBy.h5')
            store['refs'] = df
            # df = store['df']
            store.close()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(timestamp + '|' + ' Finalizando ' + categoria + ': archivo' + anio + '.feather' + ' .')
        except:
            continue