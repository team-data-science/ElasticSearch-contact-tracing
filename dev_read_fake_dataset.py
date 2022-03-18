import pandas as pd
import json

from pydantic import Json

# get the just created parquet file
dataset = pd.read_parquet("./data/businesses.parquet.gzip")

# The base dataset .. we need this
#dataset = pd.read_json("./data/yelp_academic_dataset_business.json", lines=True)

print(dataset)
print(dataset.dtypes)
print(dataset.size)

print(dataset.BUSINESS_NAME.value_counts().head(1))


my_st = dataset.head(1)
my_json = my_st.to_json(orient='records')

print(my_json)