import pandas as pd

def build_time_series(dataFrame):
    """
    Build a time-series DataFrame by setting the index to 'Observation Date'.

    Parameters
    ----------
    dataFrame : pandas.DataFrame
        Input DataFrame containing columns including 'Observation Date' and 'Observation Value'.

    Returns
    -------
    pandas.DataFrame
        Time-series DataFrame with the index set to 'Observation Date'.

    Notes
    -----
    This function modifies the input DataFrame in-place.

    """
    # Keep only the 'Observation Date' and 'Observation Value' columns
    dataFrame.drop(dataFrame.columns.difference(['Observation Date', 'Observation Value']), 1, inplace=True)
    
    # Convert 'Observation Date' to datetime and set it as the index
    dataFrame['Observation Date'] = pd.to_datetime(dataFrame['Observation Date'])
    dataFrame = dataFrame.set_index('Observation Date')
    
    return dataFrame