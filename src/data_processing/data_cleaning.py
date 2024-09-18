from utils import categorize_body_parts_in_service_column, drop_columns, drop_rows_by_column


def clean_data(df):
    # Convert data to lower case
    df = df.map(lambda x: x.lower() if isinstance(x, str) else x)

    # Remove unnecessary columns
    df = drop_columns(df, 'Unnamed: 6')

    # Extract body parts to its own column
    df=categorize_body_parts_in_service_column(df)


    # Drop rows with missing values
    df = drop_rows_by_column(df, 'PRODUCT INDEX')
    df = drop_rows_by_column(df, 'SP. 1')
   

    return df