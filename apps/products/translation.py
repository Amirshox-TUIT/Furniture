from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from .models import *


@register(ProductCategory)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(ProductTag)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(ProductColor)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(ProductModel)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'long_description')

