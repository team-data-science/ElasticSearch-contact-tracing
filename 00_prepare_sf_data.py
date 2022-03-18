from ast import Lambda
from numpy import NaN
import pandas as pd
from pandas import DataFrame
import json

from sqlalchemy import true

# create a converter that makes a json out of the string in 'Business Location' (uses ' instead of ")
converter = {"Business Location": lambda x: x.replace("\'","\"")}

# read the csv using the converter
in_df = pd.read_csv("./data/registered-business-locations-san-francisco.csv", converters = converter )

cleaned_df = in_df.dropna(subset=['Business Location'])
print(cleaned_df.dtypes)
print(cleaned_df.head(1))
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
#print(normalized.dtypes)

# create columns for long and lat
expanded_df = pd.DataFrame(normalized['coordinates'].to_list(), columns = ['longitude', 'latitude'])

#ex_df = in_dataset.merge(expanded_df, how='left')
merged_df = pd.merge(normalized, expanded_df, left_index=True, right_index=True)
#print(merged_df.dtypes)

# only take the columns we need
filtered_df = merged_df[['Location Id', 'DBA Name','Street Address','City','Source Zipcode','latitude', 'longitude']]

# let's see where the data is
print(filtered_df['City'].value_counts())

# filter only for SF locations
sf_data = filtered_df.loc[filtered_df['City'] == 'San Francisco']

# random sample 10k businesses
#sf_data = sf_data.sample(n=10000)

ex_df = sf_data.rename(columns={
    'Location Id': 'business_id', 
    'DBA Name': 'business_name', 
    'Street Address': 'business_address', 
    'City': 'city',
    'Source Zipcode': 'zip',
    })

#print(ex_df.dtypes)
print(ex_df.shape)

ex_df.to_json('./data/sf_businesses.json', lines=True, orient='records')