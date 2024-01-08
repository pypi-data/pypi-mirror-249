#!/usr/bin/env python
# coding: utf-8

# In[8]:


import re

def EasyData_key_setup(api_key):
    """
    Verify and store the EasyData API key.

    Parameters
    ----------
    api_key : str
        The EasyData API key for the State Bank of Pakistan's EasyData database.

    Returns
    -------
    None
        If the key is verified, it is stored in the Easydata_key variable and a success message is printed.

    Raises
    ------
    ValueError
        If the provided key is not 40 characters long or starts with a non-alphabetic character.
    """
    

    try:
        # Check if the key is 40 characters long
        if len(api_key) != 40:
            raise ValueError("The key should be exactly 40 characters long.")

        # Check if the key starts with an alphabet character
        if not re.match("^[a-zA-Z]", api_key):
            raise ValueError("The key should start with an alphabet character.")

        # Set the global variable
        global Easydata_key
        Easydata_key = api_key
        print("EasyData API key Verified")
    except ValueError as e:
        print(f"Error: {e}")

# Example usage

#EasyData_key_setup("C10D3D29160CE5693F56AA9846ABB2C438D8B230")


# In[9]:


def session_has_key():
    """
    Check if EasyData API key has been verified for the current session.

    Returns
    -------
    bool
        True if EasyData API key is already verified for the current session, False otherwise.
    """

    return 'Easydata_key' in globals()


# In[10]:


def get_easydata_key():
    """
    Print the EasyData API key if entered for the current session.

    Returns
    -------
    None
        If EasyData API key is entered, print the key.
    ValueError
        If no EasyData API key has been entered for the current session.
    """

    if 'Easydata_key' in globals():
        print(f"EasyData API key for the current session: {Easydata_key}")
    else:
        raise ValueError("No EasyData API key has been entered for the current session.")

# Example usage

#get_easydata_key()


# # DOWNLOAD SERIES IN A CSV FILE IN CURRENT DIRECTORY

# In[11]:


import requests
import os
import pandas as pd

def download_series(Series_ID, Start_date, End_date, format="csv"):
    """
    Download time-series data from the EasyData platform of the State Bank of Pakistan and save as CSV.

    Parameters
    ----------
    Series_ID : str
        The ID of the series.
    Start_date : str
        The start date for the series in the format "YYYY-MM-DD".
    End_date : str
        The end date for the series in the format "YYYY-MM-DD".
    format : str, optional
        The format of the downloaded data, either "json" or "csv" (default is "csv").

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the data from the CSV file.

    Raises
    ------
    ValueError
        If the format is not "json" or "csv" or if the request is unsuccessful.
    """
    # Check if the format is valid
    if format not in ["json", "csv"]:
        raise ValueError("Invalid format. Supported formats are 'json' and 'csv'.")

    # Construct the URL for the HTTP GET request
    url = f"https://easydata.sbp.org.pk/api/v1/series/{Series_ID}/data?api_key={Easydata_key}&start_date={Start_date}&end_date={End_date}&format={format}"

    try:
        # Make the HTTP GET request
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        response.raise_for_status()

        # Get the current working directory
        current_directory = os.getcwd()

        # Construct the file path for the CSV file in the current directory
        csv_file_path = os.path.join(current_directory, f"{Series_ID}_{Start_date}_{End_date}.{format}")

        # Write the downloaded content to the CSV file
        with open(csv_file_path, "w", encoding="utf-8") as csv_file:
            csv_file.write(response.text)

        print(f"CSV data saved to {csv_file_path}")

        # Load CSV as DataFrame
        data_frame = pd.read_csv(csv_file_path,usecols=range(8))

        return data_frame

    except requests.exceptions.HTTPError as errh:
        raise ValueError(f"HTTP Error: {errh}")
    except requests.exceptions.RequestException as err:
        raise ValueError(f"Request Error: {err}")

# Example usage

#data_frame = download_series("Series_ID", "Start_date" ,"End_date", format)
  


# # Download Series in a Pandas DataFrame Format for Further Analysis

# In[5]:


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

# Example Usage

#build_time_series(data_frame)


# In[7]:


def plot_time_series(data_frame):
    """
    Plot a time-series using Plotly Express.

    Parameters
    ----------
    dataFrame : pandas.DataFrame
        Input DataFrame containing columns 'Observation Date' and 'Observation Value'.

    Returns
    -------
    None
        Displays the interactive time-series plot using Plotly Express.

    Examples
    --------
    >>> import pandas as pd
    >>> data = {'Observation Date': ['2023-01-01', '2023-01-02'],
    ...         'Observation Value': [10, 15]}
    >>> df = pd.DataFrame(data)
    >>> plot_time_series(df)
    """

    import matplotlib.pyplot as plt
    import pandas as pd

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(data_frame['Observation Date'], data_frame['Observation Value'], color='blue', linestyle='-', linewidth=2, markersize=8)

    # Styling
    plt.title('Time-Series Graph', fontsize=16)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Observation Value', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)

    # Set a gray background
    plt.gca().set_facecolor('#F0F0F0')  # Adjust the color code as needed

    # Show the plot
    plt.show()

# Example Usage

    # Pass the dataFrame downloaded through build_time_series function into this function:
#plot_time_series(data_frame)


# In[ ]:




