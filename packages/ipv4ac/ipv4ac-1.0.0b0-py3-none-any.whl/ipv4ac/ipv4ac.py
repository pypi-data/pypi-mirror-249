""" A main module contains function for check if an IPv4 has a correct format.

"""

import re


def ipv4_address_check(ipv4: str) -> int:
    """Check if an IPv4 address has correct format.

    Args:
        ipv4 (str): A string contains IPv4 to verification.

    Returns:
        int: 0 if a correct format of IPv4 address.
        int: 1 if a not correct format of IPv4 address.
        int: 2 if a parameter has different type than string.

    """

    if not isinstance(ipv4, str):
        return 2

    regexp = "^([0-9]{1,3}\\.){3}[0-9]{1,3}$"
    if not re.match(regexp, ipv4):
        return 1

    list_of_octets = ipv4.split(".")
    for octet in list_of_octets:
        if not 0 <= int(octet) <= 255:
            return 1

    return 0
