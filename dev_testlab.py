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
in_df = pd.read_csv("./data/registered-business-locations-san-francisco-error.csv", converters = converter )

# convert the business location into json otherwise the normalization later will not work
in_df['Business Location'] = in_df['Business Location'].map(lambda x: my_convert_json(x))

# filter out not needed columns otherwise dataframe will be empty after filter
filtered_df = in_df[['Location Id', 'DBA Name','Street Address','City','Source Zipcode','Business Location']]

# remove the NaNs 
# reset_index() very important! Otherwise merge will merge wrong later
cleaned_nonan_df = filtered_df.dropna().reset_index()

# Normalize the business location
normalized = pd.json_normalize(cleaned_nonan_df['Business Location'], max_level=1)
print(normalized.dtypes)
print(normalized)

# crate a df with long lat (will only contain long lat columns)
longlat_df = pd.DataFrame(normalized['coordinates'].to_list(), columns = ['longitude', 'latitude'])

##print(normalized.dtypes)

# merge again dataframe with long lat
merged_df = pd.merge(cleaned_nonan_df, longlat_df, left_index=True, right_index=True)
#print(merged_df.shape)
#print(merged_df.dtypes)

print(in_df['Business Location'])
print(longlat_df)
print(merged_df)