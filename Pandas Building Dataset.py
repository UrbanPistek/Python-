import quandl
import pandas as pd
import pickle
import numpy as np
from statistics import mean
from sklearn import datasets, linear_model
from sklearn.model_selection import cross_validate, train_test_split
from sklearn import svm, preprocessing
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

api_key = 'y6C3BDAZHtA994sevNsk'
# dfex = quandl.get('FMAC/HPI_AL', authtoken=api_key)
# print(dfex.head())

def make_state_dataframe():
    fithty_states = pd.read_html('https://state.1keydata.com/state-abbreviations.php')
    '''
    # List
    # print(fithty_states)
    # Data Frame
    # print(fithty_states[0])
    # Column
    # print(fithty_states[2][1])
    
    for abbv in fithty_states[0][0][1:]:
        print("FMAC/HPI_"+str(abbv))'''

    list_qaundl = []
    list_states = []
    for abbv in fithty_states[2][1][1:]:
        # print("FMAC/HPI_"+str(abbv))
        list_qaundl.append("FMAC/HPI_"+str(abbv))
        list_states.append(str(abbv))

    for abbv in fithty_states[2][3][1:]:
        # print("FMAC/HPI_" + str(abbv))
        list_qaundl.append("FMAC/HPI_"+str(abbv))
        list_states.append(str(abbv))
    print(list_qaundl)  # Generate list to get all quandl data
    print(list_states)
    print('****************************************')

    main_df = pd.DataFrame()

    for index in range(len(list_qaundl)):
        query = list_qaundl[index]
        df = quandl.get(query, authtoken=api_key) # Retreive all Data from qaundl
        df.rename(columns={'NSA Value': list_states[index] + ' NSA Value', 'SA Value': list_states[index] + ' SA Value'}, inplace=True)
        # Rename Each column so it can be joined

        if main_df.empty:  # Returns Boolean
            main_df = df  # Mainly done for the first data frame, after that it already has data
        else:
            main_df = main_df.join(df)  # Using join makes sense because all the data has the same index
    # print(main_df.head())

    pickle_out = open('fithty_states.pickle', 'wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    '''Pickling serializes any python object and saves the 
    bit stream so you can load it back in'''

# make_state_dataframe()

pickle_in = open('fithty_states.pickle', 'rb') # Since you already pickled out the data once, now you can call it back in
HPI_data = pickle.load(pickle_in)
# print(HPI_data)

'''
# To Pickle with pandas;
HPI_data.to_pickle('new_pickle.pickle') # Sends out pickle
HPI_data2 = pd.read_pickle('new_pickle.pickle') # Reads back in 

# To Change columns; 
HPI_data['AL'] = HPI_data['AL NSA Value'] *3

# To plot dataframe with mathplotlib; 
HPI_data.plot()
plt.legend().remove()
plt.show()
'''

# Same code as before but instead used to create a dataframe for pct change
def make_state_dataframe_pct_change():
    fithty_states = pd.read_html('https://state.1keydata.com/state-abbreviations.php')

    list_qaundl = []
    list_states = []
    for abbv in fithty_states[2][1][1:]:
        list_qaundl.append("FMAC/HPI_" + str(abbv))
        list_states.append(str(abbv))

    for abbv in fithty_states[2][3][1:]:
        list_qaundl.append("FMAC/HPI_" + str(abbv))
        list_states.append(str(abbv))

    main_df_pct_change = pd.DataFrame()

    for index in range(len(list_qaundl)):
        query = list_qaundl[index]
        df = quandl.get(query, authtoken=api_key)  # Retreive all Data from qaundl
        df.rename(columns={'NSA Value': list_states[index] + ' NSA Value', 'SA Value': list_states[index] + ' SA Value'},inplace=True)
        df[list_states[index]+' NSA Value'] = ((df[list_states[index]+' NSA Value'] - df[list_states[index]+' NSA Value'][0]) / df[list_states[index]+' NSA Value'][0] * 100.0)
        df[list_states[index]+' SA Value'] = ((df[list_states[index]+' SA Value'] - df[list_states[index]+' SA Value'][0]) / df[list_states[index]+' SA Value'][0] * 100.0)
        # Algorithm for making pct change, needed to be executed at each column
        # For simplicity use;  df = df.pct_change()

        if main_df_pct_change.empty:
            main_df_pct_change = df
        else:
            main_df_pct_change = main_df_pct_change.join(df)

    main_df_pct_change.to_pickle('pct_change_data.pickle')

# make_state_dataframe_pct_change()

# Create a benchmark dataframe (US average Housing price index)
def HPI_Benchmark():
    df = quandl.get("FMAC/HPI_USA", authtoken=api_key)
    df["NSA Value"] = ((df["NSA Value"] - df["NSA Value"][0]) / df["NSA Value"][0] * 100.0)
    df["SA Value"] = ((df["SA Value"] - df["SA Value"][0]) / df["SA Value"][0] * 100.0)
    df.rename(columns={'NSA Value': 'Bench NSA'}, inplace=True)
    df.rename(columns={'SA Value': 'Bench SA'}, inplace=True)
    return df

HPI_data_pct_change = pd.read_pickle('pct_change_data.pickle')

'''
*********GENERAL DATA ANALYSIS STUFF***********

# To Plot pct change data with benchmark data; 
fig = plt.figure()
axl = plt.subplot2grid((1,1),(0,0))

benchmark = HPI_Benchmark() 

HPI_data_pct_change.plot(ax = ax1)
benchmark.plot(ax = ax1, color = 'k' , linewidth = 10)

plt.legend().remove()
plt.show()

# Data Analysis Stuff; 
HPI_data_Correlation = HPI_data_pct_change.corr()  # Creates correlation table for all columns
HPI_data_Correlation.describe() # gives information on the dataframe column by column


# Resmapling Data and then Plotting it as monthly against yearly;
fig = plt.figure()
axl = plt.subplot2grid((1,1),(0,0))

# Resampling Data; Changes data from shown at one rate, to being shown at a different rate (monthly to yearly)
TX1yr = HPI_data_pct_change['TX NSA Value'].resample('A').mean()
print(TX1yr)

HPI_data_pct_change['TX NSA Value'].plot(ax=axl, label='Monthly TX HPI')
TX1yr.plot(ax=axl, label='Yearly TX HPI')

plt.legend()
plt.show()

# Dealing with missing data (NaN); 
HPI_data.dropna(inplace=True)  # Deletes any NaN by default
HPI_data.fillna(method='ffill', inplace=True)  # Takes data from before and fills it in, to fill with use use value=9898


# Rolling Data; In a window of time, do some operations 
HPI_data_pct_change['TXMA12'] = HPI_data_pct_change['TX NSA Value'].rolling(12).mean()  # Finds the mean for 12 data points 
fig = plt.figure()
axl = plt.subplot2grid((2,1),(0,0))
axl = plt.subplot2grid((2,1),(1,0), share=axl)

# Plotting the standard deviation and mean; 
HPI_data_pct_change['TXSTD12'] = HPI_data_pct_change['TX NSA Value'].rolling(12).std()
HPI_data_pct_change['TXMA12'] = HPI_data_pct_change['TX NSA Value'].rolling(12).mean()# Finds the mean for 12 data points
fig = plt.figure()
axl = plt.subplot2grid((2,1),(0,0))
ax2 = plt.subplot2grid((2,1),(1,0), sharex=axl)

HPI_data_pct_change[['TX NSA Value', 'TXMA12']].plot(ax=axl)
HPI_data_pct_change['TXSTD12'].plot(ax=ax2)

plt.legend()
plt.show()

# Plotting the two graphs and a correlation between them 
fig = plt.figure()
axl = plt.subplot2grid((2,1),(0,0))
ax2 = plt.subplot2grid((2,1),(1,0), sharex=axl)

TX_AK_12corr = (HPI_data_pct_change['TX NSA Value']).rolling(12).corr(HPI_data_pct_change['AK NSA Value'])
HPI_data_pct_change['TX NSA Value'].plot(ax=axl, label='TX HPI')
HPI_data_pct_change['AK NSA Value'].plot(ax=axl, label='AK HPI')
axl.legend(loc=4)

TX_AK_12corr.plot(ax=ax2, label='TA_AK_12corr')

plt.legend()
plt.show()

# ******************USING NEW DATAFRAMES**********************

bridge_height = {'meters':[10.26, 10.31, 10.27, 10.22, 10.23, 6212.42, 10.28, 10.25, 10.31]}

df = pd.DataFrame(bridge_height)
df['STD'] = df['meters'].rolling(2).std()
print(df)

df_std = df.describe()['meters']['std']
df = df[(df['STD'] < df_std)] # Comparison operator used to redefine the dataframe 
df.plot()
plt.show()
'''
def mortgage_30y():
    df = quandl.get("FMAC/MORTG", trim_start="1975-01-01", authtoken=api_key)
    df["Value"] = ((df["Value"] - df["Value"][0]) / df["Value"][0] * 100.0)
    df = df.resample('D').mean()
    df = df.resample('M').mean()
    df.columns = ['M30']
    return df

def sp500_data():
    df = quandl.get("MULTPL/SP500_REAL_PRICE_MONTH", trim_start="1975-01-01", authtoken=api_key)
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df=df.resample('M').mean()
    df.rename(columns={'Value':'sp500'}, inplace=True)
    df = df['sp500']
    return df

def gdp_data():
    df = quandl.get("FRED/GDPSOPQ027S", trim_start="1975-01-01", authtoken=api_key)
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df=df.resample('M').mean()
    df.rename(columns={'Value':'GDP'}, inplace=True)
    df = df['GDP']
    return df

def us_unemployment():
    df = quandl.get("EIA/STEO_XRUNR_M", trim_start="1975-01-01", authtoken=api_key)
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df=df.resample('1D').mean()
    df=df.resample('M').mean()
    return df

'''

# Added a couple more datasets and joined them into one main dataframe 
m30= mortgage_30y()
sp500 = sp500_data()
US_GDP = gdp_data()
unemployment = us_unemployment()
HPI_bench = HPI_Benchmark()

HPI = HPI_bench.join([m30, unemployment, sp500, US_GDP, HPI_data_pct_change])
HPI.dropna(inplace=True)
print(HPI.corr())

HPI.to_pickle('HPI.pickle')
'''

# *************APPLYING MACHINE LEARNING ALGORITHM**************

def create_labels(cur_hpi, fut_hpi):
    if fut_hpi > cur_hpi:
        return 1
    else:
        return 0

def moving_average(values):
    return mean(values)

housing_data = pd.read_pickle('HPI.pickle')
housing_data = housing_data.pct_change()
housing_data.replace([np.inf, -np.inf], np.nan, inplace=True)
housing_data.dropna(inplace=True)


housing_data['US_HPI_FUTURE'] = housing_data['Bench NSA'].shift(-1)
# print(housing_data[['US_HPI_FUTURE', 'Bench NSA']].head())

housing_data['label'] = list(map(create_labels, housing_data['Bench NSA'], housing_data['US_HPI_FUTURE']))
#  Applying a custom function to an entire dataframe, always applying a calculation to an entire data fraame
print(housing_data.head())

# Example of rolling apply
# housing_data['Example'] = pd.rolling_apply(housing_data['M30'], 10, moving_average)

# Features are X and labels are Y
X = np.array(housing_data.drop(['label', 'US_HPI_FUTURE'], 1))
X = preprocessing.scale(X)
y = np.array(housing_data['label'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
clf = svm.SVC(kernel='linear')
clf.fit(X_train, y_train)
print(clf.score(X_test, y_test))