from modeltranslation.translator import register, TranslationOptions
from .models import *

@register(Section)
class SectionTranslationOptions(TranslationOptions):
    fields = ('name', 'slug')


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('name', 'slug')


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name', 'slug')


@register(Book)
class BookTranslationOptions(TranslationOptions):
    fields = ('name', 'slug', 'description')
