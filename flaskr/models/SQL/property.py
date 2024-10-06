
from datetime import datetime, timezone
from flaskr.database import mySQL_db as db


# Define the Property model
class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)  
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=True)
    size = db.Column(db.Numeric(5, 2), nullable=True) 
    rooms = db.Column(db.Integer, nullable=True) 
    city = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    url = db.Column(db.String(255), nullable=True)
    sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    # updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Property {self.id} - {self.description}>'
