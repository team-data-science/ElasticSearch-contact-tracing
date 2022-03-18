from elasticsearch import Elasticsearch
from numpy import source, take
import pandas as pd
from pandas import DataFrame
import json
import datetime as datetime



es = Elasticsearch("http://localhost:9200")

business = {
  "query": {
    "match": {
      "business_id": "1059819-03-161"
      }
    }
}

business2 = {
  "query":{
    "simple_query_string":{
      "query":"1059819-03-161",
      "fields": ["business_id"],
      "default_operator":"AND"
    }
  }
}

res = es.search(index="my_app_scans", body=business2, size=9999)

df = DataFrame.from_dict(res['hits']['hits'])

print(df.shape)

'''

# Get the existing indices
print(es.indices.get_alias().keys())

# Remove a index
#es.indices.delete(index='test-index', ignore=[400, 404])
#print(es.indices.get_alias().keys())


# Get Index API
#print(client.indices.get(index="*"))

query_body = {
    "query": {
        "match": {
            "deviceID": 5167915669906
            } 
        } 
    }

res = es.search(index="my_app_scans", body=query_body)

#df = DataFrame.from_dict(res['hits']['hits'])

df = pd.json_normalize(res['hits']['hits'])
print(df)
print(df.dtypes)
print(df.iloc[0]['_source.latitude'])

time = datetime.datetime.fromtimestamp(867974400000000/1000000)
print(time)


#################################
# business



my_query = {
        "match": {
            "postal_code": "30340"
            } 
        } 

res = es.search(index="my_app_scans", query=my_query ,size=9999)

df = pd.json_normalize(res['hits']['hits'])

df = df.drop_duplicates(subset=['_source.business_id'])

print(df)



query_body = {
    "query": {
        "match": {
            "business_id": "1059819-03-161"
            } 
        } 
    }

'''

#df = df['_source.user_birth_date'].apply(lambda s: datetime.datetime.fromtimestamp(s).strftime("%m/%d/%Y, %H:%M:%S"))  
#print(df)



'''

res = es.search(index="my_app_scans", body=all_postal_codes , size=9999)

df_zip = pd.json_normalize(res['hits']['hits'])

print(df_zip['_source.postal_code'])
'''