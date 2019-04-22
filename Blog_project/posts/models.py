from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from tinymce import HTMLField

User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=25)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField(null=True, blank=True)
    # comments_count = models.IntegerField(default=0)
    # view_count = models.IntegerField(default=0)
    thumbnail = models.ImageField()
    # author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL)

    # if you want to post create by the auther only then uncomment the below line
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField(default=True)
    previous_post = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='previous', blank=True, null=True)
    next_post = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='next', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'pk' : self.pk,
        })

    def get_update_url(self):
        return reverse('post-update', kwargs={
            'pk' : self.pk,
        })

    def get_delete_url(self):
        return reverse('post-delete', kwargs={
            'pk' : self.pk,
        })

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comments_count(self):
        return Comment.objects.filter(post=self).count()

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
