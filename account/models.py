from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from novel.utils.storage import ImageStorage
from novel.models import Name

class Account(models.Model):
    SEX_CHOICES = { 1: '男士', 2: '女士',}
    ACTIVE_CHOICES = { 0: '注销', 1: '正常',}

    name     = models.CharField(max_length=128, verbose_name="用户名称* （带*为必填项）")
    password = models.CharField(max_length=128, verbose_name="密码*")
    sex      = models.SmallIntegerField(default=1, choices=SEX_CHOICES.items(),verbose_name="性别")
    birth    = models.DateField(blank=True, null=True,verbose_name="出生日期")
    phone    = models.CharField(max_length=128, unique=True, verbose_name="手机号*") # unique one
    email    = models.EmailField(unique=True, verbose_name="邮箱")
    picture                = models.ImageField(upload_to="Imag/%Y/%m/%d", default = 'Imag/default_img.jpg', storage=ImageStorage(), blank=True,null=True,verbose_name="头像")
    openid                 = models.CharField(max_length=128, blank=True, null=True,verbose_name="openID")
    personalized_signature = models.CharField(max_length=128, blank=True, null=True,verbose_name="个性签名")
    data_joined            = models.DateField(auto_now_add=True, verbose_name="加入日期")
    last_login             = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name="最近登录日期")
    is_active              = models.SmallIntegerField(default=0, choices=ACTIVE_CHOICES.items(),verbose_name="账号状态")

    def __unicode__(self):
        return self.phone
    class Meta:
        verbose_name='用户'
        verbose_name_plural=verbose_name

class Bookshelf(models.Model):
    book = models.ForeignKey(Name, on_delete=models.CASCADE, to_field='id', verbose_name="书编号")
    user = models.ForeignKey(Account, on_delete=models.CASCADE, to_field='id', verbose_name="用户编号")
    chapter = models.IntegerField(blank=True, default=1, verbose_name="章节编号")
    bookname = models.CharField(max_length=128, blank=True, null=True, verbose_name="书名")
    username = models.CharField(max_length=128, blank=True, null=True, verbose_name="用户名")
    chaptername = models.CharField(max_length=128, blank=True, null=True, verbose_name="章节名")
    time        = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name="记录时间")
    class Meta:
        verbose_name='书架'
        verbose_name_plural=verbose_name

class Comment(models.Model):
    book = models.ForeignKey(Name, on_delete=models.CASCADE, to_field='id', verbose_name="书编号")
    user = models.ForeignKey(Account, on_delete=models.CASCADE, to_field='id', verbose_name="用户编号")
    chapter = models.IntegerField(blank=True, default=1, verbose_name="章节编号")
    bookname = models.CharField(max_length=128, blank=True, null=True, verbose_name="书名")
    username = models.CharField(max_length=128, blank=True, null=True, verbose_name="用户名")
    chaptername = models.CharField(max_length=128, blank=True, null=True, verbose_name="章节名")
    time        = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name="记录时间")
    content     = models.TextField(blank=True, null=True, verbose_name="评论内容")
    starnum     = models.IntegerField(default=0, verbose_name="点赞")
    reply       = models.IntegerField(default=0, verbose_name="回复数")
    prtid       = models.IntegerField(default=0, verbose_name="回复ID")#0用作一层评论，1保留保留作为帖子用
    class Meta:
        verbose_name='评论'
        verbose_name_plural=verbose_name

class Star(models.Model):
    comment   = models.ForeignKey(Comment, on_delete=models.CASCADE, to_field='id', verbose_name="评论编号")
    user      = models.ForeignKey(Account, on_delete=models.CASCADE, to_field='id', verbose_name="用户编号")
    time      = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name="记录时间")

class EmailVerifyRecord(models.Model):
    """邮箱激活码"""
    code=models.CharField(max_length=20,verbose_name='验证码')
    email=models.EmailField(max_length=50,verbose_name='邮箱')
    send_type=models.CharField(verbose_name='验证码类型',choices=(('register','注册'),('forget','忘记密码')),
                max_length=20)
    send_time=models.DateTimeField(verbose_name='发送时间', auto_now_add=True,)
    class Meta:
        verbose_name='邮箱验证码'
        verbose_name_plural=verbose_name
    def __str__(self):
        return '{0}({1})'.format(self.code,self.email)


#class Profile(models.Model):
#    SEX_CHOICES = { 1: '男士', 2: '女士',}
#
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    sex  = models.SmallIntegerField(default=1, choices=SEX_CHOICES.items(),verbose_name="性别")
#    birth= models.DateField(blank=True, null=True,verbose_name="出生日期")
#    phone= models.CharField(max_length=128, blank=True, null=True,verbose_name="手机号")
#    picture = models.ImageField(upload_to="Image/", blank=True,null=True,verbose_name="头像")
#    openid = models.CharField(max_length=128, blank=True, null=True,verbose_name="openID")
#    personalized_signature = models.CharField(max_length=128, blank=True, null=True,verbose_name="个性签名")
#
#    def __unicode__(self):
#        return self.user.username
     

# 基本上无论什么时候保存事件（Save事件）发生，create_user_profile和save_user_profile方法都会被信号连接到用户模型。
# Profile模块也会被自动创建和更新,这种信号被称为post_save
#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Profile.objects.create(user=instance)
 
#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.profile.save()