from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from .models import *


@register(AboutModel)
class NewsTranslationOptions(TranslationOptions):
    fields = ('profession', 'bio',)
