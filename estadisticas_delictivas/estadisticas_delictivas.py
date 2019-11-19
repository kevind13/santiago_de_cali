import pandas as pd
import os
import glob
import numpy as np

# data: https://www.policia.gov.co/grupo-informaci%C3%B3n-criminalidad/estadistica-delictiva

crime_type = 'lesiones personales'

source='/Users/finke/Workspaces/colombia/Estadística delictiva Colombia/' + crime_type + '/'

target='./'+crime_type+'/'

for file in glob.glob(source + '*.xlsx'):
    # import file
    df = pd.read_excel(file)
    df.dropna(axis=1, how='all', inplace=True) # drop columns where all elements are NaN
    print(file)
    
    # read where header of original file ends
    dff = df.copy()
    dff.iloc[:,0]=dff.iloc[:,0].str.lower()
    ix = dff.loc[dff.iloc[:,0]=='fecha'].index[0]
    columns=df.iloc[ix].str.strip().str.lower().str.replace(' ','_').str.replace('(','').str.replace(')','').rename(index='')
    df.columns=columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower()
    df = df.iloc[ix+1:].reset_index(drop=True)
    ix = df.loc[df.iloc[:,-1]>10].index[0]
    df = df.iloc[:ix,:-1]

    # place NaN where no data available
    df=df.replace(r'-', np.nan, regex=True)
    df=df.replace(r'^\s*$', np.nan, regex=True)

    # make all columns small caps without tildes
    for column in df.columns:
        if (type(df[column][0]) is str) or (df[column].isna()[0] and (type(df[column].any()) is str)):
            df[column]=df[column].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower()
    
    # select crimes by city
    df=df[df['municipio']=='cali (ct)']
    # export database to csv
    if file.split('.')[-1]=='xlsx':
        df.to_csv(target+file.split('/')[-1][:-5]+'.csv', encoding='utf-8', index=False)
    if file.split('.')[-1]=='xls':
        df.to_csv(target+file.split('/')[-1][:-4]+'.csv', encoding='utf-8', index=False)

    # os.remove(file)

# df1 = pd.read_csv('./hurto personas/hurto-personas-2018_parte_1.csv')
# df2 = pd.read_csv('./hurto personas/hurto-personas-2018_parte_2.csv')
# df1.append(df2).reset_index(drop=True).to_csv('./hurto personas/hurto-personas-2018.csv')