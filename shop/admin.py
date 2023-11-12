from django.contrib import admin
from .models import Section, Genre, Book, Author
from modeltranslation.admin import TranslationAdmin

class AuthorAdmin(TranslationAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Author, AuthorAdmin)

class SectionAdmin(TranslationAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Section, SectionAdmin)

class GenreAdmin(TranslationAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Genre, GenreAdmin)


class BookAdmin(TranslationAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    filter_horizontal = ['authors', 'genre']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Book, BookAdmin)