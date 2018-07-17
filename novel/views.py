#coding=utf-8
import json, hashlib
from django.core import serializers
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponse, Http404, JsonResponse
from django.db.models import F
from bulk_update.helper import bulk_update

from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger ,EmptyPage

from .models import Chaptername, Name, Websetting
from account.models import Bookshelf, Comment

from .novelSort import all_click, content_click, get_top_n_books

# Create your views here.
def index(request):
    """
    图书首页
    """
    novelList = Name.objects.all()[:10]
    allrank   = Name.objects.order_by('-allrank')[:10]
    monthrank = Name.objects.order_by('-monthrank')[:10]
    weekrank = Name.objects.order_by('-weekrank')[:10]
    nbookrank = Name.objects.order_by('-id')[:10]
    xuanhuan = Name.objects.filter(category = '玄幻魔法').order_by('-allrank', '-id')[:5]
    yanqing  = Name.objects.filter(category = '都市言情').order_by('-allrank', '-id')[:5]
    kehuan   = Name.objects.filter(category = '科幻小说').order_by('-allrank', '-id')[:5]
    kongbu   = Name.objects.filter(category = '恐怖灵异').order_by('-allrank', '-id')[:5]
    lishi    = Name.objects.filter(category = '历史军事').order_by('-allrank', '-id')[:5]
    zhentan  = Name.objects.filter(category = '侦探推理').order_by('-allrank', '-id')[:5]
    wangyou  = Name.objects.filter(category = '网游动漫').order_by('-allrank', '-id')[:5]
    qita     = Name.objects.filter(category = '其他类型').order_by('-allrank', '-id')[:5]
    ad1      = Websetting.objects.get(key = 'niad1')
    ad2      = Websetting.objects.get(key = 'niad2')
    lb1      = Websetting.objects.get(key = 'nilb1')
    lb2      = Websetting.objects.get(key = 'nilb2')
    lb3      = Websetting.objects.get(key = 'nilb3')
    lb4      = Websetting.objects.get(key = 'nilb4')
    # output = ', '.join([q.xs_name for q in novelList])
    # allclick, allsort = get_top_n_books(10)
    print("xuanhuan == ", nbookrank)
    context = {
        'novelList' : novelList,
        'allrank'  : allrank,
        'monthrank'  : monthrank,
        'weekrank'  : weekrank,
        'nbookrank'  : nbookrank,
        'xuanhuan' : xuanhuan,
        'yanqing' : yanqing,
        'kehuan' : kehuan,
        'kongbu' : kongbu,
        'lishi' : lishi,
        'zhentan' : zhentan,
        'wangyou' : wangyou,
        'qita' : qita,
        'ad1' : ad1, 'ad2' : ad2,
        'lb1' : lb1, 'lb2' : lb2,
        'lb3' : lb3, 'lb4' : lb4
    }

    return render(request, 'novel/index.html', context)


class ChapterlistView(View):
   '''图书章节'''
   def get(self,request, novel_id):
       #展示界面，取数据
       try:
           novel = Chaptername.objects.values('id', 'xs_chaptername', 'id_name', 'num_id').filter(
               id_name=novel_id).order_by('num_id')
           book  = Name.objects.get(name_id = novel_id)
           ad    = Websetting.objects.get(key = 'ncad')
           if request.session.get('userid',None):
               # bookshelf = Bookshelf.objects.select_related('book').get(book_id=book.id,
               #                                                             user_id=request.session.get('userid', None))
               bookshelf = Bookshelf.objects.get(book_id=book.id, user_id=request.session.get('userid', None))
           else:
               return render(request, 'novel/chapterlist.html', {'novel': novel, 'book': book, 'ad': ad})
       except Chaptername.DoesNotExist:
           raise Http404("Chaptername does not exist")
       except Bookshelf.DoesNotExist:
           return render(request, 'novel/chapterlist.html', {'novel': novel, 'book': book, 'ad': ad})
       return render(request, 'novel/chapterlist.html', {'novel': novel, 'book': book, 'ad': ad, 'bookshelf': bookshelf})
   def post(self,request,novel_id):
       # 加入书架 join bookshelf
       if request.is_ajax():
           userid = request.session.get('userid', None)
           if userid:
               print(request.POST)
               bookid = request.POST.get("bid")
               bookname = request.POST.get("bname")
               print(bookid, bookname)
               dic = {'book_id': request.POST.get("bid"), 'user_id': userid,
                      'bookname': request.POST.get("bname"), 'username': request.session.get('userid', None)}
               data = Bookshelf.objects.get_or_create(**dic)
               if data != None:
                   return JsonResponse({"status": "1"}, safe=False)
           return JsonResponse({"status": "0"}, safe=False)

