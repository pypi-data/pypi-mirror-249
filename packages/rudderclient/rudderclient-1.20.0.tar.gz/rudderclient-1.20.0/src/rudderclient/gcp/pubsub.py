"""
This library provides an easy way to interact with Pub/Sub API.

"""


from google.cloud import pubsub_v1


def write_message(project_id, topic_id, message_str, **kwargs):
    """
    Publish a message in Pub Sub.

    Parameters:
    ----------
        project_id: The ID of the gcp project where you want to publish a message.
        topic_id: The topic name where you want to publish the message.
        **kwargs: Dictionary with the necessary attributes and its values
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    # Data must be a bytestring
    message = message_str.encode("utf-8")

    future = publisher.publish(topic_path, message, **kwargs)

    result = future.result()

    return result
