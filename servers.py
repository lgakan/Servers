#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from abc import ABC, abstractmethod
from typing import Optional, List, TypeVar, Dict


class Product:
    def __init__(self, name: str, price: float):
        if re.fullmatch('[a-zA-Z]+[0-9]+', name): #tutaj był bład
            self.name = name
            self.price = price
        else:
            raise ValueError

    def __eq__(self, other):
        return self.price == other.price and self.name == other.name

    def __hash__(self):
        return hash((self.name, self.price))


class ServerError(Exception):
    pass

class TooManyProductsFoundError(ServerError):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    def __init__(self, val: float, new_value: float):
        self.val = val
        self.new_value = new_value
        self.message = f'There is too many products: {self.val},there should be {self.new_value} products'

    def __str__(self):
        return self.message


class Server(ABC):
    n_max_returned_entries = 2

    @abstractmethod
    def get_all_products(self, n_letters: int = 1):
        raise NotImplementedError

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_entries(self, n_letters: int = 3):
        # raise NotImplementedError
        products_list = self.get_all_products(n_letters)
        regex = r'^[a-zA-Z]{' + str(n_letters) + r'}\d{2,3}$'
        # super(get_all_products())
        entries = []
        for p in products_list:
            if re.match(regex, p.name):
                entries.append(p)
            if len(entries) > self.n_max_returned_entries:
                raise TooManyProductsFoundError(val=len(entries), new_value=self.n_max_returned_entries)
        # return entries #tuaj są nieposortowana lista
        return sorted(entries, key=lambda price_of_product: price_of_product.price)


class ListServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products = products

    def get_all_products(self, n_letters: int = 3):
        answer = []
        for i in self.products:
            valid_item = re.search(r'^[a-zA-Z]{' + str(n_letters) + r'}\d{2,3}$', i.name)

            if valid_item:
                answer.append(i)
        return answer


class MapServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products: Dict[str, Product] = {product.name: product for product in products}

    def get_all_products(self, n_letters: int = 1) -> List[Product]:
        answer = []
        for prod_name in self.products:
            valid_item = re.search(r'^[a-zA-Z]{' + str(n_letters) + r'}\d{2,3}$', prod_name)
            if valid_item:
                answer.append(self.products[prod_name])
            if len(answer) > self.n_max_returned_entries:
                raise TooManyProductsFoundError(val=len(answer), new_value=self.n_max_returned_entries)
        return answer


HelperType = TypeVar('HelperType', bound=Server)


class Client:
    def __init__(self, server: HelperType):
        self.Server: server = server
        self.Server: server.n_max_returned_entries

    def get_total_price(self, n_letters: int) -> Optional[float]:
        try:
            entries = self.Server.get_entries(n_letters)
        except TooManyProductsFoundError:
            return None
        if len(entries) == 0:
            return None
        total_amount = 0
        for elem in entries:
            total_amount += elem.price
        return total_amount
