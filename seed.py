from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add Users
eddie = User(first_name='Eddie', last_name="Sandler",image_url="https://eddiesandler.github.io/resources/images/avatar.jpg")
barbara = User(first_name='Barbara', last_name="Hessel", image_url=None)
bruce = User(first_name='Bruce', last_name="Sandler",image_url="https://eddiesandler.github.io/resources/images/Bruce.jpg")

# Add new objects to session, so they'll persist
db.session.add(eddie)
db.session.add(barbara)
db.session.add(bruce)

# Commit--otherwise, this never gets saved!
db.session.commit()
