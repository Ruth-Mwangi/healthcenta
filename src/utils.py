import json
import os
import models

def impute_missing_values_with_mean(column):
    """
    Impute missing values in a pandas Series with the mean of non-missing values.

    Parameters:
    - column (pandas.Series): The Series with missing values to be imputed.

    Returns:
    - pandas.Series: The Series with missing values replaced by the mean of the non-missing values.
    """
    mean_value = column.mean()
    
    return column.fillna(mean_value)

def categorize_body_parts_in_service_column(df):
    """
    Categorizes services based on body parts. 

    This function creates a new column `BODY_PART` in the DataFrame to indicate the body part 
    relevant to each service. It assigns the body part from the `SERVICE` column and uses 
    forward filling to propagate the body part to subsequent rows until a new body part is encountered.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data with a 'SERVICE' column.

    Returns:
    pd.DataFrame: The DataFrame with a new 'BODY_PART' column.
    """
    body_parts_str = os.getenv('BODY_PARTS')
    body_parts = body_parts_str.lower().split(',') if body_parts_str else []

    df['BODY_PART'] = df['SERVICE'].apply(lambda x: x if x in body_parts else None)

    df['BODY_PART'] = df['BODY_PART'].ffill()

    return df

def drop_columns(df, columns):
    """
    Drops one or more columns from the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame from which columns will be dropped.
    columns (str or list of str): A single column name or a list of column names to drop.

    Returns:
    pd.DataFrame: A new DataFrame with the specified columns removed.
    """
    if isinstance(columns, str):
        columns = [columns]
    
    if not isinstance(columns, list):
        raise TypeError("Parameter 'columns' must be a string or a list of column names")

    missing_columns = [col for col in columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Columns not found in DataFrame: {', '.join(missing_columns)}")

    return df.drop(columns=columns)

def drop_rows_by_column(df, column_name):
    """
    Drops rows from the DataFrame where the specified column is NaN (empty).

    Parameters:
    df (pd.DataFrame): The DataFrame from which rows will be removed.
    column_name (str): The name of the column to check for NaN values.

    Returns:
    pd.DataFrame: A new DataFrame with the rows where the specified column is NaN removed.
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")
    
    return df.dropna(subset=[column_name])


def transform_to_json(row):
    """
    Transforms a DataFrame row into a JSON object with nested structures for service details
    and a list of service providers.

    Args:
        row (pandas.Series): A row from a DataFrame containing service information.

    Returns:
        dict: A JSON object containing the service details and service providers.
    """
    providers_str = os.getenv('SERVICE_PROVIDERS')

    providers_columns = providers_str.split(',') if providers_str else []
    providers_list = []
    
    for provider in providers_columns:
        provider_id = int(provider.split(".")[1])
        provider_price = row.get(provider)
        
        if provider_price is not None: 
            provider_data = models.ServiceProvider(id=provider_id, price=provider_price)
            providers_list.append(provider_data)
    
    department = models.Department(name=row.get('DEPARTMENT', ''))
    speciality = models.Specialty(name=row.get('SPECIALTY', ''))
    category = models.Category(name=row.get('CATEGORY', ''))
    nature_of_procedure = models.NatureOfProcedure(name=row.get('NATURE OF ENT. PROCEDURE', ''))

    service_data = models.ServiceData(
        name=row.get('SERVICE', ''),
        product_index=row.get('PRODUCT INDEX', ''),
        department=department,
        speciality=speciality,
        category=category,
        nature_of_procedure=nature_of_procedure,
        service_providers=providers_list
    )
   
    return service_data.model_dump()


def save_json(data, file_path):
    """
    Saves JSON file.
    Args:
    data (JSON): The JSON to save.
    file_path (str): The file path where the JSON file will be saved.
    """

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Data successfully saved to {file_path}")
    
   
