from django.db import models
from django.template.defaultfilters import slugify
from datetime import datetime

# Create your models here.

NAME_MAX_LENGTH = 64
DESC_MAX_LENGTH = 512


class Year(models.Model):
    year = models.IntegerField(default=datetime.now().year)
    description = models.CharField(max_length=DESC_MAX_LENGTH)


class Category(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    description = models.CharField(max_length=DESC_MAX_LENGTH)
    forum_has = models.IntegerField(default=0)
    date_added = models.DateTimeField()
    parent = models.CharField(max_length=NAME_MAX_LENGTH)

    parent_choices = [
        ("WELCOME"),
        ("OPERATIONS"),
        ("ELECTRIC VEHICLE"),
    ]

    def __str__(self):
        return self.name
    

class Topic(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    description = models.CharField(max_length=DESC_MAX_LENGTH)
    category_has = models.IntegerField(default=0)
    date_added = models.DateTimeField()
    category = models.ForeignKey(Category, related_name='topics', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Post(models.Model):
    CONTENT_MAX_LENGTH = 8192
    FILES_MAX_LENGTH = 512

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    description = models.CharField(max_length=DESC_MAX_LENGTH)
    content = models.CharField(max_length=CONTENT_MAX_LENGTH)
# comment: use FileField() here?
    file = models.CharField(max_length=FILES_MAX_LENGTH)
# comment end
    viewership = models.IntegerField(default=0)
    topic_has = models.IntegerField(default=0)
    date_added = models.DateTimeField()
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class User(models.Model):
    student_id = models.IntegerField(unique=True, null=False)
    first_name = models.CharField(max_length=NAME_MAX_LENGTH)
    last_name = models.CharField(max_length=NAME_MAX_LENGTH)
# comment: upload_to is null
    picture = models.ImageField()
# comment end
    bio = models.CharField(max_length=DESC_MAX_LENGTH)
    admin = models.BooleanField(default=False)


class Team(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    description = models.CharField(max_length=DESC_MAX_LENGTH)


class TeamLead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    leader = models.BooleanField(default=False)
    topic_access = models.ManyToManyField(Topic, related_name="access", on_delete=models.CASCADE)


class TeamMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


