from google.cloud import secretmanager


def create_secret(project_id, secret_id):
    """
    Create a new secret.

    Parameters:
    ----------
        project_id: str
            Id of the project.
        secret_id: str
            Secret id name.
    """
    client = secretmanager.SecretManagerServiceClient()
    project_detail = f"projects/{project_id}"
    response = client.create_secret(
        request={
            "parent": project_detail,
            "secret_id": secret_id,
            "secret": {"replication": {"automatic": {}}},
        }
    )
    return response


def add_secret_version(project_id, secret_id, data):
    """
    Add a new payload version in the secret given.

    Parameters:
    ----------
        project_id: str
            Id of the project.
        secret_id: str
            Secret id name.
        data: str
            The secret payload you want to save.
    """
    client = secretmanager.SecretManagerServiceClient()
    parent = create_secret_path(project_id, secret_id)
    response = client.add_secret_version(
        request={"parent": parent, "payload": {"data": data.encode("UTF-8")}}
    )
    return response


def get_secret_name(project_id: str, secret_id: str):
    """
    Get information about the given secret. This only returns metadata about
    the secret container, not any secret material.

    Parameters:
    ----------
        project_id: str
            Id of the project.
        secret_id: str
            Secret id name.

    Returns:
    -------
    The name of the secret.
    """

    client = secretmanager.SecretManagerServiceClient()

    name = create_secret_path(project_id, secret_id)

    response = client.get_secret(request={"name": name})

    return response.name


def create_secret_path(project_id, secret_id):
    """
    Returns the secret path for google where the resource is.

    Parameters:
    ----------
        project_id: str
            Id of the project.
        secret_id: str
            Secret id name.

    Returns:
    -------
    The path value where the secret is saved in GCP.
    """
    client = secretmanager.SecretManagerServiceClient()
    secret_path = client.secret_path(project_id, secret_id)

    return secret_path


def access_latest_secret_version(secret_path):
    """
    Returns a secret value from secret manager service.

    Parameters:
    ----------
        secret_path: str
            Secret resource name like projects/xxxxxx/secrets/xxxxxxxx/versions/latest

    Returns:
    -------
    The value of the secret.
    """
    client = secretmanager.SecretManagerServiceClient()
    secret = client.access_secret_version(request={"name": secret_path})
    value = secret.payload.data.decode("UTF-8")
    return value


def list_secrets(project_id: str):
    """
    List all secrets in the given project.

    Parameters:
    ----------
        project_id: str
            Id of the project.

    Returns:
    -------
    The list with the secret names of the project.
    """

    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the parent project.
    parent = f"projects/{project_id}"
    secrets = []

    # Create a list with all secrets.
    for secret in client.list_secrets(request={"parent": parent}):
        secrets.append(secret.name)

    return secrets
