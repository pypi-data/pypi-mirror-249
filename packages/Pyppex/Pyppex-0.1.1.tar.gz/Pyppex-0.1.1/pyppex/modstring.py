from typing import Literal, Any

def modstring(element:Any, mod:Literal['green', 'yellow', 'red', 'blue', 'bold', 'italic', 'underline']) -> str:
    """
    Modifies the element passed to turn it into string and adding one of the mod list.

    Args:
    -----
        - `element`: any type of class object to turn into string and to be modified.
        - `mod` (str): modification to add to the text.
    
    Returns:
    --------
        - `str`: modified text.
    """
    mods = {'green':'\033[32m', 'yellow':'\033[33m', 'red':'\033[31m', 'blue':'\033[34m', \
            'bold':'\033[1m', 'italic':'\033[3m', 'underline':'\033[4m', \
            'end':'\033[0m'}
    try:
        return mods.get(mod) + str(element) + mods.get('end')
    
    except ValueError:
        print('The value passed to "color" is not listed.')