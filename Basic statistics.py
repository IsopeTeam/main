# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 19:26:12 2020

@author: Phippe.ISOPE
"""

import numpy as np
import seaborn as sns
import pandas as pd
import dabest
from matplotlib import pyplot as plt

plt.close('all')

"""
From pandas library
"""

sheet=pd.read_clipboard()                   # If you have selected the headers, if not pd.read_clipboard(header=None)
stat_sheet = sheet.describe()               # basic stats (N,mean, std, percentile, min, max)
corr_sheet = sheet.corr(method='pearson')   # correlation matrix

print ("----------------------------")
print ("Basic statistics\n")
print (stat_sheet)
print ("----------------------------")
print ("\n")
print ("Correlation matrix\n")
print (sheet.corr(method='pearson'))
print ("----------------------------")

fig, (ax1, ax2) = plt.subplots(2, 1)
for col in sheet.columns:
    ax1.plot(sheet[col].values)
ax2 = sheet.boxplot()    

"""
From Seaborn
"""
sns.pairplot(sheet)

"""
From dabest
"""
print ("----------------------------")
two_groups_unpaired = dabest.load(sheet, idx=(sheet.columns[0], sheet.columns[1]), resamples=5000)
two_groups_unpaired.mean_diff.plot()
two_groups_unpaired.hedges_g.plot()
stat=two_groups_unpaired.mean_diff.statistical_tests
print ('Further Statistics from the first 2 columns')
print (stat.transpose())


#two_groups_unpaired.mean_diff
#two_groups_unpaired.mean_diff.results
#two_groups_unpaired.mean_diff.statistical_tests
#two_groups_unpaired.hedges_g.results
