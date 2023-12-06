import streamlit as st
import requests
import json

from streamlit_option_menu import option_menu
import upload, download, delete

st.set_page_config(
    page_title = "My S3 Bucket",
)

class MultiApp:
    def __init__(self):
        self.app=[]
    def add_app(self, title, function):
        self.app_append({
            "title": title,
            "function": function
        })
        
    def run():
        with st.sidebar:
            app = option_menu(
                menu_title='Navigator ',
                options=['Upload','Download','Delete'],
                icons=['upload','download','gear'],
                menu_icon='cast',
                default_index=0,
                styles={
                    "container": {"padding": "5!important"},
                    "icon": {"font-size": "15px"}, 
                    "nav-link": {"font-size": "13px", "text-align": "left", "margin":"0px"},}
                )
        
        if app== "Upload":
            upload.app()
        if app== "Download":
            download.app()
        if app== "Delete":
            delete.app()
    run()