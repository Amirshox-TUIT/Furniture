from django.contrib import admin
from apps.blogs.models import *

admin.site.register(CategoryModel)
admin.site.register(BlogModel)
admin.site.register(TagModel)
admin.site.register(CommentModel)