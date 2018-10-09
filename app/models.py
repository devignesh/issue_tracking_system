from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import make_password

# Create your models here.


class BaseTime(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            # password=make_password(password),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, access_token, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.access_token = access_token
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User table holds the user basic details.
    """
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=256)
    access_token = models.CharField(max_length=30)
    date_of_birth = models.CharField(max_length=30)
    role = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    is_authenticated = True
    is_anonymous = False
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['access_token', 'password']

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password


class Project(BaseTime):
    """
    Project table holds all the project data
    """
    title = models.CharField(max_length=50)
    description = models.TextField()
    languages = models.CharField(max_length=50)
    company_id = models.IntegerField(default=0)


class Issue(BaseTime):
    """
    Issue table holds all the issue for the projects
    """
    STATUS_OPEN = 'O'
    STATUS_INPROGRESS = 'IP'
    STATUS_CLOSED = 'C'
    STATUS_CHOICES = (
        (STATUS_OPEN, 'Open'),
        (STATUS_INPROGRESS, 'InProgress'),
        (STATUS_CLOSED, 'Closed'),
    )

    title = models.CharField(max_length=500)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignee_id')
    labels = models.CharField(max_length=50)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_OPEN)
    commands = models.ManyToManyField('Commands', related_name='commands_list')


class Commands(BaseTime):
    """
    Commands table holds all the discussions.
    """
    comment = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="issue_id")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
