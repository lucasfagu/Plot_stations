#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 20:45:59 2019

@author: lucas

Ler dados cemaden de precipitação

"""

#municipio;codEstacao;uf;nomeEstacao;latitude;longitude;datahora;valorMedida
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import pandas as pd

df = pd.read_csv('/home/lucas/Downloads/SC_2019_7.csv',delimiter=';',index_col=False,header=0)

soma=0
vezes = 0
names=[]

for j in range(0,df.shape[0],1):
    df.valorMedida[j] = float(df.valorMedida[j].replace(',','.'))

for i in range(0,df.shape[0],1):
    try:
        if df.nomeEstacao[i] not in names:
            names.append(df.nomeEstacao[i])
    except:
        pass
    
soma=0

d = {'nome': [], 'acumu': []}
acumulados = pd.DataFrame(data=d)

for i in range(0,len(names),1):
#    teste = names[i]
    for j in range(0,df.shape[0],1):
        if df.nomeEstacao[j] == names[i]:
#            print(df.municipio[j])
            soma = soma + df.valorMedida[j]
#            print(teste,'primeir loop',soma,df.valorMedida[j])
        else:
            pass
        if int(j) == int(df.shape[0])-1:
            print(names[i], 'observou acumulado de ', soma)
            d = {'nome': [names[i]], 'acumu': [soma]}
            dd = pd.DataFrame(data=d)
            acumulados = acumulados.append(dd)
            #make a df with names and acumuldao
            
            soma=0
            
#fazer mapa com pontos de cada estação
lat=[]
lon=[]
for i in range(0,len(names),1):
    for j in range(0,df.shape[0],1):
        if df.nomeEstacao[j] == names[i]:
            if df.latitude[j] not in lat:
                lat.append(df.latitude[j])
                lon.append(df.longitude[j])

for j in range(0,int(len(lat)),1):
    lat[j] = float(lat[j].replace(',','.'))
    lon[j] = float(lon[j].replace(',','.'))    
    
import pynmet as pyn

code = pd.read_csv('/home/lucas/Downloads/pynmet-master/pynmet/data/estacoes.csv')

lat_inmet=[]
lon_inmet=[]
for i in range(0,code.shape[0],1):
    if code.UF[i] == 'SC':
        lat_inmet.append(code.lat[i])
        lon_inmet.append(code.lon[i])

margin = 2 # buffer to add to the range
lat_min = -29.5#min(lat) - margin
lat_max = -25.8#max(lat) + margin
lon_min = -54.5#min(lon) - margin
lon_max = -48#max(lon) + margin

# create map using BASEMAP
m = Basemap(llcrnrlon=lon_min,
            llcrnrlat=lat_min,
            urcrnrlon=lon_max,
            urcrnrlat=lat_max,
            lat_0=(lat_max - lat_min)/2,
            lon_0=(lon_max-lon_min)/2,
            projection='merc',
            resolution = 'h')
m.drawcoastlines()
m.drawcountries()
m.drawstates()
m.drawmapboundary(fill_color='#46bcec')
m.fillcontinents(color = 'white',lake_color='#46bcec')
#m.bluemarble()
#m.drawrivers()
# convert lat and lon to map projection coordinates
for i in range(0,len(lat),1):
    x,y = m(lat[i],lon[i])
    m.plot(x, y, 'bo', markersize=1.5,color='b')
# INMET
for i in range(0,len(lat_inmet),1):
    x,y = m(lon_inmet[i],lat_inmet[i])
    m.plot(x, y, 'bo', markersize=1.5,color='r')    
    
m.drawparallels(np.arange(-31.,-24.,1),labels=[1,0,0,0],linewidth=0.0)
# draw meridians
m.drawmeridians(np.arange(-56.,-47.,1),labels=[0,0,0,1],linewidth=0.0)
plt.savefig('/home/lucas/estacoes_SC.png',dpi=300)
plt.show()

#prec='lat','on','prec_acum'

#    for i in range(0,acumulados.shape[0],1):
#        for j in range(0,df.shape[0],1)
#            if acumulados.nome[i] == df.nomeEstacao[j]:
#                acumulados['lat'] = 
            