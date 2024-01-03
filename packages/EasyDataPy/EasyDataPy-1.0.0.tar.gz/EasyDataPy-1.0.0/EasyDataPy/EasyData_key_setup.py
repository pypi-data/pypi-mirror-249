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
        If the key is verified, it is stored in the Easydata_key variable.

    Raises
    ------
    ValueError
        If the provided key is not 40 characters long or starts with a non-alphabetic character.
    """

    # Check if the key is 40 characters long
    if len(api_key) == 40:
        # Check if the key starts with an alphabet character
        if re.match("^[a-zA-Z]", api_key):
            global Easydata_key
            Easydata_key = api_key
            print("EasyData API key Verified")
        else:
            raise ValueError("The key should start with an alphabet character.")
    elif len(api_key) < 40:
        raise ValueError("The key is less than 40 characters. Please check again; it should be 40 characters long.")
    else:
        raise ValueError("The key is longer than 40 characters. Please check again; it should be 40 characters long.")