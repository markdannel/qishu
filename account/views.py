from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from novel.utils.email_send import send_register_email
from django.views import View
from account.models import EmailVerifyRecord

from .models import Account
from .forms import AccountForm, LoginForm, AccountModifyForm, ForgetForm, ResetForm, LoginwithcaptchaForm


class RegisterView(View):
    """注册"""

    def get(self, request):
        user_form = AccountForm()
        return render(request, 'account/register.html', {'user_form': user_form})

    def post(self,request):
        # form对象先不保存，等到图片保存后返回字符串或是默认图片
        user_form = AccountForm(request.POST or None, request.FILES or None)
        if user_form.is_valid():

            newproject = user_form.save(commit=False)
            # 加密
            newproject.password = make_password(newproject.password, None, 'pbkdf2_sha256')
            newproject.save()
            print(newproject.picture)
            send_register_email(newproject.email, 'register')
            return render(request, 'account/active_register.html')
        else:
            #messages.error(request, ('register fail'))
            pass
        return render(request, 'account/register.html', {'user_form': user_form})
# def register(request):
#     '''注册'''
#     # 只有当请求为 POST 时，才表示用户提交了注册信息
#     if request.method == 'POST':
#         # form对象先不保存，等到图片保存后返回字符串或是默认图片
#         user_form = AccountForm(request.POST or None, request.FILES or None)
#         if user_form.is_valid():
#
#             newproject = user_form.save(commit=False)
#             # 加密
#             newproject.password = make_password(newproject.password, None, 'pbkdf2_sha256')
#             #newproject.picture = u'Imag/default_img.jpg'
#             #print(newproject)
#             #if request.FILES:
#             #    newproject.picture = str(request.FILES['picture'])
#             newproject.save()
#             print(newproject.picture)
#             messages.success(request, ('register success'))
#             request.session['username'] = newproject.name
#             request.session['userid'] = newproject.id
#             request.session['userpic'] = str(newproject.picture)
#             request.session['usersex'] = newproject.sex
#             return redirect("/novel")
#         else:
#             messages.error(request, ('register fail'))
#     else:
#         # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
#         user_form = AccountForm()
#
#     return render(request, 'account/register.html', {'user_form': user_form})


class LoginView(View):
    """激活账户"""

    def get(self, request):
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        loginerrornum = request.session.get('loginerrornum', 0)
        print('loginerrornum', loginerrornum)
        form = LoginForm(request.POST)
        if loginerrornum > 1:
            form = LoginwithcaptchaForm(request.POST)

        try:
            phon = request.POST['phone']
            if phon.find('@')<0 and len(phon) > 11:
                messages.error(request, '手机号不能长于11位')
                return render(request, 'account/login.html', {'form': form})
            account = Account.objects.get(Q(phone=phon)|Q(email=phon))
            ps_bool = check_password(request.POST['password'], account.password)
            if ps_bool:
                if account.is_active == 1:
                    request.session['username'] = account.name
                    request.session['userid'] = account.id
                    request.session['userpic'] = str(account.picture)
                    request.session['usersex'] = account.sex
                    request.session['loginerrornum'] = 0
                    return redirect("/novel")
                else:
                    messages.error(request, '尚未激活，请先激活')
                    return render(request, 'account/login.html', {'form': form})
            loginerrornum += 1
            request.session['loginerrornum'] = loginerrornum
            messages.error(request, '账号或密码错误')
        except:
            loginerrornum += 1
            request.session['loginerrornum'] = loginerrornum
            messages.add_message(request, messages.WARNING, '账号或密码错误!')
        return render(request, 'account/login.html', {'form': form})
# @transaction.atomic
# def viewfunc(request):
#     create_parent()
#
#     try:
#         with transaction.atomic():
#             generate_relationships()
#     except IntegrityError:
#         handle_exception()

# def login(request):
#     '''登录'''
#     # 只有当请求为 POST 时，才表示用户提交了注册信息
#     if request.method == 'POST':
#         loginerrornum = request.session.get('loginerrornum', 0)
#         print('loginerrornum', loginerrornum)
#         form = LoginForm(request.POST)
#         if loginerrornum > 1:
#             form = LoginwithcaptchaForm(request.POST)
#
#         try:
#             phon = request.POST['phone']
#             account  = Account.objects.get(phone = phon)
#             ps_bool = check_password(request.POST['password'], account.password)
#             if ps_bool:
#                 request.session['username'] = account.name
#                 request.session['userid'] = account.id
#                 request.session['userpic'] = str(account.picture)
#                 request.session['usersex'] = account.sex
#                 request.session['loginerrornum'] = 0
#                 return redirect("/novel")
#             loginerrornum += 1
#             request.session['loginerrornum'] = loginerrornum
#             messages.error(request, '账号或密码错误')
#         except:
#             messages.add_message(request,messages.WARNING,'账号或密码错误!')
#
#     else:
#         # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
#         form = LoginForm()
#
#     return render(request, 'account/login.html', {'form': form})

def logout(request):
    '''登出'''
    try:
        del request.session['username']
        del request.session['userid']
    except KeyError:
        pass
    return redirect("/novel")

def index(request):
    '''主页'''
    return render(request, 'index.html')

def myself(request):
    '''个人设置'''
    if request.session.get('userid',None) == None:
        return redirect("/account/login")
    if request.method == 'POST':
        user_obj = Account.objects.get(pk = request.session.get('userid',None))
        userform = AccountModifyForm(request.POST, instance=user_obj)
        print(userform)
        if userform.is_valid():
            userform.save()
        return redirect("/novel")
    else:
        user = Account.objects.get(pk = request.session.get('userid',None))
        user_form = AccountModifyForm(instance=user)
        print(user.birth)
        context = {
            'user'  : user,
            'user_form' : user_form
        }
        return render(request, 'account/myself.html', context)


class ActiveUserView(View):
    """激活账户"""

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = Account.objects.get(email=email)
                user.is_active = 1
                user.save()

                return render(request, 'account/active_regsuccess.html')

class ForgetPwdView(View):
    '''忘记密码'''
    def get(self,request):
        forget_form=ForgetForm()
        return render(request,'account/forget.html',{'forget_form':forget_form})
    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email=request.POST.get('email','')
            send_register_email(email,'forget')
            return render(request,'account/success_send.html')
        else:
            return render(request,'account/forget.html',{'forget_form':forget_form})


class ResetView(View):
    '''重置密码'''
    def get(self,request,active_code):
        record=EmailVerifyRecord.objects.filter(code=active_code)
        print(record)
        if record:
            for i in record:
                email=i.email
                is_register=Account.objects.filter(email=email)
                if is_register:
                    return render(request,'account/pwd_reset.html',{'email':email})
        return redirect('index')
 
 
#因为<form>表单中的路径要是确定的，所以post函数另外定义一个类来完成
class ModifyView(View):
    """重置密码post部分"""
    def post(self,request):
        reset_form=ResetForm(request.POST)
        if reset_form.is_valid():
            pwd1=request.POST.get('newpwd1','')
            pwd2=request.POST.get('newpwd2','')
            email=request.POST.get('email','')
            print(email)
            if pwd1!=pwd2:
                return render(request,'account/pwd_reset.html',{'msg':'密码不一致！', 'email':email})
            else:
                user=Account.objects.get(email=email)
                user.password = make_password(pwd2, None, 'pbkdf2_sha256') # 加密
                print('modify user = ', user)
                user.save()
                return redirect('account:login')
        else:
            email=request.POST.get('email','')
            return render(request,'account/pwd_reset.html',{'msg':reset_form.errors, 'email':email})