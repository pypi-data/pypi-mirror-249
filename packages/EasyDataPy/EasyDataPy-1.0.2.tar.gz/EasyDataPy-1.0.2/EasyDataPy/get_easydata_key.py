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
    global Easydata_key

    if 'Easydata_key' in globals():
        print(f"EasyData API key for the current session: {Easydata_key}")
    else:
        raise ValueError("No EasyData API key has been entered for the current session.")