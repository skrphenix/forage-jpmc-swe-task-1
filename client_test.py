import unittest
import json
import urllib.request
import random

from client3 import getDataPoint, getRatio


class ClientTest(unittest.TestCase):
    def test_getDataPoint_calculatePrice(self):
        quotes = [
            {'top_ask': {'price': 121.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453',
             'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
            {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453',
             'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
        ]
        for quote in quotes:
            stock = quote["stock"]
            bid_price = quote["top_bid"]["price"]
            ask_price = quote["top_ask"]["price"]
            price = (bid_price + ask_price) / 2

            self.assertEqual(getDataPoint(quote), (stock, bid_price, ask_price, price))

    def test_getDataPoint_calculatePriceBidGreaterThanAsk(self):
        quotes = [
            {'top_ask': {'price': 119.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453',
             'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
            {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453',
             'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
        ]
        for quote in quotes:
            stock = quote["stock"]
            bid_price = quote["top_bid"]["price"]
            ask_price = quote["top_ask"]["price"]
            price = (bid_price + ask_price) / 2

            self.assertEqual(getDataPoint(quote), (stock, bid_price, ask_price, price))

    def test_getRatio(self):
        quotes = [
            {'top_ask': {'price': 121.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453',
             'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
            {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453',
             'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
        ]

        prices = {}
        for quote in quotes:
            stock, _, _, price = getDataPoint(quote)
            prices[stock] = price

        price_a, price_b = prices["ABC"], prices["DEF"]
        self.assertEqual(getRatio(price_a, price_b), price_a / price_b)

    def test_server(self):
        query = "http://localhost:8080/query?id={}"
        quotes = json.loads(urllib.request.urlopen(query.format(random.random())).read())

        prices = {}
        for quote in quotes:
            stock, _, _, price = getDataPoint(quote)
            prices[stock] = price

        price_a, price_b = prices["ABC"], prices["DEF"]
        self.assertEqual(getRatio(price_a, price_b), price_a / price_b)


if __name__ == '__main__':
    unittest.main()
