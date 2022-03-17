import pandas as pd

# read the file and use a custom seperator
dataset = pd.read_csv("./data/DCA_LICENSES_1.TXT", sep='|')

print(dataset.dtypes)
# Only take the fields we need
df_select = dataset[['LICENSE_NBR','BUSINESS_NAME','ZIP','BOROUGH','X_COORD','Y_COORD']]

print(df_select.size)
print(df_select.shape)

# remove missing values for (mostly for longitude & latitude)
df_not_null = df_select.dropna()
print(df_not_null.size)

# let's see where the most data is 
print(df_not_null['BOROUGH'].value_counts())

# Filter out only rows where Borough is Manhattan
manhattan_data = df_not_null.loc[df_not_null['BOROUGH'] == 'Manhattan']

# Print to make sure we have enough rows( count will be times 7 because of the 7 columns)#
print(f'Manhattan rows = {manhattan_data.size}')

# sample 10k rows
manhattan_data_10k = manhattan_data.sample(n=10000)
print(f'10k Manhattan sample rows = {manhattan_data_10k.size}')
print(manhattan_data_10k.head(1))

# let's find out our zip code distribution
print(df_not_null['ZIP'].value_counts())


ex_df = manhattan_data_10k

ex_df.to_json('./data/ny_businesses.json')
