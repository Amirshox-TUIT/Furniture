from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from .models import *


@register(AuthorsModel)
class NewsTranslationOptions(TranslationOptions):
    fields = ('profession', 'bio',)


@register(CategoriesModel)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(TagsModel)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(BlogsModel)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


