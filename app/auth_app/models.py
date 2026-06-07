import bcrypt
from datetime import datetime, timedelta, UTC
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    '''
    Custom user model using:
    - email as the username field;
    - bcrypt for password hashing.
    '''

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def set_password(self, raw_password):
        self.password = bcrypt.hashpw(
            raw_password.encode('utf-8'),
            bcrypt.gensalt()).decode('utf-8'
        )
        self.save()

    def check_password(self, raw_password):
        return bcrypt.checkpw(
            raw_password.encode('utf-8'),
            self.password.encode('utf-8')
        )


class Role(models.Model):
    '''
    Model to represent user roles, such as admin, editor, viewer, etc.
    Each role can have multiple permissions associated with it.
    '''
    name = models.CharField(max_length=50, unique=True)


class Resource(models.Model):
    '''Model to represent resources in the application.'''
    name = models.CharField(max_length=50, unique=True)


class Action(models.Model):
    '''Model to represent user action on resource such as CRUD'''
    name = models.CharField(max_length=50, unique=True)


class Permission(models.Model):
    '''Model to represent permissions in the application.'''
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)


class UserRole(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE
    )

class RolePermission(models.Model):
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE
    )
    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE
    )


class RefreshToken(models.Model):
    '''
    Model to store refresh tokens for users.
    Each token is associated with a user and has an expiration time.
    '''

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        default=datetime.now(UTC) + timedelta(days=7)
    )
