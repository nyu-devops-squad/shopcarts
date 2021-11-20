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
import factory
from factory.fuzzy import FuzzyChoice, FuzzyInteger
from services.models import Shopcart


class ShopcartFactory(factory.Factory):
    """ Creates fake shopcarts that you don't have to feed """

    class Meta:
        model = Shopcart

    product_id = FuzzyChoice(choices=[1001,2002,3003,4747,9999])
    customer_id = FuzzyChoice(choices=[1000,2000,3000,8000])
    product_name = FuzzyChoice(choices=["a","b","d","c","e"])
    product_price = FuzzyChoice(choices=[10.01,200.2,30,4747,999])
    quantity = FuzzyInteger(0, 10, step=1)