class ContentView(View):
   '''章节内容'''
   def get(self,request, novel_id, num_id):
       try:
           bias = int(request.GET.get('bias', '0'))
           print(bias)
           if bias > 0:
               checkchap = Chaptername.objects.values('id', 'num_id').filter(id_name=novel_id).order_by('num_id')
               print(checkchap)
               for row in checkchap:
                   if row['num_id'] > num_id:
                       num_id = row['num_id']
                       break
           print("num_id = ", num_id)
           content = Chaptername.objects.get(id_name=novel_id, num_id=num_id)
           book = Name.objects.get(name_id=novel_id)
           if request.session.get('userid', None):
               bookshelf = Bookshelf.objects.filter(book_id=book.id
                                                    , user_id=request.session.get('userid', None)).update(
                   chapter=content.num_id, chaptername=content.xs_chaptername)
               Bookshelf.objects.update()
           # 点击进入章节内容，Redis记录一次点击数
           # content_click(book.id, book.category)
           # all_click(book.id)
           Name.objects.filter(pk=book.id).update(allrank=F("allrank") + 11, monthrank=F("monthrank") + 11,
                                                  weekrank=F("weekrank") + 11)
       except Chaptername.DoesNotExist:
           raise Http404("Chaptername does not exist")
       return render(request, 'novel/content.html', {'content': content, 'book': book})



class BookshelfView(View):
    """
    书架
    """
    def get(self,request):
        try:
            if request.session.get('userid',None) == None:
                return redirect("/account/login")
            page = int(request.GET.get('page', '1'))
            bookshelf = Bookshelf.objects.select_related('book').filter(user_id = request.session.get('userid',None))
            paginator = Paginator(bookshelf, 10)
            try:
                pags = paginator.page(int(page))
            except PageNotAnInteger:
                pags = paginator.page(1)
            except EmptyPage:
                pags = paginator.page(paginator.num_pages)
        except Bookshelf.DoesNotExist:
            raise Http404("Chaptername does not exist")
        return render(request, 'novel/bookshelf.html', {'bookshelf': pags})
    def post(self, request):
        print(request.POST, request.POST.get('bid'))
        if request.is_ajax():
            n, res = Bookshelf.objects.filter(pk = request.POST.get('bid')).delete()
            if n > 0:
                return JsonResponse({"status":"1"}, safe=False)
            return JsonResponse({"status":"0"}, safe=False)

