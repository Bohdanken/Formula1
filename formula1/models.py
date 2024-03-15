from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    
    NAME_MAX_LENGTH = 128 # Class attribute to define max_length for name field, ensuring consistency and ease of change
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)# Unique category name with a defined maximum length
    description = models.TextField()# A text field for category descriptions, no max length

    # Integer fields for tracking the number of views and likes a category has, defaulting to 0
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    # A slug field for the category, ensuring URL friendliness and uniqueness
    slug = models.SlugField(unique=True)

    # Overrides the save method to automatically generate a slug from the category name before saving
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)  # Generates a slug based on the category name
        super(Category, self).save(*args, **kwargs)  # Calls the parent class's save method

    # Meta class to define plural name in admin interface
    class Meta:
        verbose_name_plural = 'categories'

    # Returns the category name when the object is printed, improving readability
    def __str__(self):
        return self.name

# Define the Topic model.
class Topic(models.Model):
    category = models.ForeignKey(Category, related_name='topics', on_delete=models.CASCADE)  # Link to the Category model.
    name = models.CharField(max_length=128)  # Topic name.
    description = models.TextField()  # Description of the topic.

# Define the Post model.
class Post(models.Model):
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)  # Link to the Topic model.
    title = models.CharField(max_length=200)  # Title of the post.
    content = models.TextField()  # The main content of the post.
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # The author of the post, linked to the User model.
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-generated timestamp of when the post was created.
    year = models.DateField()  # Year associated with the post (if decided to place here).

class Page(models.Model):
    TITLE_MAX_LENGTH = 128  

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    def __str__(self):
        return self.user.username
