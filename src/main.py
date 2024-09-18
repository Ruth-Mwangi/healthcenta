import os
import json
from dotenv import load_dotenv
import pandas as pd

from api.client import post_data_to_api
from data_processing.data_cleaning import clean_data
from data_processing.data_transformation import transform_data_to_json
from utils import save_json

def main():
    load_dotenv()
    raw_data_file_path=os.getenv('RAW_DATA')
    processed_data_file_path = os.getenv('PROCESSED_DATA')
    api_url =  os.getenv('MOCKY_API')

    # Load and clean data
    raw_data=pd.read_excel(raw_data_file_path)
    cleaned_data=clean_data(raw_data)
    
    # Transform data and save to file
    transformed_data = transform_data_to_json(cleaned_data)
    save_json(transformed_data,processed_data_file_path)

    # Post data to api
    print("Posting data to API...")
    response = post_data_to_api(processed_data_file_path, api_url)
    
    if response:
        print("Response from API:", response)
    else:
        print("No response or failed request.")
    

if __name__ == "__main__":
    main()