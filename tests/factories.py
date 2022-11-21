# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test Factory to make fake objects for testing
"""
from datetime import date

import factory
from factory.fuzzy import FuzzyDate
from service.models import Order, Item
import random


class OrderFactory(factory.Factory):
    """Creates fake orders that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Order

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("first_name")
    address = factory.Faker("address")
    date_created = FuzzyDate(date(2008, 1, 1))


class ItemFactory(factory.Factory):
    """Creates fake Items for orders"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""
        model = Item

    id = factory.Sequence(lambda n: n)
    product_id = random.randint(1, 20000)
    price = random.random() * 10 + 10
    quantity = random.randint(1, 20)
    order_id = random.randint(1, 20)
    status = "active"
    # order = factory.SubFactory(OrderFactory)
