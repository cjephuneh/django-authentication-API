import secrets
import uuid


def get_unique_uuid() -> str:
    """
    This method return a Unique String ID
    """
    return str(uuid.uuid4())


def generate_unique_token(token_length: int = 48) -> str:
    """
    This method is to generate unique token string
    using secrets module.
    """
    return str(secrets.token_urlsafe(token_length))
