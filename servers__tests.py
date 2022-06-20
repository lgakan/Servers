import unittest
from collections import Counter

from servers import Server, ListServer, Product, Client, MapServer, TooManyProductsFoundError

server_types = (ListServer, MapServer)


class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))


class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))


class MaxProduct(unittest.TestCase):
    def test_max_found_products_error(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1), Product('PW234', 5)]
        for server_type in server_types:
            server = server_type(products)
            self.assertRaises(TooManyProductsFoundError, server.get_entries, 2)


class SortList(unittest.TestCase):
    def test_total_sorted_products(self):
        products = [Product('P12', 1), Product('PP234', 3), Product('PP235', 2)]
        sorted_list = [Product('PP235', 2), Product('PP234', 3)]
        for server_type in server_types:
            server = server_type(products)
            self.assertEqual(sorted_list, server.get_entries(2))


class TestExceptionAndNoMatchingProducts(unittest.TestCase):
    def test_price_if_exception_raised(self):
        products_exception = [Product('PP234', 1), Product('PQ234', 1), Product('PW234', 1), Product('PE234', 1), Product('PR234', 1)]
        for server_type in server_types:
            server = server_type(products_exception)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(2))
    def test_if_no_products_matching(self):
        products_not_matching = [Product('A234', 2)] * Server.n_max_returned_entries
        for server_type in server_types:
            server = server_type(products_not_matching)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(2))

if __name__ == '__main__':
    unittest.main()
