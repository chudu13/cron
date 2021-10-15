from django.db import models
import uuid
from users.models import Profile


class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    demo_link = models.CharField(max_length=1500, null=True, blank=True)
    source_link = models.CharField(max_length=1500, null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    created = models.DateTimeField(auto_now_add=True)
    like_total = models.IntegerField(default=0, null=True, blank=True)
    like_ratio = models.IntegerField(default=0, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title

    @property
    def get_like_count(self):
        reviews = self.review_set.all()
        like = reviews.filter(value='up').count()
        total_lakes = reviews.count()

        ratio = (like / total_lakes) * 100
        self.vote_total = total_lakes
        self.vote_ratio = ratio
        self.save()


class Review(models.Model):
    LIKE_TYPE = (
        ('up', 'Лайк'),
        ('down', 'Дизлайк')
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=120, choices=LIKE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
