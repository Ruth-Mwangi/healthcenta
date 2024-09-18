import unittest
from dotenv import load_dotenv
import pandas as pd
import sys
import os
# Set the correct path for the src directory
sys.path.append(os.path.abspath('src'))

from data_processing.data_cleaning import clean_data
import utils


class TestHealthCentaUtils(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        raw_data_file_path=os.getenv('RAW_DATA')
        processed_data_file_path = os.getenv('PROCESSED_DATA')
        self.clean_data = pd.read_json(processed_data_file_path)
        self.raw_data = pd.read_excel(raw_data_file_path)

    def test_transform_to_json(self):
        cleaned_data=clean_data(self.raw_data)
        data = cleaned_data.iloc[0]
        expected_json = {
            "name": "service a",
            "product_index": "hc-ser-0001",
            "department": {
                "name": "electrocardiography"
            },
            "speciality": {
                "name": "cardiology"
            },
            "category": {
                "name": "fetal medicine"
            },
            "nature_of_procedure": {
                "name": "diagnostic imaging"
            },
            "service_providers": [
                {
                    "id": 1,
                    "price": 100.0
                },
                {
                    "id": 2,
                    "price": 200.0
                },
                {
                    "id": 3,
                    "price": 150.0
                },
                {
                    "id": 4,
                    "price": 300.0
                }
            ]
        }
        result = utils.transform_to_json(data)

        # Assertions for each key in the transformed JSON
        self.assertEqual(result['name'], expected_json['name'])
        self.assertEqual(result['product_index'], expected_json['product_index'])
        self.assertEqual(result['department']['name'], expected_json['department']['name'])
        self.assertEqual(result['speciality']['name'], expected_json['speciality']['name'])
        self.assertEqual(result['category']['name'], expected_json['category']['name'])
        self.assertEqual(result['nature_of_procedure']['name'], expected_json['nature_of_procedure']['name'])

        # Assertions for service_providers
        for i in range(4):  # Adjust range if there are more service providers
            self.assertEqual(result['service_providers'][i]['id'], expected_json['service_providers'][i]['id'])
            self.assertEqual(result['service_providers'][i]['price'], expected_json['service_providers'][i]['price'])

    # Test case for dropping unnecessary columns
    def test_drop_columns(self):
        df = utils.drop_columns(self.raw_data, 'Unnamed: 6')
        self.assertNotIn('Unnamed: 6', df.columns)

    # Test case for dropping rows with missing values
    def test_drop_rows_by_column(self):
        df = utils.drop_rows_by_column(self.raw_data, 'SP. 1')
        self.assertEqual(df.shape[0], 9)  

        df = utils.drop_rows_by_column(self.raw_data, 'SP. 4')
        self.assertEqual(df.shape[0], 9)

if __name__ == '__main__':
    unittest.main()