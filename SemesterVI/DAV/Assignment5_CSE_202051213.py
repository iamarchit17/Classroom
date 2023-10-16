#202051213
#Archit Agrawal

from google.colab import drive
drive.mount('/content/drive')

!pip install joypy
!pip install squarify
!pip install plotly

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import transforms
from statsmodels.graphics.mosaicplot import mosaic
from joypy import joyplot 
import squarify
import plotly.express as px
from itertools import product

filename = '/content/drive/MyDrive/data/Lab4/Milk_Production_2007_2012.csv'
milk_df = pd.read_csv(filename)

filename = '/content/drive/MyDrive/data/Lab4/Egg_Production_2007_2012.csv'
egg_df = pd.read_csv(filename)

milk_df['Type'] = 'Milk'
egg_df.rename(columns = {'2007-08 (In lakh nos.)' : '2007-08', 
                           '2008-09 (In lakh nos.)' : '2008-09', 
                           '2009-10 (In lakh nos.)' : '2009-10', 
                           '2010-11 (In lakh nos.)' : '2010-11', 
                           '2011-12 (In lakh nos.)' : '2011-12'}, inplace=True)
egg_df['Type'] = 'Egg'
egg_df = egg_df.replace('Total', 'All India')

df = pd.concat([milk_df, egg_df])
df = pd.melt(df, id_vars=['States/Uts', 'Type'], value_vars=['2007-08',	'2008-09',	'2009-10',	'2010-11', '2011-12'], var_name='Year')
df = df.set_index(['Year', 'Type'])
df = df.groupby(['Year', 'Type', 'States/Uts'])['value'].sum().unstack('States/Uts')
df.head()

df_all_india = df['All India']
df_all_india = df_all_india.iloc[0:].unstack()
print(df_all_india)
df_all_india_arr = df_all_india.values.T
df_all_india_arr

"""# Nested Pie Chart"""

fig, ax = plt.subplots()
size = 0.4
cmap = plt.get_cmap('tab20c')
outer_colors = cmap([1,8])
inner_colors = cmap([3,7,11,13,17])

outerlabels = df_all_india.columns.tolist()
innerlabels = df_all_india.index.tolist()

print(df_all_india_arr.flatten())
print(df_all_india_arr.sum(axis=1))

l2 = ax.pie(df_all_india_arr.flatten(), radius = 1 - size, colors = inner_colors, wedgeprops = dict(width = size, edgecolor = 'w'))

l1 = ax.pie(df_all_india_arr.sum(axis = 1), radius = 1, colors = outer_colors, labels = outerlabels, wedgeprops = dict(width = size, edgecolor = 'w'))


ax.legend(innerlabels, loc=(1,0.5))
ax.set(aspect = 'equal', title = 'Nested Pie Chart for Egg and Milk Production across Different Years')
plt.show()

"""# Mosaic Plot"""

df_all_india = df['All India']
print(df_all_india)
dic = df_all_india.to_dict()
labelizer = lambda k:dic[k]
mosaic(df_all_india, labelizer = labelizer, gap = 0.01)
plt.show()

"""# Tree Map"""

df_all_india = df_all_india.reset_index()

fig = px.treemap(df_all_india, path = ['Year', 'Type'], values = 'All India')
fig.show()

fig = px.treemap(df_all_india, path = ['Type', 'Year'], values = 'All India')
fig.show()