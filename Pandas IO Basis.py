import pandas as pd

df = pd.read_csv('CMHC-HPPU50_AB.csv')
print(df.head())
df.set_index('Date', inplace=True)

# Outputs data to a new csv file
df.to_csv('newcsvData.csv')

# Sets the date to be the index cause csv file do not have a index
df = pd.read_csv('newcsvData.csv', index_col=0)

# Converts Data to an Html
df.to_html('htmlExample.html')


