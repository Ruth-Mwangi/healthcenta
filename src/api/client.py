import json
import os

import requests


def post_data_to_api(data_file_path: str, api_url: str):
    postman_http_proxy = os.getenv('POSTMAN_HTTP_PROXY')
    postman_https_proxy = os.getenv('POSTMAN_HTTPS_PROXY')
    postman_cert_path = os.getenv('POSTMAN_CERT')
    try:
        with open(data_file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File not found: {data_file_path}")
        return
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {data_file_path}")
        return

    headers = {
    'Content-Type': 'application/json'
    }
    proxies = {
    'http': postman_http_proxy,
    'https': postman_https_proxy
}

    try:
        response = requests.post(api_url, json=data,headers=headers,proxies=proxies,verify=False)
        response.raise_for_status()  
        body_bytes = response.request.body
        response_str = body_bytes.decode('utf-8') 
        body_data = json.loads(response_str)
        response_data= {
            'status':response.status_code,
            'headers':response.request.headers,
            'body':body_data
        }

        return response_data
    
    except Exception as e :
        print("Error posting data:{e}")
        return