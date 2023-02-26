def save(data:dict[str, str], name:str):
    """
    This method saves some data associated to a name (to retrieve the data back).
    Previously saved data will be overwritten.
    :param data: A key-value dictionary containing the variables names (as keys) and their data (as values).
    :param name: The name to use to store the data and to retrieve it back (the identity of the owner of the data).
    """

def load(name:str) -> dict[str, str]:
    """
    Can load some previously saved data on the disk (if any).
    Returns an empty dictionary if no data was found / in case of failure.
    :param name: The name of the owner of the data, to get its data back.
    :return: The data itself, or an empty dictionary.
    """
    return {}