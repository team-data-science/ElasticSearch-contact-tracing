import streamlit as st
from pandas import DataFrame
import pandas as pd
from elasticsearch import Elasticsearch
from pandas.io.json import json_normalize
from streamlit_folium import folium_static
import folium
import datetime as datetime

# connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# make sure that the whole page is used
st.set_page_config(layout="wide")

# Add title to sidebar
st.sidebar.title('San Francisco App Scan Tracker')

################ Search by free text

text = st.sidebar.text_input("Free Text Search")

# add the link to the Atlanta map below the code

# search for postal code
if text:

    #build the search query that searches everything
    query_body = {
        "query": {
            "simple_query_string" : {
                "query": text
            }
        }
    }

    # search the index. 1k is enough to find all the businesses. 
    # The problem is that it wants to return all documents for this query for you
    # There is no group by query for strings (we just uploaded it as string)
    res = es.search(index="my_app_scans", body=query_body , size=1000)

    # get the results and put them into a dataframe
    df = pd.json_normalize(res['hits']['hits'])

    # drop the duplicates
    df = df.drop_duplicates(subset=['_source.business_id'])

    # rename the lang lot columns so they have the right name for the map function
    df = df.rename(columns={"_source.latitude": "latitude", "_source.longitude": "longitude"})
    
    df = df.filter(items = ['_source.business_id','_source.business_name','_source.business_address','latitude','longitude','_source.zip'], axis = 1)
    
    # Add the table with a headline
    st.header(f"Businesses for search: {text}")
    # show the data as table
    
    table_df = df.filter(items = ['_source.business_id','_source.business_name','_source.business_address','_source.zip'], axis = 1)
    
    # fix names before printing the table
    table_df = table_df.rename(columns={"_source.business_id": "Business ID", "_source.business_name": "Name", "_source.business_address": "Address", "_source.zip": "Postal Code"})
    
    # print the table
    table1 = st.dataframe(data=table_df)
    
    # this will print the boring standard app from streamlit
    #st.map(data=df, zoom=None, use_container_width=True)

    # print a folium map. Really cool
    map = folium.Map(location=[df.iloc[0]['latitude'], df.iloc[0]['longitude']], zoom_start=13)
    
    # add the markers
    for index, row in df.iterrows():
        folium.Marker(
            [row['latitude'], row['longitude']], popup=f"{row['_source.business_name']} <br> ID= {row['_source.business_id']}").add_to(map)

    folium_static(map)


################ Search by postal code

# add the input field for postal code
postal_code = st.sidebar.text_input("Zip Code")

# add the link to the Atlanta map below the code
link = "[All San Francisco Zip codes](https://www.usmapguide.com/california/san-francisco-zip-code-map/)"
st.sidebar.markdown(link, unsafe_allow_html=False) 

# add a separator 
myseparator = "---"
st.sidebar.markdown(myseparator, unsafe_allow_html=False) 

# search for postal code
if postal_code:

     #build the search query
    query_body = {
    "query": {
        "match": {
            "zip": postal_code
            } 
        } 
    }

    # search the index. 1k is enough to find all the businesses. The problem is that it wants to return all documents for this query for you
    # There is no group by query for strings (we just uploaded it as string)
    res = es.search(index="my_app_scans", body=query_body , size=1000)

    # get the results and put them into a dataframe
    df = pd.json_normalize(res['hits']['hits'])

    # drop the duplicates
    df = df.drop_duplicates(subset=['_source.business_id'])

    # rename the lang lot columns so they have the right name for the map function
    df = df.rename(columns={"_source.latitude": "latitude", "_source.longitude": "longitude"})
    
    df = df.filter(items = ['_source.business_id','_source.business_name','_source.business_address','latitude','longitude','_source.zip'], axis = 1)
    
    # Add the table with a headline
    st.header("Businesses in Postal code")
    # show the data as table
    
    table_df = df.filter(items = ['_source.business_id','_source.business_name','_source.business_address','_source.zip'], axis = 1)
    
    # fix names before printing the table
    table_df = table_df.rename(columns={"_source.business_id": "Business ID", "_source.business_name": "Name", "_source.business_address": "Address", "_source.zip": "Postal Code"})
    
    # print the table
    table2 = st.dataframe(data=table_df)
    
    # this will print the boring standard app from streamlit
    #st.map(data=df, zoom=None, use_container_width=True)

    # print a folium map. Really cool
    m = folium.Map(location=[df.iloc[0]['latitude'], df.iloc[0]['longitude']], zoom_start=13)
    
    # add the markers
    for index, row in df.iterrows():
        folium.Marker(
            [row['latitude'], row['longitude']], popup=f"{row['_source.business_name']} <br> ID= {row['_source.business_id']}").add_to(m)

    folium_static(m)


