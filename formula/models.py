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
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    description = models.CharField(max_length=DESC_MAX_LENGTH)
    forum_has = models.IntegerField(default=0)
    date_added = models.DateTimeField()

    def __str__(self):
        return self.name
    
class Subcategory(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    description = models.CharField(max_length=DESC_MAX_LENGTH)
    category_has = models.IntegerField(default=0)
    date_added = models.DateTimeField()

    def __str__(self):
        return self.name
    
class Topic(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    description = models.CharField(max_length=DESC_MAX_LENGTH)
    subcategory_has = models.IntegerField(default=0)
    date_added = models.DateTimeField()

    def __str__(self):
        return self.name
    
class Post(models.Model):
    CONTENT_MAX_LENGTH = 8192
    FILES_MAX_LENGTH = 512

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    description = models.CharField(max_length=DESC_MAX_LENGTH)
    content = models.CharField(max_length=CONTENT_MAX_LENGTH)
    file = models.CharField(max_length=FILES_MAX_LENGTH)
    viewership = models.IntegerField(default=0)
    topic_has = models.IntegerField(default=0)
    date_added = models.DateTimeField()

    def __str__(self):
        return self.name
    
class User(models.Model):
    student_id = models.IntegerField(unique=True, null=False)
    first_name = models.CharField(max_length=NAME_MAX_LENGTH)
    last_name = models.CharField(max_length=NAME_MAX_LENGTH)
# comment: upload_to is null
    picture = models.ImageField()
# comment ends
    description = models.CharField(max_length=DESC_MAX_LENGTH)
    admin = models.BooleanField(default=False)

class Team(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    description = models.CharField(max_length=DESC_MAX_LENGTH)

class TeamLead(models.Model):
    lead_in = models.IntegerField(default=0)

class TeamMember(models.Model):
    member_in = models.IntegerField(default=0)

class HasAccess(models.Model):
    subcategory = models.IntegerField(default=0)
    team_lead = models.IntegerField(default=0)

