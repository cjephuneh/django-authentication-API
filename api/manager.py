from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    A Custom manager class for the Users model.

    Note:
    This manager class is used to customize the creation
    of user instances.
    """

    use_in_migrations = True

    def _create_user(self, username: str, email: str, password: str, **extra_fields):
        """
        Create and save a regular user with the given
        username, email, and password.

        Return Type -> Users():
        Users: The created user instance.
        """
        if not email:
            raise ValueError("email address must be required.")
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username: str, email: str, password: str, **extra_fields):
        """
        Create and save a regular user with the given
        username, email, and password.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(
        self, username: str, email: str, password: str, **extra_fields
    ):
        """
        Create and save a superuser with the given
        username, email, and password.

        Return Type -> Users():
        Users: The created superuser instance.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)
