import streamlit as st
import requests
import json
import time

def app():
    api_base_file = "https://i52vmx81j2.execute-api.ap-northeast-1.amazonaws.com/prod/files"
    response = requests.get(api_base_file)
    data = response.json()
    
    items = data['Items']
    
    colms = st.columns((1, 2, 2, 1))
    fields = ["№", 'Name', 'Type', "Action"]
    for col, field_name in zip(colms, fields):
        # header
        col.write(field_name)
        
    for i, item in enumerate(items):
        item_name = item["FileName"]
        item_type = item["FileType"]
        col1, col2, col3, col4 = st.columns((1, 2, 2, 1))
        col1.write(i) #index
        col2.write(item_name) #File name
        col3.write(item_type) #File type
        if col4.button("Delete", item_name, type="primary"):
            response = delete_item(item_name, item_type, api_base_file)
            
            if response.status_code == 200:
                st.toast("You delete '"+item_name+"'")
                time.sleep(0.5)
                st.experimental_rerun()
            else:
                st.toast("Delete file failed")

                
def delete_item(item_name, item_type, url):
    metadata = {
                    "name": item_name,
                    "type": item_type
                }
    delete_url = "{}?delete={}".format(url,json.dumps(metadata))
    response = requests.delete(delete_url)
    
    return response
    