# -*- coding: utf-8 -*-
"""
Original file is located at
    https://colab.research.google.com/drive/17cPIiH3-ya7jfEOZ6ZKjIeX66oNec1HA
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.gofplots import qqplot

#Patient Attendance Data
path = '/content/drive/MyDrive/data/Lab2/JK-Allopathic-Outpatient_attendance-May-2019.csv'
patients_data = pd.read_csv(path)
patients_data.head()

patients_data.columns

"""# Tasks on Patient Attendance Data

1. Compute total patient attendance for all district for all four range group and plot the bar diagram. Set the bar plot parameters for better visualization.
2. Compute total patient attendance for all district for each Facility Type (DH, CHC and SC) for all four range groups and plot the staked bar diagram of three. Set the bar plot parameters for better visualization.
3. Plot group bar plot for Performance - Overall Average of different Facility Type (DH, CHC and SC) of Anantnag, Jammu, Poonch, Reasi and Udhampur.
4. Present dot plot for Performance - Maximum of any 20 different district. Performance - Maximum for different Facility Type should be combined appropriately using a aggregation function for each district.

Task 1
"""

cols = ['No. of facilities by performance - 1 to 100',
       'No. of facilities by performance - 101 to 500',
       'No. of facilities by performance - 501 to 1000',
       'No. of facilities by performance - >1000']

district = patients_data.groupby('District').sum()[cols]
district.reset_index(inplace=True)

new_district_data = district.melt('District', var_name='Facilities', value_name='Number of Facilities')

fig = plt.figure(figsize=(13,6),dpi=200)
plt.xticks(rotation=45)
sns.barplot(data=new_district_data, x='District', y='Number of Facilities', hue='Facilities')

"""Task 2"""

district_fac = patients_data.groupby(['District','Facility Type']).sum()[cols]
district_fac.plot(kind='bar',stacked=True, figsize=[34,10])

"""Task 3"""

dist = ['Anantnag','Jammu','Poonch','Reasi','Udhampur']
patients_dist = patients_data[patients_data['District'].isin(dist)]
sns.barplot(data=patients_dist, y="Performance - Overall Average **", x='District', hue='Facility Type')

"""Task 4"""

district_unique_20 = patients_data['District'].unique()[:20]

district_max_pf = patients_data[patients_data['District'].isin(district_unique_20)]
district_max_pf = district_max_pf.groupby('District').agg(Performance_Maximum_Agg = ('Performance - Maximum', 'sum'))

fig = plt.figure(figsize=(10,5),dpi=100)
plt.xticks(rotation=45)
sns.scatterplot(data=district_max_pf, y='Performance_Maximum_Agg', x='District')

"""# Tasks on FIFA Football Players Data
1. Present Age of various football players as histogram and kernel density plots. Set appropriate parameters of the plot.
2. Present Age of various Football players as Kernel Density plots for each of FC Barcelona, Chelsea, Juventus and Real Madrid Clubs. Set appropriate parameters of the plot.
3. Plot Value of players as Stacked Histogram Preferred Foot wise (right and left).
4. Check distribution of International Reputation using Q-Q plot.
"""

#Football Player Data
path = '/content/drive/MyDrive/data/Lab2/Fifa_player_football_data.csv'
football_data = pd.read_csv(path)
football_data.head()

"""Task 1"""

age_hist = sns.histplot(data=football_data, x='Age', binwidth=1).set_title('Histogram: Age of Different Football Players')

age_kde = sns.kdeplot(data=football_data, x='Age', color='b').set_title('Kernel Density Plot: Age of Different Football Players')

"""Task 2"""

clubs = ['FC Barcelona', 'Chelsea', 'Juventus', 'Real Madrid']
temp_df = football_data[football_data['Club'].isin(clubs)]

age_kde_club = sns.kdeplot(data=temp_df, x='Age',hue='Club', color='b').set_title('Kernel Density Plot: Age of Different Players in Particular Club')

"""Task 3"""

fig = plt.figure(figsize=(42,8),dpi=200)
plt.xticks(rotation=90)
hist_pref_foot = sns.histplot(data=football_data,x='Value',hue='Preferred Foot').set_title('Value of Players Preferred Foot-Wise')

"""Task 4"""

qqplot(football_data["International Reputation"],line='45')
plt.show()