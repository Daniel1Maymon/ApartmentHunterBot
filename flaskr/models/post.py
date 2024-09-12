from pymongo.errors import PyMongoError

from flaskr.database import mongo


def update_posts_by_filter(filter_criteria, update_values):
    """
    Updates posts in the database based on the given filter criteria.

    Parameters:
    - filter_criteria: A dictionary containing the filter criteria (e.g., {'link': 'https://example.com'}).
    - update_values: A dictionary containing the fields to update and their new values (e.g., {'hasBeenSent': True}).

    Returns:
    - The number of documents that were updated.
    """

    result = mongo.db.collection.update_many(
        filter=filter_criteria, update={"$set": update_values}
    )

    return result.modified_count


def get_posts_by_filter(filter_criteria):
    """
    Retrieves posts from the database based on the given filter criteria.

    Parameters:
    - filter_criteria: A dictionary containing the filter criteria (e.g., {'link': 'https://example.com'}).

    Returns:
    - A list of posts that match the filter criteria.
    """
    posts = mongo.db.collection.find(filter_criteria)
    return list(posts)


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


def insert_posts(posts: list):
    try:
        result = mongo.db.collection.insert_many(documents=posts)

    except PyMongoError as e:
        raise PyMongoError(f"An error occurred while saving the posts: {e}")


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