class CommentView(View):
    '''书评'''
    def get(self,request, book_id, chapter_id):
        if request.session.get('userid',None) == None:
            return redirect("/account/login")
        if request.is_ajax():
            cid = request.GET.get("cid")
            print(request.GET, cid)
            if cid is not None:
                comment = Comment.objects.values('id', 'reply', 'chapter', 'username', 'time', 'content', 'book_id', 'user_id', 
                                                 'prtid', 'user__picture').filter(prtid = cid, book_id= book_id, 
                                                                                  chapter = chapter_id, user__id = F('user'))
                #print("soc2 = ", serializers.serialize('json', list(comment)))
                if comment != None:
                    #serialized_obj = serializers.serialize('json', comment)
                    commentlist = list(comment)
                    for item in commentlist:
                        item['time'] = item['time'].strftime("%Y-%m-%d")
                    data = json.dumps(commentlist)
                    return JsonResponse(data, safe=False)
            return JsonResponse({"status":"1"}, safe=False)
        try:
            page = int(request.GET.get('page', '1'))
            book = Name.objects.get(id = book_id)
            chapter = Chaptername.objects.get(id = chapter_id)
            comment = Comment.objects.select_related('user').filter(prtid = 0, book_id= book_id, chapter = chapter_id)
            paginator = Paginator(comment, 10)
            try:
                pags = paginator.page(int(page))
            except PageNotAnInteger:
                pags = paginator.page(1)
            except EmptyPage:
                pags = paginator.page(paginator.num_pages)
        except Comment.DoesNotExist:
            raise Http404("Comment does not exist")
        return render(request, 'novel/comment.html', {'book': book, 'chapter': chapter, 'comment': pags})

    def post(self, request, book_id, chapter_id):
        if request.session.get('userid',None) == None:
            return redirect("/account/login")
        # 插入评论
        if request.is_ajax():
            userid = request.session.get('userid',None)
            content = request.POST.get("content")
            prtid   = request.POST.get("prtid")
            if prtid is None:
                prtid = 0
            print(content)
            dic = {'book_id': book_id, 'user_id': userid, 'prtid': prtid,'content': content,
                'chapter': chapter_id, 'username': request.session.get('username',None)}
            data, _ = Comment.objects.get_or_create(**dic)
            if prtid != 0:
                cc = Comment.objects.get(pk = prtid)
                cc.reply = cc.reply + 1
                cc.save()
            if data != None:
                    return JsonResponse({"status":"1"}, safe=False)
            return JsonResponse({"status":"0"}, safe=False)
        pass


class MorenovelView(View):
    '''更多小说'''
    def get(self,request):
        try:
            page = int(request.GET.get('page', '1'))
            ctg = request.GET.get('ctg', '玄幻魔法')
        except ValueError:  
            page = 1
            ctg = '玄幻魔法'
        novel = Name.objects.filter(category = ctg).order_by('-allrank', '-id')
        paginator = Paginator(novel, 10)
        try:
            pags = paginator.page(int(page))
        except PageNotAnInteger:
            pags = paginator.page(1)
        except EmptyPage:
            pags = paginator.page(paginator.num_pages)
        context = {
            'novel' : pags,
            'ctg' : ctg,
        }
        return render(request, 'novel/morenovel.html', context)


class ChaptersortView(View):
    '''章节排序'''
    def get(self,request):
        num = int(request.GET.get('novel', 0))
        novel = Name.objects.filter().values('name_id')
        for nl in novel:
            num = int(nl['name_id'])
            if num > 0:
                chapters = Chaptername.objects.filter(id_name = num).order_by("num_id")
                prevnext = 0
                prevnumid = 0
                previd = 0
                for item in chapters:
                    if prevnumid != item.prev:
                        Chaptername.objects.filter(pk=item.id).update(prev=prevnumid)
                    prevnumid = item.num_id
                for item in chapters:
                    if prevnext != item.num_id and previd > 0:
                        Chaptername.objects.filter(pk=previd).update(next=item.num_id)
                    previd = item.id
                    prevnext = item.next

        return render(request, 'novel/index.html')


def fix(request):

    return render(request, 'novel/fix.html')







############# def -> class ###########


