import requests
import os
import pandas as pd

def download_series(Series_ID, api_key, Start_date, End_date, format="csv"):
    """
    Download time-series data from the EasyData platform of the State Bank of Pakistan and save as CSV.

    Parameters
    ----------
    Series_ID : str
        The ID of the series.
    api_key : str
        The API key for the session.
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
    url = f"https://easydata.sbp.org.pk/api/v1/series/{Series_ID}/data?api_key={api_key}&start_date={Start_date}&end_date={End_date}&format={format}"

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
        data_frame = pd.read_csv(csv_file_path)

        return data_frame

    except requests.exceptions.HTTPError as errh:
        raise ValueError(f"HTTP Error: {errh}")
    except requests.exceptions.RequestException as err:
        raise ValueError(f"Request Error: {err}")