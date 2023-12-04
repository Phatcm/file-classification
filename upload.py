import streamlit as st
import requests
import json

def app():
    # User interface
    uploaded_files = st.file_uploader("Choose a file to upload", accept_multiple_files=True)
    overall_progress = st.progress(0)
    progress_text = "Operation in progress. Please wait."

    if st.button("Upload and process"):
        #loop to process uploaded files
        for i, file in enumerate(uploaded_files):
            
            #get s3 pregisned url
            if file is not None:
                api_base_url = "https://o38ehtiqc5.execute-api.ap-northeast-1.amazonaws.com/prod/files"
                api_url = "{}?upload={}".format(api_base_url, file.name)
                print(api_url)
                response = requests.post(api_url)
            
            if response.status_code == 200:
                response_result=json.loads(response.text)  # Access the presigned URL directly from the response body
                #st.write("S3 Presigned URL:", response_result)
            
            #send files through presigned url
            files = {'file': file}
            r = requests.post(response_result['url'], data=response_result['fields'], files=files)
            
            if r.status_code == 204:
                # st.toast("File "+ file.name +" uploaded successfully!", icon ='🚨')
            
                #create metadata info
                metadata = {
                    "name": file.name,
                    "type": file.type
                }
                
                #send metadata to dynamodb
                api_url = "{}?metadata={}".format(api_base_url, json.dumps(metadata))
                print(api_url)
                dynamodb_response = requests.post(api_url)
                
                # if dynamodb_response.status_code == 200:
                #     st.write("File metadata uploaded successfully to Dynamodb")
            else:
                st.write("Error uploading file to S3")

            #progress bar
            if i == len(uploaded_files)-1:
                progress_text = "All files have been uploaded successfully."
            overall_progress.progress((i + 1) / len(uploaded_files), text= progress_text)
            
    else:
        st.write("Please choose a file to upload")