#def comment(request, book_id, chapter_id):
#    """
#    书评
#    """
#    # 查询子评论
#    if request.session.get('userid',None) == None:
#            return redirect("/account/login")
#    if request.is_ajax() and request.method == 'GET':
#        cid = request.GET.get("cid")
#        print(request.GET, cid)
#        if cid is not None:
#            comment = Comment.objects.values('id', 'reply', 'chapter', 'username', 'time', 'content', 'book_id', 'user_id', 
#                                             'prtid', 'user__picture').filter(prtid = cid, book_id= book_id, 
#                                                                              chapter = chapter_id, user__id = F('user'))
#            #print("soc2 = ", serializers.serialize('json', list(comment)))
#            if comment != None:
#                #serialized_obj = serializers.serialize('json', comment)
#                commentlist = list(comment)
#                for item in commentlist:
#                    item['time'] = item['time'].strftime("%Y-%m-%d")
#                data = json.dumps(commentlist)
#                return JsonResponse(data, safe=False)
#        return JsonResponse({"status":"1"}, safe=False)
#    # 插入评论
#    if request.is_ajax() and request.method == 'POST':
#        userid = request.session.get('userid',None)
#        content = request.POST.get("content")
#        prtid   = request.POST.get("prtid")
#        if prtid is None:
#            prtid = 0
#        print(content)
#        dic = {'book_id': book_id, 'user_id': userid, 'prtid': prtid,'content': content,
#            'chapter': chapter_id, 'username': request.session.get('username',None)}
#        data, _ = Comment.objects.get_or_create(**dic)
#        if prtid != 0:
#            cc = Comment.objects.get(pk = prtid)
#            cc.reply = cc.reply + 1
#            cc.save()
#        if data != None:
#                return JsonResponse({"status":"1"}, safe=False)
#        return JsonResponse({"status":"0"}, safe=False)
#    try:
#        book = Name.objects.get(id = book_id)
#        chapter = Chaptername.objects.get(id = chapter_id)
#        comment = Comment.objects.select_related('user').filter(prtid = 0, book_id= book_id, chapter = chapter_id)
#        print(serializers.serialize('json', comment))
#    except Bookshelf.DoesNotExist:
#        raise Http404("Chaptername does not exist")
#    return render(request, 'novel/comment.html', {'book': book, 'chapter': chapter, 'comment': comment})

# def chapterlist(request, novel_id):
#     """
#     图书章节
#     """
#     # 加入书架 join bookshelf
#     if request.is_ajax():
#         userid = request.session.get('userid',None)
#         if userid:
#             print(request.POST)
#             bookid = request.POST.get("bid")
#             bookname = request.POST.get("bname")
#             print(bookid, bookname)
#             dic = {'book_id': request.POST.get("bid"), 'user_id': userid,
#                 'bookname': request.POST.get("bname"), 'username': request.session.get('userid',None)}
#             data = Bookshelf.objects.get_or_create(**dic)
#             if data != None:
#                 return JsonResponse({"status":"1"}, safe=False)
#         return JsonResponse({"status":"0"}, safe=False)
#     # 展示界面，取数据
#     try:
#         novel = Chaptername.objects.values('id', 'xs_chaptername', 'id_name', 'num_id').filter(id_name = novel_id).order_by('num_id')
#         book  = Name.objects.get(name_id = novel_id)
#         ad    = Websetting.objects.get(key = 'ncad')
#         bookshelf = None
#         if request.session.get('userid',None):
#             bookshelf = Bookshelf.objects.select_related('book').get(book_id = book.id, user_id = request.session.get('userid',None))
#
#     except Chaptername.DoesNotExist:
#         raise Http404("Chaptername does not exist")
#     except Bookshelf.DoesNotExist:
#         template = loader.get_template('novel/chapterlist.html')
#         context = {'novel': novel, 'book': book, 'ad': ad, 'bookshelf': bookshelf}
#         return HttpResponse(template.render(context, request))
#         #return render(request, 'novel/chapterlist.html', {'novel': novel, 'book': book, 'ad': ad, 'bookshelf': bookshelf})
#     return render(request, 'novel/chapterlist.html', {'novel': novel, 'book': book, 'ad': ad, 'bookshelf': bookshelf})