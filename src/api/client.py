import json
import os

import requests

def is_proxy_up(proxy_url):
    """Check if the proxy server is reachable."""
    try:
        response = requests.get('http://www.google.com', proxies={'http': proxy_url, 'https': proxy_url}, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def post_data_to_api(data_file_path: str, api_url: str):
    postman_http_proxy = os.getenv('POSTMAN_HTTP_PROXY')
    postman_https_proxy = os.getenv('POSTMAN_HTTPS_PROXY')
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
  
    proxies = {}
    if postman_http_proxy and postman_https_proxy:
        # Check if the Postman proxy is up
        if is_proxy_up(postman_http_proxy):
            proxies = {
                'http': postman_http_proxy,
                'https': postman_https_proxy
            }
        else:
            print("Postman proxy server is not up. Sending request without proxy.")

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
    
    except requests.RequestException as e :
        print("Error posting data:",e)
        return