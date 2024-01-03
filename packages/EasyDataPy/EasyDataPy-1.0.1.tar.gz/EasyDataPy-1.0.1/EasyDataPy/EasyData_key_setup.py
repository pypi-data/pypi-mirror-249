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
    global Easydata_key

    try:
        # Check if the key is 40 characters long
        if len(api_key) != 40:
            raise ValueError("The key should be exactly 40 characters long.")

        # Check if the key starts with an alphabet character
        if not re.match("^[a-zA-Z]", api_key):
            raise ValueError("The key should start with an alphabet character.")

        # Set the global variable
        Easydata_key = api_key
        print("EasyData API key Verified")
    except ValueError as e:
        print(f"Error: {e}")

# Example usage
EasyData_key_setup("C10D3D29160CE5693F56AA9846ABB2C438D8B230")

