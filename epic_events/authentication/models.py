from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)

# Create your models here.


class UserManager(BaseUserManager):

    """
        Customisation of the User object using the BaseUserManager class.
        Custom users and super users.
    """

    def create_user(self, username, team, password=None):
        """
            Creates and saves user with given username and team
        """
        if not team:
            raise ValueError("Users must have a team")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(username=username, team=team)

        if team == "Gestion":
            user.is_admin = True
            user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        """
            Creates and saves superuser with given username and password
        """
        user = self.create_user(
            username,
            password=password,
            team="Gestion",
        )
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    """
        Customisation of the User object using the AbstractBaseUser class.
        Custom users and super users. (username/password/team)
    """

    use_in_migrations = True

    class Team(models.TextChoices):
        GESTION = 'Gestion'
        COMMERCIAL = 'Commercial'
        SUPPORT = 'Support'

    username = models.CharField(
        max_length=25,
        unique=True,
        null=False,
        blank=False,
        verbose_name='Nom'
    )
    team = models.fields.CharField(
        choices=Team.choices,
        max_length=25,
        null=False,
        blank=False,
        verbose_name='Equipe'
    )
    is_active = models.BooleanField(default=True, verbose_name='Actif')
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()
