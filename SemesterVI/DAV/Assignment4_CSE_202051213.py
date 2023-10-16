#Archit Agrawal
#202051213
"""
Original file is located at
    https://colab.research.google.com/drive/1g8kgliILM3N6SyuWEwycFEF87gGdKu4S
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install joypy

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import transforms
from statsmodels.graphics.gofplots import qqplot
from joypy import joyplot

filename = '/content/drive/MyDrive/data/Lab4/Milk_Production_2007_2012.csv'
milk_df = pd.read_csv(filename)

filename = '/content/drive/MyDrive/data/Lab4/Egg_Production_2007_2012.csv'
egg_df = pd.read_csv(filename)

milk_df['Type'] = 'Milk'
milk_df.head()

egg_df.rename(columns = {'2007-08 (In lakh nos.)' : '2007-08', 
                           '2008-09 (In lakh nos.)' : '2008-09', 
                           '2009-10 (In lakh nos.)' : '2009-10', 
                           '2010-11 (In lakh nos.)' : '2010-11', 
                           '2011-12 (In lakh nos.)' : '2011-12'}, inplace=True)
egg_df['Type'] = 'Egg'
egg_df.head()

"""# Task 1: Merge two data frames such that the new data frame has multi-level columns (like years under milk and eggs). Try to change the column names if required."""

df = pd.concat([milk_df, egg_df])
df = pd.melt(df, id_vars=['States/Uts', 'Type'], value_vars=['2007-08',	'2008-09',	'2009-10',	'2010-11', '2011-12'], var_name='Year')
df = df.set_index(['Type', 'Year'])
df.head(10)

"""# Task 2: Present the production of milk in Gujarat, Kerala, Andhra Pradesh, Uttar Pradesh and Punjab on 2007-2008 as a Pie chart. The pie chart should consist of proportion in percentage and labels for each piece."""

cols = ['Gujarat', 'Kerala', 'Andhra Pradesh', 'Uttar Pradesh', 'Punjab']
df2 = milk_df[milk_df['States/Uts'].isin(cols)]
color = sns.color_palette('pastel')[0:5]
plt.pie(df2['2007-08'], labels = df2['States/Uts'], colors = color, autopct='%.0f%%')
plt.title("Pie Chart for Milk Production of States for the year 2007-08")
plt.show()

"""# Task 3: Plot five pie charts of egg production in Gujarat, Kerala, Andhra Pradesh, Uttar Pradesh and Punjab for the five years range. Each pie chart should represent the proportional egg production in Gujarat, Kerala, Andhra Pradesh, Uttar Pradesh and Punjab for a given year."""

df3 = egg_df[egg_df['States/Uts'].isin(cols)]

fig, axes = plt.subplots(5,1,figsize=(12,15))
axes[0].pie(df3['2007-08'], labels = df3['States/Uts'], colors = color, autopct='%.0f%%')
axes[0].set_title('2007-08')
axes[1].pie(df3['2008-09'], labels = df3['States/Uts'], colors = color, autopct='%.0f%%')
axes[1].set_title('2008-09')
axes[2].pie(df3['2009-10'], labels = df3['States/Uts'], colors = color, autopct='%.0f%%')
axes[2].set_title('2009-10')
axes[3].pie(df3['2010-11'], labels = df3['States/Uts'], colors = color, autopct='%.0f%%')
axes[3].set_title('2010-11')
axes[4].pie(df3['2011-12'], labels = df3['States/Uts'], colors = color, autopct='%.0f%%')
axes[4].set_title('2011-12')
plt.show()

"""# Task 4: Plot Stacked Area Chart that represents the proportional egg production state wise over five years. There would be five stacked colors for Gujarat, Kerala, Andhra Pradesh, Uttar Pradesh and Punjab."""

egg_df = egg_df.drop('Type', axis = 1)
egg_df = egg_df.set_index('States/Uts')

fig = plt.figure(figsize=(10,8))
labels=['Gujarat', 'Kerala', 'Andhra Pradesh', 'Uttar Pradesh', 'Punjab']
x_axis=['2007-08', '2008-09', '2009-10', '2010-11', '2011-12']
plt.stackplot(x_axis,egg_df.loc['Gujarat'],egg_df.loc['Kerala'],egg_df.loc['Andhra Pradesh'],egg_df.loc['Uttar Pradesh'],egg_df.loc['Punjab'],labels=labels)
plt.legend(loc='upper right')
plt.xlabel('Year')
plt.ylabel('Values')
plt.show()