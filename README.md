# qishu

# install
# 1.fulltext search: pip install whoosh django-haystack jieba
# 2.captcha: pip install django-simple-captcha
#


# problem
# 1.python manage.py migrate: table already exit
    -> python manage.py migrate appname --fake, continue the first step
# 2.in the render function of views: NoReverseMatch(match another template)
    -> 1,clear cache 2,check the .html file exit direct use undefined value {{}} eg:{{a.name}}
