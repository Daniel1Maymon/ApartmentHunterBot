from pymongo import MongoClient
from datetime import datetime, timezone
from flaskr.database import mongo
from pymongo.errors import PyMongoError

def save_schedule(schedule_data):
    """
    Saves a new schedule in the database or updates an existing one.

    Parameters:
    - schedule_data: A dictionary containing the schedule details.

    Returns:
    - The ID of the inserted or updated document.
    """
    schedule_data['created_at'] = datetime.now(timezone.utc).isoformat()
    schedule_data['updated_at'] = datetime.now(timezone.utc).isoformat()
    schedule_data['is_active'] = True

    existing_schedule = mongo.db.schedules.find_one({})

    if existing_schedule:
        result = mongo.db.schedules.update_one(
            {"_id": existing_schedule["_id"]},
            {"$set": schedule_data}
        )
        return existing_schedule["_id"] if result.modified_count > 0 else None
    else:
        result = mongo.db.schedules.insert_one(schedule_data)
        return result.inserted_id

def get_schedule(filter_criteria={}):
    """
    Retrieves a schedule from the database based on the given filter criteria.

    Parameters:
    - filter_criteria: A dictionary containing the filter criteria (e.g., {'is_active': True}).

    Returns:
    - The schedule document that matches the filter criteria.
    """
    return mongo.db.schedules.find_one(filter_criteria)

def update_schedule_by_filter(filter_criteria, update_values):
    """
    Updates schedules in the database based on the given filter criteria.

    Parameters:
    - filter_criteria: A dictionary containing the filter criteria (e.g., {'is_active': True}).
    - update_values: A dictionary containing the fields to update and their new values (e.g., {'end_option': 'on-date'}).

    Returns:
    - The number of documents that were updated.
    """
    result = mongo.db.schedules.update_many(
        filter=filter_criteria,
        update={'$set': update_values}
    )
    return result.modified_count

def delete_schedule(filter_criteria={}):
    """
    Deletes schedules from the database based on the given filter criteria.

    Parameters:
    - filter_criteria: A dictionary containing the filter criteria (e.g., {'is_active': False}).

    Returns:
    - The number of documents that were deleted.
    """
    result = mongo.db.schedules.delete_many(filter_criteria)
    return result.deleted_count