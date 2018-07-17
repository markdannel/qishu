import xadmin
from xadmin import views
# Register your models here.
from .models import Account, Bookshelf, Comment

class AccountAdmin(object):
    list_display = ('id', 'name', 'email', 'phone', 'sex', 'birth', 'picture', 'is_active', 'data_joined', 'last_login')
    #设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'name')
    #列表页出现搜索框，参数是搜索的域
    search_fields = ('name', 'email', 'phone')
    
    #ordering设置默认排序字段，负号表示降序排序
    ordering = ('id',)
  
    #list_editable 设置默认可编辑字段
    list_editable = ['sex']
  
    #fk_fields 设置显示外键字段
    #fk_fields = ('machine_room_id',)

class BookshelfAdmin(object):
    list_display = ('id', 'bookname', 'book_id', 'chaptername', 'chapter', 'username', 'user_id', 'time')
    list_select_related = None

class CommentAdmin(object):
    list_display = ('id', 'prtid', 'username', 'user_id', 'reply', 'content', 'book_id', 'chapter', 'time')

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = "棋书中文网管理系统"
    site_footer = "棋书中文网"
    # menu_style = "accordion"

xadmin.site.register(Account, AccountAdmin)
xadmin.site.register(Bookshelf, BookshelfAdmin)
xadmin.site.register(Comment, CommentAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
