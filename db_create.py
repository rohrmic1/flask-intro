from app import db
from models import BlogPost

# create the database and the db table
db.create_all()

# insert data
# db.session.add(BlogPost("Good", "I\'m good."))
# db.session.add(BlogPost("Well", "I\'m well."))
# db.session.add(BlogPost("Excellent", "I\'m excellent."))
# db.session.add(BlogPost("Okay", "I\'m okay."))
# db.session.add(BlogPost("postgres", "local postgres instance"))

db.session.add(BlogPost("TBD", "{'comp': 'BRINE', 'jk': '80804946cbe61431', 'title': 'Markit EDM/SQL Server Database Developer', 'loc': 'Zürich, ZH'}"))

# commit the changes
db.session.commit()