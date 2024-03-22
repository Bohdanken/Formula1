from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from time import strftime

from Formula1 import settings

# GENERAL FIELD LIMIT
NAME_MAX_LENGTH = 64
DESC_MAX_LENGTH = 4_096


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

    def get_name(self):
        return self.username


class NameSlugMixin(models.Model):
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        year: str = str(self.date_added.year)
        name: str = self.name
        self.slug = slugify(name + '-' + year)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True

    def lend_slug(self, increment):
        year = self.date_added.year + increment
        return slugify(self.name + '-' + str(year))


class Clone:
    @staticmethod
    def clone_all(self, copies):
        all = self.objects.all()
        for cat in all:
            clone = cat.clone()
            n = copies
            while (n - 1 > 0):
                clone = clone.clone()
                n -= 1


class Category(NameSlugMixin, models.Model):
    GENERAL = "GE"
    OPERATION = "OP"
    EVEHICLE = "EV"
    CHOICES = [
        (GENERAL, "General"),
        (OPERATION, "Operations"),
        (EVEHICLE, "Electric Vehicle"),
    ]

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=False, null=False)
    description = models.CharField(max_length=DESC_MAX_LENGTH)
    date_added = models.DateTimeField(null=False, default=timezone.now())
    parent = models.CharField(max_length=NAME_MAX_LENGTH, choices=CHOICES, default=GENERAL)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name} {str(self.date_added.year)}'

    def get_name(self):
        return self.slug

    def clone(self):
        reference = Category.objects.get(slug=self.slug)
        name = reference.name
        description = reference.description
        year = reference.date_added.year - 1
        date_added = reference.date_added.replace(year=year)
        parent = reference.parent
        clone = Category.objects.create(name=name, description=description, date_added=date_added, parent=parent)
        clone.save()
        print(f"CATEGORY clone successful - {clone.slug} copy FROM {self.slug}")
        return clone


class Topic(NameSlugMixin, models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=False, null=False)
    description = models.CharField(max_length=DESC_MAX_LENGTH)
    date_added = models.DateTimeField(null=True, default=timezone.now())
    category = models.ForeignKey(Category, related_name='topics', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} {str(self.date_added.year)}'

    def get_name(self):
        return self.slug

    def clone(self):
        reference = Topic.objects.get(slug=self.slug)
        name = reference.name
        description = reference.description
        year = reference.date_added.year - 1
        date_added = reference.date_added.replace(year=year)
        cat_slug = slugify(reference.category.name + '-' + str(year))
        category = Category.objects.get(slug=cat_slug)
        clone = Topic.objects.create(name=name, description=description, date_added=date_added, category=category)
        clone.save()
        print(f"TOPIC clone successful - {clone.slug} copy FROM {self.slug}")
        return clone


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
    date_added = models.DateTimeField(null=False, default=timezone.now())
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE)

    def __str__(self):
        return self.get_name()

    def get_name(self):
        return f'{self.title}-{self.pk}'

    def clone(self):
        reference = Post.objects.get(pk=self.pk)
        title = reference.title
        description = reference.description
        content = reference.content
        viewership = reference.viewership
        user = reference.user
        year = reference.date_added.year - 1
        date_added = reference.date_added.replace(year=year)
        top_slug = slugify(reference.topic.name + '-' + str(year))
        topic = Topic.objects.get(slug=top_slug)
        clone = Post.objects.create(title=title, date_added=date_added, topic=topic, user=user)
        clone.description = description
        clone.content = content
        clone.viewership = viewership
        clone.save()
        print(f"POST clone successful - {clone.get_name()} copy FROM {self.get_name()}")
        return clone


class Team(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    description = models.CharField(max_length=DESC_MAX_LENGTH)
    slug = models.SlugField(null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Team, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name


class TeamLead(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team = models.OneToOneField(Team, on_delete=models.CASCADE, blank=False)
    topic_access = models.ManyToManyField(Topic, related_name="access", blank=True)

    class Meta:
        db_table = "Team Lead"

    def __str__(self):
        return f'{self.user.get_name()} : {self.team.get_name()}'

    def get_name(self):
        return self.user.name


class TeamMember(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        db_table = "Team Member"

    def __str__(self):
        return f'{self.user.get_name()} : {self.team.get_name()}'

    def get_name(self):
        return self.user.name
