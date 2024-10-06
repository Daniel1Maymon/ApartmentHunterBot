from flaskr.database import mySQL_db as db
from flaskr.models.SQL.property import Property

# save_post_to_db
def save_post_on_db(data):
    new_property = Property(
        price=data['price'],
        size=data['size'],
        rooms=data['rooms'],
        city=data['city'],
        address=data['address'],
        url=data['url'],
        description= data['description'],
        phone=data['phone']
    )
    
    db.session.add(new_property)
    db.session.commit()

# read_post_from_db

# update_post_from_db

# Check if post exists
def check_exists(str_to_check):
    str_to_check = f"%{str_to_check}%"
    
    # result = db.session.query(User).filter(User.email.ilike(substring)).all()

    result = db.session.query(Property).filter(Property.url.ilike(str_to_check)).first()
    
    return result