from django.contrib import admin

# Register your models here.
from .models import Chaptername, Name, Websetting


@admin.register(Name)
class NameAdmin(admin.ModelAdmin):
    list_display = ('id', 'xs_name', 'xs_author', 'category', 'name_id', 'allrank', 'weekrank', 'monthrank')
    #list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    #设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'xs_name')
    
    #ordering设置默认排序字段，负号表示降序排序
    ordering = ('id',)
  
    #list_editable 设置默认可编辑字段
    #list_editable = ['machine_room_id', 'temperature']
  
    #fk_fields 设置显示外键字段
    #fk_fields = ('machine_room_id',)

@admin.register(Chaptername)
class ChapternameAdmin(admin.ModelAdmin):
    list_display = ('id', 'xs_chaptername', 'id_name', 'num_id', 'url')
    list_display_links = ('id', 'xs_chaptername')

@admin.register(Websetting)
class WebsettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'key', 'value', 'url', 'time')
    #list_display_links = ('id')
    list_editable = ['name', 'value', 'url']

class MyAdminSite(admin.AdminSite):
    site_header = '棋书中文网管理系统'  # 此处设置页面显示标题
    site_title = '棋书中文网'  # 此处设置页面头部标题
 
admin_site = MyAdminSite(name='management')