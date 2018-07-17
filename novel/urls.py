from django.conf.urls import url
from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

from novel.views import BookshelfView, MorenovelView, CommentView, ChapterlistView, ContentView,\
    ChaptersortView

app_name = 'novel'
urlpatterns = [
    
    # ex: /novel/
    path(r'', views.index, name='index'),path('fix', views.fix, name='f'),
    path('bookshelf/', BookshelfView.as_view(), name='bookshelf'),
    path('comment/<int:book_id>/<int:chapter_id>/', CommentView.as_view(), name='comment'),
    # ex: /novel/69999
    path('<int:novel_id>/', ChapterlistView.as_view(), name='chapterlist'),
    # ex: /novel/69999/1
    path('<int:novel_id>/<int:num_id>/', ContentView.as_view(), name='content'),
    path('morenovel/', MorenovelView.as_view(), name='morenovel'),
    path('chapsort/', ChaptersortView.as_view(), name='chapsort'),

]