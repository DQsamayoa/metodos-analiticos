import arxivscraper
import pandas as pd
import numpy as np
import feather
import os
    
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


for categoria in cats:
    for anio in range(2000, 2020):
        fecha_inicio = str(anio) + '-01-01'
        fecha_fin = str(anio) + '-12-31'
        try:
            scraper = arxivscraper.Scraper(category = categoria, date_from = fecha_inicio, date_until = fecha_fin, t = 30)
            output = scraper.scrape()
            df = pd.DataFrame(output, columns = cols)
            df['categoria'] = cats[categoria] 
            df['indice'] = df.index
            vals = df.authors.values.tolist()
            rs = [len(r) for r in vals]
            a = np.repeat(df.index, rs)
            df_auth = pd.DataFrame(np.column_stack((a, np.concatenate(vals))), columns = ['indice', 'authors'])
            df_auth['indice'] = df_auth.indice.astype(int)
            df_result = pd.merge(df.drop(['authors'], axis = 1), df_auth, on = ['indice'], how = 'inner')  
                
            folder_path = 'datos/' + categoria.replace(':', '_') + '/'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                    
            feather.write_dataframe(df_result, folder_path + str(anio) + '.feather')
            except:
                continue