import xadmin

# Register your models here.
from .models import Chaptername, Name


class NameAdmin(object):
    list_display = ('id', 'xs_name', 'xs_author', 'category', 'name_id', 'allrank', 'weekrank', 'monthrank')
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'xs_name')

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('id',)
    search_fields = ('xs_name', 'xs_author')

    # list_editable 设置默认可编辑字段
    # list_editable = ['machine_room_id', 'temperature']

    # fk_fields 设置显示外键字段
    # fk_fields = ('machine_room_id',)


class ChapternameAdmin(object):
    list_display = ('id', 'xs_chaptername', 'id_name', 'num_id', 'url')
    list_display_links = ('id', 'xs_chaptername')
    search_fields = ('xs_chaptername', 'xs_content')


xadmin.site.register(Name, NameAdmin)
xadmin.site.register(Chaptername, ChapternameAdmin)
