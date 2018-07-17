from django.contrib import admin

# Register your models here.
from .models import Account, Bookshelf, Comment

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'sex', 'birth', 'picture', 'is_active', 'data_joined', 'last_login')

@admin.register(Bookshelf)
class BookshelfAdmin(admin.ModelAdmin):
    list_display = ('id', 'bookname', 'book_id', 'chaptername', 'chapter', 'username', 'user_id', 'time')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'prtid', 'username', 'user_id', 'reply', 'content', 'book_id', 'chapter', 'time')