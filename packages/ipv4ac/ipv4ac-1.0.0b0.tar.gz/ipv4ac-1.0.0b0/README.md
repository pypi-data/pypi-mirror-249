
# IPv4AC

Internet Protocol Version 4 Address Check is a simple module provides a function to check if an IPv4 address has correct format.


## Installing

Install the module by [pip][1] (check [how to use pip][2]):

```
$ python3 -m pip install ipv4ac
```


## A simple example

```python
# Import the function from the module
from ipv4ac import ipv4_address_check

# Set an IPv4 address
ip_address = '192.168.100.1'

# Use the function to check the address
check_result = ipv4_address_check(ip_address)
```

[1]: https://pypi.org/ 
[2]: https://pip.pypa.io/en/stable/getting-started/