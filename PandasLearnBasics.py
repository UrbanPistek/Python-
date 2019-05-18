import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
style.use('ggplot')

web_stats = {'Day': [1,2,3,4,5,6],
             'Visitors': [43,53,34,45,64,34],
             'Bounce_Rate': [65,72,62,64,54,66]}

# Created a data frame from above stats (df = data frame)
df = pd.DataFrame(web_stats)
print(df)
'''
print(df.head()) # prints first 5
print(df.tail()) # prints last 5
print(df.tail(2)) # prints last 2
'''
# Index is what you want to compare your data too
df.set_index('Day',inplace=True)
'''
print(df[Bounce_Rate]) # Show one column
print(df.Visitors)
print(df[['Bounce_Rate','Visitors']]) # Show two columns
print(np.array(df[['Bounce_Rate','Visitors']])) # Convert to numpy array
'''