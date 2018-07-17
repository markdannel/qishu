from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views

from account.views import ForgetPwdView,ResetView,ModifyView, LoginView,RegisterView
from account.views import ActiveUserView

from . import views

app_name = 'account'
urlpatterns = [
    path('change-password/', auth_views.PasswordChangeView.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    # ex: /account/myself
    path('myself/', views.myself, name='myself'),
    #忘记密码
    path('forget/',ForgetPwdView.as_view(),name='forget_pwd'),
    #重置密码
    path('reset/<str:active_code>',ResetView.as_view(),name='reset'),
    path('modify/',ModifyView.as_view(),name='modify'),
    path('active/<str:active_code>',ActiveUserView.as_view(),name='active'),
]