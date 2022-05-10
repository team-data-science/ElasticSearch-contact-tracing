# ElasticSearch-contact-tracing

#SF Open Dataset:
Download from Kaggle: https://www.kaggle.com/datasets/san-francisco/sf-registered-business-locations-san-francisco

Original source & license infos: https://data.sfgov.org/Economy-and-Community/Registered-Business-Locations-San-Francisco/g8m3-pdis

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
