import streamlit as st
import requests
import json
import time
import pandas as pd

def app():
    api_base_file = "https://i52vmx81j2.execute-api.ap-northeast-1.amazonaws.com/prod/files"
    response = requests.get(api_base_file)
    data = response.json()
    
    items = data['Items']
    df = pd.DataFrame(items, columns=['FileName'])
    st.write(df)
    
    st.title("Python Talks Search Engine")
    text_search = st.text_input("Search videos by title or speaker", value="")
    # Filter the dataframe using masks
    search_result = df["FileName"].str.contains(text_search)
    
    if text_search:
        st.write(search_result)