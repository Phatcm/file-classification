# File-classification
End user upload files though front-end, lambda function act as back-end and handle file classification and organize it in s3 using presigned URL.

![Screenshot 2023-12-09 215156](https://github.com/Phatcm/file-classification/assets/99520246/d7bb01aa-7a50-4d00-a571-e816cd53b26b)

## Installation Guide
Required: 
 - Python 3.9, Terraform, VSCode installed
 - AWS CLI install and profile configure
 - Edit aws credential information in terraform.tfvars

To install dependencies:
```
pip install -r requirements.txt
```

Provision infrastructure in AWS with terraform:
```
terraform init
```
```
terraform apply
```

UI creation:
```
streamlit run main.py
```

The website will automatically open in browser, if not access with:
```
http://localhost:8501
```
