from ast import Lambda
from numpy import NaN
import pandas as pd
from pandas import DataFrame
import json

from sqlalchemy import true

# create a converter that makes a json out of the string in 'Business Location' (uses ' instead of ")
converter = {"Business Location": lambda x: x.replace("\'","\"")}

# read the csv using the converter
in_df = pd.read_csv("./data/registered-business-locations-san-francisco-original.csv", converters = converter )

cleaned_df = in_df.dropna(subset=['Business Location'])

# Load the json from business location, if error then fill it with NaN so we can clean it again
def my_convert_json(value):
    try:
        return json.loads(value)
    except:
        return NaN


# perform lambda that parses the string for Business Location for each row into a json
cleaned_df = cleaned_df['Business Location'].apply(lambda x: my_convert_json(x))

# remove the NaN rows
cleaned_nonan_df = cleaned_df.dropna()

# normalize the DataFrame to create new columns
normalized = pd.json_normalize(cleaned_nonan_df)

# create columns for long and lat
expanded_df = pd.DataFrame(normalized['coordinates'].to_list(), columns = ['latitude', 'longitude'])

#ex_df = in_dataset.merge(expanded_df, how='left')
merged_df = pd.merge(in_df, expanded_df, left_index=True, right_index=True)
print(merged_df.dtypes)

# only take the columns we need
filtered_df = merged_df[['Location Id', 'DBA Name','Street Address','City','Source Zipcode','latitude', 'longitude']]

# let's see where the data is
print(filtered_df['City'].value_counts())

# filter only for SF locations
sf_data = filtered_df.loc[filtered_df['City'] == 'San Francisco']

# random sample 10k businesses
ex_df = sf_data.sample(n=10000)

#print(ex_df.dtypes)
print(ex_df.shape)

ex_df.to_json('./data/sf_businesses.json', lines=True, orient='records')

#print(dataset['Business Location'][1])

#print(dataset2.head(1).to_json())

#my_str = dataset[0]['Business Location'][0]
#print(my_str)

#myjson = json.loads(my_str)
#print(myjson)

#print(myjson['coordinates'][0])

#new_df = dataset['Business Location'].apply(lambda x: pd.Series({'X': json.loads(x[0])['coordinates'][0]}))
#print(new_df)

#new_df = pd.json_normalize(dataset)

'''
print(dataset.dtypes)
# Only take the fields we need
df_select = dataset[['LICENSE_NBR','BUSINESS_NAME','STREET','ZIP','BOROUGH','X_COORD','Y_COORD']]

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

'''