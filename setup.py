import random

from model import db, Donor, Donation 

db.connect()

# This line will allow you "upgrade" an existing database by
# dropping all existing tables from it.
db.drop_tables([Donor, Donation])

db.create_tables([Donor, Donation])

jae = Donor(name="Jae")
jae.save()

alice = Donor(name="Alice")
alice.save()

bob = Donor(name="Bob")
bob.save()

charlie = Donor(name="Charlie")
charlie.save()

xavier = Donor(name="Xavier")
xavier.save()

donors = [alice, bob, charlie, jae, xavier]

for x in range(20):
    Donation(donor=random.choice(donors), value=random.randint(100, 10000)).save()
