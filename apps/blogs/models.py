from ckeditor.fields import RichTextField
from django.db import models

from apps.users.models import UserModel


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AuthorsModel(BaseModel):
    full_name = models.CharField(max_length=128)
    profession = models.CharField(max_length=128)
    email = models.EmailField()
    bio = models.TextField()
    photo = models.ImageField(upload_to='photos/')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class CategoriesModel(BaseModel):
    title = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class TagsModel(BaseModel):
    title = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class BlogsModel(BaseModel):
    title = models.CharField(max_length=255)
    description = RichTextField()
    author = models.ForeignKey(AuthorsModel, on_delete=models.CASCADE, related_name='blogs')
    image = models.ImageField(upload_to='blogs/')
    category = models.ManyToManyField(CategoriesModel, related_name='blogs')
    tag = models.ManyToManyField(TagsModel, related_name='blogs')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'


class CommentsModel(BaseModel):
    blog = models.ForeignKey(BlogsModel, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    text = models.TextField()
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.blog.title}"

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'



