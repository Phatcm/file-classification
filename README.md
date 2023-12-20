# File-classification
End user upload files though front-end, lambda function act as back-end and handle file classification and organize it in s3 using presigned URL.

![Screenshot 2023-12-10 072023](https://github.com/Phatcm/file-classification/assets/99520246/c4eb4ec8-85fd-420d-995e-d4cc679c9028)
![Screenshot 2023-12-10 072035](https://github.com/Phatcm/file-classification/assets/99520246/d9f0da60-cbd6-4986-a58c-e2db028a5c1f)


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
