import factory
from factory.fuzzy import FuzzyChoice, FuzzyDecimal
from service.models import Product, Category
from faker import Faker

fake = Faker()

class ProductFactory(factory.Factory):
    """Creates fake products for testing"""

    class Meta:
        """Maps factory to data model"""
        model = Product

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda x: fake.name())  # Creează un nume fals pentru produs
    description = factory.LazyAttribute(lambda x: fake.text())  # Creează o descriere falsă pentru produs
    price = FuzzyDecimal(1.0, 1000.0)  # Creează un preț aleatoriu între 1.0 și 1000.0
    available = factory.LazyAttribute(lambda x: fake.boolean())  # Creează un status aleatoriu (True/False)
    category = FuzzyChoice([category.name for category in Category.objects.all()])  # Alegere aleatorie dintre categoriile existente în DB
