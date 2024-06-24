
def fill_missing_parents(df):
    """
    Reads a CSV file into a DataFrame, checks if both "事業本部" and "事業部" columns are empty
    for any row, and fills the "事業本部" column with the keyword "missing_parents" for those rows.

    Parameters:
    filename (str): The path to the CSV file to be processed.

    Returns:
    pd.DataFrame: The updated DataFrame with "missing_parents" filled in where appropriate.
    """

    # Create a boolean mask where both "事業本部" and "事業部" columns are NaN (empty)
    mask = df["headquarter"].isna() & df["division"].isna()

    # Update the "事業本部" column to "missing_parents" where the mask is True
    df.loc[mask, "headquarter"] = "missing_parents"

    # Return the updated DataFrame
    return df

def connect_root_node(df,company_name):
    df['companyName'] = company_name
    return df 
