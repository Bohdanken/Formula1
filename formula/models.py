from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import datetime

# GENERAL FIELD LIMIT
NAME_MAX_LENGTH = 64
DESC_MAX_LENGTH = 512

class SlugMixin(models.Model):
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class StrMixin(models.Model):
    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True


class Category(SlugMixin, StrMixin, models.Model):
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
    forum_has = models.IntegerField(default=0)
    date_added = models.DateTimeField(null=True)
    parent = models.CharField(max_length=NAME_MAX_LENGTH, choices=CHOICES, default=GENERAL)

    class Meta:
        verbose_name_plural = 'Categories'

    
class Topic(SlugMixin, StrMixin, models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    description = models.CharField(max_length=DESC_MAX_LENGTH)
    date_added = models.DateTimeField(null=True)
    category = models.ForeignKey(Category, related_name='topics', on_delete=models.CASCADE)


class UserProfile(StrMixin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.IntegerField(unique=True, null=False, default=0)
    first_name = models.CharField(max_length=NAME_MAX_LENGTH)
    last_name = models.CharField(max_length=NAME_MAX_LENGTH)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.CharField(max_length=DESC_MAX_LENGTH, blank=True)
    admin = models.BooleanField(default=False)


class Post(StrMixin, models.Model):
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
    author = models.ForeignKey(UserProfile, related_name='author', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Team(StrMixin, models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    description = models.CharField(max_length=DESC_MAX_LENGTH)


class TeamLead(StrMixin, models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    leader = models.BooleanField(default=False)
    topic_access = models.ManyToManyField(Topic, related_name="access")

    class Meta:
        db_table = "Team Lead"


class TeamMember(StrMixin, models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        db_table = "Team Member"
