def session_has_key():
    """
    Check if EasyData API key has been verified for the current session.

    Returns
    -------
    bool
        True if EasyData API key is already verified for the current session, False otherwise.
    """
    global Easydata_key

    return 'Easydata_key' in globals()