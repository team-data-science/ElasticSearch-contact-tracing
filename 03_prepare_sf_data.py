from ast import Lambda
from numpy import NaN
import pandas as pd
from pandas import DataFrame
import json

from sqlalchemy import true

def my_convert_json(value):
    try:
        return json.loads(value)
    except:
        return NaN

# create a converter that makes a json out of the string in 'Business Location' (uses ' instead of ")
converter = {"Business Location": lambda x: x.replace("\'","\"")}

# read the csv using the converter
in_df = pd.read_csv("./data/registered-business-locations-san-francisco-original.csv", converters = converter )

# convert the business location into json otherwise the normalization later will not work
in_df['Business Location'] = in_df['Business Location'].map(lambda x: my_convert_json(x))

# filter out not needed columns otherwise dataframe will be empty after filter
filtered_df = in_df[['Location Id', 'DBA Name','Street Address','City','Source Zipcode','Business Location']]

# remove the NaNs
cleaned_nonan_df = filtered_df.dropna().reset_index()

# Normalize the business location
normalized = pd.json_normalize(cleaned_nonan_df['Business Location'], max_level=1)
print(normalized.dtypes)

# crate a df with long lat (will only contain long lat columns) use the to list so that we can access the individual 
longlat_df = pd.DataFrame(normalized['coordinates'].to_list(), columns = ['longitude', 'latitude'])
print(normalized.dtypes)

# merge again dataframe with long lat
merged_df = pd.merge(cleaned_nonan_df, longlat_df, left_index=True, right_index=True)

# only take the columns we need
filtered_df = merged_df[['Location Id', 'DBA Name','Street Address','City','Source Zipcode','latitude', 'longitude']]

# let's see where the data is
print(filtered_df['City'].value_counts())

# filter only for SF locations
sf_data = filtered_df.loc[filtered_df['City'] == 'San Francisco']

# random sample 10k businesses
sf_data = sf_data.sample(n=10000)

ex_df = sf_data.rename(columns={
    'Location Id': 'business_id', 
    'DBA Name': 'business_name', 
    'Street Address': 'business_address', 
    'City': 'city',
    'Source Zipcode': 'zip',
    })

#print(ex_df.dtypes)
print(ex_df)

ex_df.to_json('./data/sf_businesses.json', lines=True, orient='records')