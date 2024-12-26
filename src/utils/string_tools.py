import re

def camel_to_snake(string: str,
                   lower: bool = True,
                   drop: str = None) -> str:
    """

    :param string: "MyName".
    :param lower: lower case or not
    :param drop: drop substring from input string.
    :return: "my_name" or "My_Name".
    """
    if drop is not None and drop in string:
        string = string.replace(drop, "")
    re_string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)

    return re_string.lower() if lower else re_string

