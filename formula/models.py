from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from Formula1 import settings

# GENERAL FIELD LIMIT
NAME_MAX_LENGTH = 64
DESC_MAX_LENGTH = 512


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        if not username:
            raise ValueError(_('The Username field must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Create and return a superuser with an email, username, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, primary_key=True)
    username = models.CharField(_('username'), unique=True, max_length=30)
    student_id = models.IntegerField(unique=True, null=False, default=0)
    picture = models.ImageField(upload_to='profile_images', default='Default_pfp.svg')
    bio = models.TextField(max_length=DESC_MAX_LENGTH, blank=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class NameSlugMixin(models.Model):
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Category(NameSlugMixin, models.Model):
    GENERAL = "GE"
    OPERATION = "OP"
    EVEHICLE = "EV"
    CHOICES = [
        (GENERAL, "General"),
        (OPERATION, "Operations"),
        (EVEHICLE, "Electric Vehicle"),
    ]

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    description = models.CharField(max_length=DESC_MAX_LENGTH)
    date_added = models.DateTimeField(null=True)
    parent = models.CharField(max_length=NAME_MAX_LENGTH, choices=CHOICES, default=GENERAL)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Topic(NameSlugMixin, models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    description = models.CharField(max_length=DESC_MAX_LENGTH)
    date_added = models.DateTimeField(null=True)
    category = models.ForeignKey(Category, related_name='topics', on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Post(models.Model):
    CONTENT_MAX_LENGTH = 8192
    FILES_MAX_LENGTH = 512

    title = models.CharField(max_length=NAME_MAX_LENGTH)
    description = models.CharField(max_length=DESC_MAX_LENGTH)
    content = models.CharField(max_length=CONTENT_MAX_LENGTH)
    # comment: use FileField() here?
    file = models.FileField(upload_to='post_files/', blank=True)
    # comment end
    viewership = models.IntegerField(default=0)
    date_added = models.DateTimeField()
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Team(NameSlugMixin, models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    description = models.CharField(max_length=DESC_MAX_LENGTH)

    def __str__(self):
        return self.name

    def get_team_name(self):
        return self.name


class TeamLead(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    topic_access = models.ManyToManyField(Topic, related_name="access")

    class Meta:
        db_table = "Team Lead"

    def __str__(self):
        return f'{self.user.get_username()} : {self.team.get_team_name()}'


class TeamMember(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        db_table = "Team Member"

    def __str__(self):
        return f'{self.user.get_username()} : {self.team.get_team_name()}'