################ Search by Business ID

# create the input field on the sidebar    
business_id = st.sidebar.text_input("Business ID")

if business_id:
    #build the search query for Elasticsearch
    query_body = {
        "query":{
            "simple_query_string":{
                "query":business_id,
                "fields": ["business_id"],
                "default_operator":"AND"
            }
        }
    }

    # search the index
    res = es.search(index="my_app_scans", body=query_body ,size=10000)
    
    # get the results and put them into a dataframe
    df = pd.json_normalize(res['hits']['hits'])
    
    table_df = df.filter(items = ['_source.scan_timestamp','_source.deviceID','_source.user_name','_source.user_birth_date'], axis = 1)
    
    # turn the epochs into timestamps
    table_df['_source.user_birth_date'] = table_df['_source.user_birth_date'].apply(lambda s: datetime.datetime.fromtimestamp(s/1000000).strftime("%Y/%m/%d"))
    table_df['_source.scan_timestamp'] = table_df['_source.scan_timestamp'].apply(lambda s: datetime.datetime.fromtimestamp(s/1000000).strftime("%Y/%m/%d %H:%M:%S"))

    # sort values by timestamp
    table_df = table_df.sort_values(by=['_source.scan_timestamp'])
    
    # fix names before printing the table
    table_df = table_df.rename(columns={"_source.scan_timestamp": "Scan Timestamp","_source.deviceID": "Device ID", "_source.user_name": "User Name", "_source.user_birth_date": "Birth Date"})

    # add a header before the table
    st.header(f"Users scanned at this business: {business_id}")
    
    # print the table
    table3 = st.dataframe(data=table_df)

################ Search by Device ID

# Below the fist chart add a input field for the invoice number
device_id = st.sidebar.text_input("Device ID")
#st.text(inv_no)  # Use this to print out the content of the input field

# if enter has been used on the input field 
if device_id:
    #build the search query for Elasticsearch
    query_body = {
    "query": {
        "match": {
            "deviceID": device_id
            } 
        } 
    }

    # search the index
    res = es.search(index="my_app_scans", body=query_body ,size=1000)
    
    # get the results and put them into a dataframe
    df = pd.json_normalize(res['hits']['hits'])

    # rename the lang lot columns so they have the right name for the map function
    df = df.rename(columns={"_source.latitude": "latitude", "_source.longitude": "longitude"})
    

    #df = df.sort_values(by='_source.scan_timestamp')
    
    # Add the table with a headline
    st.header(f"User scans for user: {device_id}")
    
    # Turn the epoch into timestamp
    df['_source.scan_timestamp'] = df['_source.scan_timestamp'].apply(lambda s: datetime.datetime.fromtimestamp(s/1000000).strftime("%Y/%m/%d %H:%M:%S"))  
    
    # filter only the needed colums for the table
    table_df = df.filter(items = ['_source.scan_timestamp','_source.business_id','_source.business_name','_source.business_address','longitude','latitude'], axis = 1)  #,'latitude','longitude'
    
    # sort the visited places by timestamp
    table_df = table_df.sort_values('_source.scan_timestamp', axis = 0)

    # fix names before printing the table
    table_df = table_df.rename(columns={"_source.scan_timestamp": "Scan Timestamp","_source.business_id": "Business ID", "_source.business_name": "Business Name", "_source.business_address": "Business Address"})

    # print the table
    table4 = st.dataframe(data=table_df) 

    # add the folium maps
    m = folium.Map(location=[df.iloc[0]['latitude'], df.iloc[0]['longitude']], zoom_start=10)
    
    for index, row in df.iterrows():
        folium.Marker(
            [row['latitude'], row['longitude']], popup=row['_source.scan_timestamp'], tooltip=row['_source.business_name']
        ).add_to(m)

    # print the map
    folium_static(m)

    




    
