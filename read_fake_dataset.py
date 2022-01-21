import pandas as pd

# get the just created parquet file
dataset = pd.read_parquet("./data/businesses.parquet.gzip")

# The base dataset .. we need this
#dataset = pd.read_json("./data/yelp_academic_dataset_business.json", lines=True)

print(dataset)
print(dataset.dtypes)

print(dataset.city.value_counts().head(20))