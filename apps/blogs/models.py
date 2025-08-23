from django.db import models

from apps.users.models import UserModel


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CategoryModel(BaseModel):
    title = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class TagModel(BaseModel):
    title = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class BlogModel(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='blogs')
    image = models.ImageField(upload_to='blogs/')
    category = models.ManyToManyField(CategoryModel, related_name='blogs')
    tag = models.ManyToManyField(TagModel, related_name='blogs')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'


class CommentModel(BaseModel):
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    text = models.TextField()
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.blog.title}"

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'



