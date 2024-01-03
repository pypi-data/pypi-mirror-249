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