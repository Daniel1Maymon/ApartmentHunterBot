from datetime import datetime
from bson.objectid import ObjectId
from flaskr.database import mongo

def insert_post(link, content):
    """
    Inserts a new post into the database.

    Parameters:
    - link: The URL link to the post.
    - content: The content/text of the post.

    Returns:
    - The ID of the inserted post.
    """
    
    pass

def get_post_by_id(post_id):
    """
    Retrieves a post by its ID.

    Parameters:
    - post_id: The ID of the post to retrieve.

    Returns:
    - The post document, or None if not found.
    """
    
    pass

def get_all_posts():
    """
    Retrieves all posts from the database.

    Returns:
    - A list of post documents.
    """
    
    pass


def delete_post(post_id):
    """
    Deletes a post by its ID.

    Parameters:
    - post_id: The ID of the post to delete.

    Returns:
    - The result of the delete operation.
    """
    
    pass
   