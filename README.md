# ElasticSearch-contact-tracing

# Requriements
Requires a Machine with at least 8GB of RAM

# Configure WSL2 to use max only 4GB of ram
```
wsl --shutdown
notepad "$env:USERPROFILE/.wslconfig"
```
.wslconfig file:
```
[wsl2]
memory=4GB   # Limits VM memory in WSL 2 up to 4GB
```

## Enter in WSL before Start
sudo sysctl -w vm.max_map_count=262144

## Use parquet loader for elasticsearch
install the loader
pip install elasticsearch-loader[parquet]

Execute the loader from your WSL on Windows
This takes about 3.5 minutes on my machine
```elasticsearch_loader --index my_app_scans --type scans parquet /mnt/c/Users/Andreas/Documents/GitHub/ElasticSearch-contact-tracing/data/businesses.parquet.gzip```

# Install for Streamlit
pip install streamlit-folium

## How to improve this project. To do for you!
- before creating the parquet file change the data types of the dataframe so that they fit
- Change the datatype for the postal code to int when you create it, load the data into Elasticsearch and make sure it's int
- Use a group query instead of scanning 1000 documents and then remove the duplicates in the Streamlit Dataframe
- Create a client that writes new scans to Elasticsearch whenever you create a scan
- create a dashboard on Kibana with stats about locations or people

# Kibana
SELECT * FROM "etl_monitori*" WHERE date = '2022-03-02'

# Logging
1 Execute 03 to create index
2 go in Kibana :5601 and Stack management
2.1 in index management show new index 
2.2 click on it to see the mapping
3 go to index patterns and create new index pattern for etl monitoring
4 go to discover and show that the data is in
5 create a dashboard
6 create a visualization
- use TSVB
7 go back to discover and search for status error - see the error 


- execute 04 to bring in data