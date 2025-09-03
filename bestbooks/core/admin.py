from django.contrib import admin

# Register your models here.

from .models import User, Book, Trade, BooksInTrade, Message, Report, Rating

admin.site.register(User)
admin.site.register(Book)
admin.site.register(Trade)
admin.site.register(BooksInTrade)
admin.site.register(Message)
admin.site.register(Report)
admin.site.register(Rating)