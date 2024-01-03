"""Unit tests for an ipv4ac module.

"""

import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../src/ipv4ac"))

from ipv4ac import ipv4_address_check  # pylint: disable=C0413


class TestIPV4AC(unittest.TestCase):
    """Unit tests for an ipv4_address_check function.

    """

    def test_incorrect_data_type(self):
        """A test for incorrect argument type.

        """
        self.assertEqual(ipv4_address_check(1), 2)
        self.assertEqual(ipv4_address_check([]), 2)
        self.assertEqual(ipv4_address_check(()), 2)
        self.assertEqual(ipv4_address_check(True), 2)
        self.assertEqual(ipv4_address_check(2.13), 2)

    def test_correct_addresses(self):
        """A test for a correct IP address.

        """
        list_of_addresses = [
            "192.168.1.1",
            "0.0.0.0",
            "255.255.255.255",
            "10.0.0.0",
            "172.16.0.1",
            "127.0.0.1",
        ]
        for address in list_of_addresses:
            self.assertEqual(ipv4_address_check(address), 0)

    def test_out_of_range(self):
        """A test to check an octet out of range.
        
        """
        list_of_addresses = [
            "256.0.0.0",
            "0.256.0.0",
            "0.0.256.0",
            "0.0.0.256",
            "-1.0.0.0",
            "0.-1.0.0.",
            "0.0.-1.0",
            "0.0.0.-1",
        ]
        for address in list_of_addresses:
            self.assertEqual(ipv4_address_check(address), 1)


if __name__ == "__main__":
    unittest.main()
