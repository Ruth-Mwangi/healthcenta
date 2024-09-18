from utils import transform_to_json


def transform_data_to_json(df):

    # Apply transformation to data
    df = df.apply(transform_to_json, axis=1).tolist()
    return df