import streamlit as st
import requests
import json
import os
import streamlit.components.v1 as components


def app():
    api_base_file = "https://i52vmx81j2.execute-api.ap-northeast-1.amazonaws.com/prod/files"
    response = requests.get(api_base_file)
    data = response.json()

    #list items
    items = data['Items']
    
    colms = st.columns((1, 2, 2, 1))
    fields = ["№", 'Name', 'Type', "Action"]
    for col, field_name in zip(colms, fields):
        # header
        col.write(field_name)

    for i, item in enumerate(items):
        item_name = item["FileName"]
        item_type = item["FileType"]
        file_name = item["FileType"]+"/"+item["FileName"]
        col1, col2, col3, col4 = st.columns((1, 2, 2, 1))
        col1.write(i) #index
        col2.write(item_name) #File name
        col3.write(item_type) #File type
        if col4.button("Download", item_name):
            api_base_url = "https://i52vmx81j2.execute-api.ap-northeast-1.amazonaws.com/prod/url"
            response = download_url(api_base_url, file_name)
            if response.status_code == 200:
                response_result = json.loads(response.text)
                presigned_url = response_result
                # trigger = trigger_download(presigned_url, item_name)
                # #Call triger html method to download using presigned url:
                # components.html(html=trigger, height=0, width=0)
                
                download_file(response, item_name)
                st.toast(f"Download file '{item_name}' sucessfully")
            else:
                st.write("Failed to retrieve presigned URL")
    
def download_url(api_base_url, file_name):
    download_url = "{}?download={}".format(api_base_url, file_name)
    response = requests.get(download_url)
    
    return response
    
# def trigger_download(url, item_name):
#     dl_link = f"""
#                     <html>
#                     <head>
#                     <script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
#                     <script>
#                     $('<a href="{url}" download="{item_name}">')[0].click()
#                     </script>
#                     </head>
#                     </html>"""
                    
#     return dl_link

def download_file(url, file_name):
    with open(file_name, 'wb') as f:
        f.write(url.content)
    st.write(f"File '{file_name}' downloaded successfully")