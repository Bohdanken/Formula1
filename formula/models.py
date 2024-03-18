from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone

# GENERAL FIELD LIMIT
NAME_MAX_LENGTH = 64
DESC_MAX_LENGTH = 512

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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    student_id = models.IntegerField(unique=True, null=False, default=0)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.CharField(max_length=DESC_MAX_LENGTH, blank=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_username()


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
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)

    def __str__(self):
        return self.author.get_username()


class Team(NameSlugMixin, models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    description = models.CharField(max_length=DESC_MAX_LENGTH)

    def __str__(self):
        return self.name
    
    def get_team_name(self):
        return self.name


class TeamLead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    topic_access = models.ManyToManyField(Topic, related_name="access")

    class Meta:
        db_table = "Team Lead"

    def __str__(self):
        return f'{self.user.get_username()} : {self.team.get_team_name()}'


class TeamMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        db_table = "Team Member"

    def __str__(self):
        return f'{self.user.get_username()} : {self.team.get_team_name()}'
