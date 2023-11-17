from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for Pets."""

    def setUp(self):
        """Clean up any existing pets."""

        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_greet(self):
        pet = Pet(name="TestPet", species="dog", hunger=10)
        self.assertEqual(pet.greet(), "I'm TestPet the dog")

    def test_feed(self):
        pet = Pet(name="TestPet", species="dog", hunger=10)
        pet.feed(5)
        self.assertEqual(pet.hunger, 5)

        pet.feed(999)
        self.assertEqual(pet.hunger, 0)

    def test_get_by_species(self):
        pet = Pet(name="TestPet", species="dog", hunger=10)
        db.session.add(pet)
        db.session.commit()

        dogs = Pet.get_by_species('dog')
        self.assertEqual(dogs, [pet])
