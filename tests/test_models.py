# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
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
Test cases for Product Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_models.py:TestProductModel

"""
import os
import logging
import unittest
from decimal import Decimal
from service.models import Product, Category, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.category, Category.CLOTHS)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = ProductFactory()
        product.id = None
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)
        # Check that it matches the original product
        new_product = products[0]
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(new_product.description, product.description)
        self.assertEqual(Decimal(new_product.price), product.price)
        self.assertEqual(new_product.available, product.available)
        self.assertEqual(new_product.category, product.category)

    def test_update_a_product(self):
        """It should Update a product and assert that it changes"""
        product = ProductFactory.create(name="Old Product", description="Old description", price=5.0, available=False, category=Category.ELECTRONICS)
        product.name = "Updated Product"
        product.description = "Updated description"
        product.price = 25.0
        product.available = True
        product.category = Category.CLOTHS
        product.save()

        updated_product = Product.query.get(product.id)
        self.assertEqual(updated_product.name, "Updated Product")
        self.assertEqual(updated_product.description, "Updated description")
        self.assertEqual(updated_product.price, 25.0)
        self.assertTrue(updated_product.available)
        self.assertEqual(updated_product.category, Category.CLOTHS)

    def test_delete_a_product(self):
        """It should Delete a product and assert that it is removed"""
        product = ProductFactory.create(name="Product to Delete", description="Description", price=15.0, available=True, category=Category.FURNITURE)
        product_id = product.id
        product.delete()

        deleted_product = Product.query.get(product_id)
        self.assertIsNone(deleted_product)

    def test_list_all_products(self):
        """It should List all products"""
        ProductFactory.create(name="Product 1", description="Description 1", price=10.0, available=True, category=Category.ELECTRONICS)
        ProductFactory.create(name="Product 2", description="Description 2", price=20.0, available=False, category=Category.CLOTHS)

        products = Product.all()
        self.assertEqual(len(products), 2)

    def test_search_by_name(self):
        """It should Search a product by name"""
        product = ProductFactory.create(name="Unique Product", description="Description", price=12.5, available=True, category=Category.ELECTRONICS)
        found_product = Product.query.filter_by(name="Unique Product").first()
        self.assertEqual(found_product.name, "Unique Product")

    def test_search_by_category(self):
        """It should Search a product by category"""
        product = ProductFactory.create(name="Category Product", description="Description", price=8.0, available=True, category=Category.FURNITURE)
        found_product = Product.query.filter_by(category=Category.FURNITURE).first()
        self.assertEqual(found_product.category, Category.FURNITURE)

    def test_search_by_availability(self):
        """It should Search a product by availability"""
        product = ProductFactory.create(name="Available Product", description="Description", price=10.0, available=True, category=Category.ELECTRONICS)
        found_product = Product.query.filter_by(available=True).first()
        self.assertTrue(found_product.available)
