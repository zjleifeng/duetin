#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: views.py
@time: 2017/10/12 下午1:11
@SOFTWARE:PyCharm
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, PasswordRestForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib import auth
from django.views.generic import ListView
from .page_paginator import DuetinPaginator
from app_auth.permissions import check_permission
import logging
from khufu import settings
from django.core.paginator import EmptyPage, PageNotAnInteger
from app_auth.models import User
from dao.models.music import MusicProfiel, Singer, AllSongMusic,PartSongMusic,AllMusicCategory
from django.db.models import Q
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from khafre.main.serilizers import MusicProfileSingerSerializer, MusicHtmlSerializer, SingerSerializer, \
    AllSongMusic_htm_Serializer,PartSongMusic_htm_Serializer,CategorySerializer,All_Songmusic_Manual_htm_Serializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from khafre.utils.pags import api_paging, js_resp_paging, js_resp_sing_paging, js_resp_htpg
from app_auth.serializers import UserHtmSer
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.utils.timezone import now, timedelta
from khafre.message.serializers import MobileVersionSer,Create_SongExceptionSerializer
from dao.models.base import OperationLogs,SongException
from app_auth.models import MobileVersion
from khafre.main.serilizers import PostData_htm_Serializer
import time
import copy
from khafre.utils.operatelog import operationlogs
from khafre.utils.json_response import json_resp
from rest_framework import permissions
from rest_framework.compat import is_authenticated
from khufu.settings import operate_s3
from khafre.utils.praiseship import Praiseship
p=Praiseship()
def pem_check(user):
    if user.has_perm('app_auth.view_operate_list'):
        return True
    else:
        return False



class Check_is_operate(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """

    def has_permission(self, request, view):
        return request.user and is_authenticated(request.user) and request.user.has_perm('app_auth.view_operate_list')

def get_pageinatior(func):
    def page_pageinatior(*args, **kwargs):

        reg = func(*args, **kwargs)
        paginate_by = settings.PAGE_NUM
        paginator = DuetinPaginator(reg[1], paginate_by)
        page = reg[0].request.GET.get('page')

        try:
            reg = paginator.page(page)
        except PageNotAnInteger:
            reg = paginator.page(1)
            page = 1
        except EmptyPage:
            reg = paginator.page(paginator.num_pages)
        return reg

    return page_pageinatior


class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            if self.request.META.has_key('HTTP_X_FORWARDED_FOR'):
                ip = self.request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = self.request.META['REMOTE_ADDR']
            context['ip_adress'] = ip

        except Exception as e:
            logging.error(u'[BaseMixin]加载基本信息出错！')

        return context

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(BaseMixin, cls).as_view(**initkwargs)
        return login_required(view)


@login_required
def operate(request):
    if pem_check(request.user):
        username = request.user.username
        return render_to_response('operate/index.html', {"username": username}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/operate/login/')

# @check_permission
def userlogin(request):
    error = []
    if request.method == 'GET':
        form = LoginForm()
        return render_to_response('operate/sign-in.html', RequestContext(request, {'form': form, }))
    else:

        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            # if user：
            #     if user.has_perm('app_auth.view_operate_list'):
            #         pass
            #     else:

            if user and user.is_active:
                if user.has_perm('app_auth.view_operate_list'):

                    auth.login(request, user)
                    return render_to_response('operate/index.html', RequestContext(request))
                else:
                    return render_to_response('operate/sign-in.html',
                                              RequestContext(request, {'form': form, 'error': "No permission login"}))
            else:

                return render_to_response('operate/sign-in.html',
                                          RequestContext(request, {'form': form, 'error': "password is wrong!"}))
        else:

            return render_to_response('operate/sign-in.html',
                                      RequestContext(request, {'form': form, 'error': "username or password is wrong"}))


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/operate/login/")


def forgetpassword(request):
    if request.method == 'GET':
        form = PasswordRestForm()
        return render_to_response('operate/forgot_password.html', RequestContext(request, {'form': form, }))
    else:
        form = PasswordRestForm(request.POST)

        if form.is_valid():
            token_generator = default_token_generator
            from_email = None
            opts = {
                'token_generator': token_generator,
                'from_email': from_email,
                'request': request,
            }
            user = form.save(**opts)
            return render_to_response('operate/user_login.html', RequestContext(request, {'success': True}))
        else:
            return render_to_response('operate/forgot_password.html', RequestContext(request, {'form': form, }))


class UsersView(BaseMixin, ListView):
    template_name = 'operate/userrecord.html'
    context_object_name = 'obj_list'

    def get_context_data(self, *args, **kwargs):

        return super(UsersView, self).get_context_data(*args, **kwargs)

    @get_pageinatior
    def get_queryset(self):
        user = self.request.user
        if pem_check(user):

            obj_list = User.objects.all().order_by('-created_at')
            count = obj_list.count()
            return self, obj_list, count
        else:
            obj_list = []
            count = 0
            return self, obj_list, count


class UserSearchView(BaseMixin, ListView):
    template_name = 'operate/userrecord.html'
    context_object_name = 'obj_list'

    def get_context_data(self, **kwargs):
        kwargs['S'] = self.request.GET.get('S', '')
        kwargs['WS'] = self.request.GET.get('WS', '')
        kwargs['WB']=self.request.GET.get('WB','')
        kwargs['WT']=self.request.GET.get('WT','')

        return super(UserSearchView, self).get_context_data(**kwargs)

    @get_pageinatior
    def get_queryset(self):

        user = self.request.user
        if pem_check(user):
            S = self.request.GET.get('S', '')
            WS = self.request.GET.get('WS', '')
            WB= self.request.GET.get('WB', '')
            WT = self.request.GET.get('WT', '')
            if S and WS:

                obj_list = User.objects.filter(Q(username__icontains=S) & Q(is_important=WS))
            elif S:
                obj_list = User.objects.filter(Q(username__icontains=S))
            elif WS:
                obj_list = User.objects.filter(Q(is_important=WS))
            elif WB:
                if WB=="1":
                    obj_list=User.objects.filter(Q(is_recommend=1)).order_by('-new_user_rank')
                else:
                    obj_list = User.objects.filter(Q(is_recommend=0))
            elif WT:
                if WT=="1":
                    obj_list=User.objects.filter(Q(add_user_rank__gt=0)).order_by('-add_user_rank')
                else:
                    obj_list=User.objects.filter(Q(add_user_rank=0))

            else:
                obj_list = User.objects.all().order_by('-created_at')[:100]

            return self, obj_list, S
        else:
            obj_list = []
            count = 0
            return self, obj_list, count

class edituser(BaseMixin, ListView):
    template_name = 'operate/userrecord.html'
    context_object_name = 'obj_list'

    def post(self, request, *args, **kwargs):
        if pem_check(request.user):

            en_id = self.kwargs.get('pk', '')
            is_important = int(request.POST.get('v', ''))
            is_act = int(request.POST.get('a', ''))
            # user_rank=int(request.POST.get('sort'))
            is_recommend = int(request.POST.get('r', ''))
            add_user_rank = int(request.POST.get('addusersort', ''))
            new_user_rank = int(request.POST.get('newusersort', ''))

            birth = request.POST.get('birth', '')
            new_birth = ""
            if birth:
                try:
                    timeArray = time.strptime(birth, "%Y/%m/%d")
                    new_birth = int(time.mktime(timeArray))

                except:
                    return json_resp(code=400, msg="修改生日出错")

            sex = int(request.POST.get('sex'))

            obj = User.objects.get(id=en_id)
            obj_old = copy.deepcopy(obj)
            try:

                obj.is_important = is_important
                obj.is_active = is_act
                obj.add_user_rank = add_user_rank
                obj.new_user_rank = new_user_rank
                obj.is_recommend = is_recommend
                obj.sex = sex
                if birth:
                    obj.birth = birth
                    obj.new_birth = new_birth

                obj.save()

                if obj_old is not None:
                    update_fields = {"is_important": is_important, "is_active": is_act, 'add_user_rank': add_user_rank,
                                     "new_user_rank": new_user_rank, "is_recommend": is_recommend,"birth":birth,"new_birth":new_birth}
                    operationlogs(self.request, obj_old, update_fields, "change")
            except User.DoesNotExist:
                logging.error(u'删除用户[EmployeeUser]ID[%s]不存在！' % en_id)
                return HttpResponse("error")
            if is_important:
                v = "V"
            else:
                v = ''
            if is_act:
                a = 'YES'
            else:
                a = 'NO'
            s = add_user_rank
            n = new_user_rank
            if is_recommend:
                r = "已推荐"
            else:
                r = ''
            if sex==0:
                r_sex='男'
            elif sex==1:
                r_sex='女'
            else:
                r_sex=""


            return json_resp(code=200, msg="ok", data={"a": a, "v": v, "s": s, 'r': r, 'n': n,"r_sex":r_sex,"r_birth":birth})
        else:
            return HttpResponseRedirect('/operate/login/')


class Music_View(APIView):
    """
    A view that returns a templated HTML representation of a given user.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/musicrecord.html'

    def get(self, request):
        music = MusicProfiel.objects.all().order_by('-rank')
        singer_obj = Singer.objects.all()
        singer_ser = SingerSerializer(singer_obj, many=True)
        return js_resp_htpg(music, request, MusicHtmlSerializer, obj_singer=singer_ser.data,pagenum=20)


class MusicSearch_View(APIView):
    """
    A view that returns a templated HTML representation of a given user.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/musicrecord.html'

    def get(self, request):
        S = self.request.GET.get('S')  # 输入框UID,music_name
        WS = self.request.GET.get('WS')  # 歌手iD
        WB = self.request.GET.get('WB')  # 是否男女对唱
        WT = self.request.GET.get('WT')  # 歌曲类型

        if 'S' in self.request.GET and self.request.GET['S']:
            S = self.request.GET['S']
            sSq = (Q(music_name__icontains=S) | Q(uid=S))
        else:
            sSq = Q()
        if 'WS' in self.request.GET and self.request.GET['WS']:
            WS = self.request.GET['WS']
            wSq = Q(singer__id=WS)
        else:
            wSq = Q()
        if 'WB' in self.request.GET and self.request.GET['WB']:
            WB = self.request.GET['WB']
            wBq = Q(is_loved=WB)
        else:
            wBq = Q()
        if 'WT' in self.request.GET and self.request.GET['WT']:
            WT = self.request.GET['WT']
            wTq = Q(style=WT)
        else:
            wTq = Q()
        # sSq = (Q(music_name__icontains=S) | Q(uid=S))
        # wSq = Q(singer__id=WS)
        # wBq = Q(is_loved=WB)
        # wTq = Q(style=WT)
        sql = sSq & wSq & wBq & wTq
        # if S and WS and WB:
        #     sql = sSq & wSq & wBq
        #
        # elif S and WB:
        #     sql = sSq & wBq
        # elif S and WS:
        #     sql = sSq & wSq
        #
        # elif WB and WS:
        #     sql = wBq & wSq
        #
        # elif S:
        #     sql = sSq
        # elif WS:
        #     sql = wSq
        # elif WB:
        #     sql = wBq
        # else:
        #     sql = (Q())
        search_word={"S":S,"WS":WS,"WB":WB,"WT":WT}

        music = MusicProfiel.objects.filter(sql).order_by('-rank')
        # music = MusicProfiel.objects.all()[:60]
        singer_obj = Singer.objects.all()
        singer_ser = SingerSerializer(singer_obj, many=True)
        return js_resp_htpg(music, request, MusicHtmlSerializer, obj_singer=singer_ser.data,search_word=search_word)


class Edit_music(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (Check_is_operate,)

    def post(self, request, pk):

        music = MusicProfiel.objects.get(id=pk)
        obj_old = copy.deepcopy(music)
        serializer = MusicHtmlSerializer(music, data=request.data)
        if serializer.is_valid():
            serializer.save()

            if music is not None:
                datas = self.request.data
                update_fields = {"sort": datas["sort"], "new_sort": datas["new_sort"],
                                 "is_loved": datas["is_loved"], "style": datas["style"],
                                 "is_online": datas["is_online"], "view_count": datas["view_count"]}

                operationlogs(self.request, obj_old, update_fields, "change")
            sort = self.request.data["sort"]
            newsort = self.request.data["new_sort"]
            musicstyle = self.request.data["style"]
            if musicstyle == "0":
                labmusicstyle = "MELODY"
            elif musicstyle == "1":
                labmusicstyle = "RAP"
            elif musicstyle == "2":
                labmusicstyle = "Rap&Melody"
            else:
                labmusicstyle = "Undefined"
            isloved = self.request.data["is_loved"]
            if isloved == "0":
                labisloved = " "
            else:
                labisloved = "YES"
            isonline = self.request.data["is_online"]
            if isonline == "0":
                labisonline = "否"
            else:
                labisonline = "是"

            v_count = self.request.data['view_count']

            return json_resp(code=200, msg='ok', data={"sort": sort, "newsort": newsort, "labmusicstyle": labmusicstyle,
                                                       "labisloved": labisloved, "labisonline": labisonline,
                                                       "v_count": v_count})
        else:
            return HttpResponse(serializer.errors)


class MusicOperate_View(APIView):
    """
    被唱过的歌曲列表
    A view that returns a templated HTML representation of a given user.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/musicoperate.html'

    def get(self, request):
        music = MusicProfiel.objects.filter(Q(music_part__part__in=[0, 1]), is_online=True).order_by('-view_count','-rank')

        # singer_obj = Singer.objects.all()
        # singer_ser = SingerSerializer(singer_obj, many=True)
        return js_resp_htpg(music, request, MusicHtmlSerializer,  pagenum=20)


class MusicOperate_no_View(APIView):
    """没有被唱过的歌曲"""
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/music_no_operate.html'

    def get(self, request):
        # music = MusicProfiel.objects.filter(is_online=True).order_by('-rank')

        music = MusicProfiel.objects.filter(Q(music_part__part=None), is_online=True).order_by('-view_count','-rank')

        # singer_obj = Singer.objects.all()
        # singer_ser = SingerSerializer(singer_obj, many=True)
        return js_resp_htpg(music, request, MusicHtmlSerializer, pagenum=20)


        # return HttpResponse("error slug")


class MusicOperateSearch_View(APIView):

    """
    被唱过的歌曲搜索
    A view that returns a templated HTML representation of a given user.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/musicoperate.html'

    def get(self, request):
        S = self.request.GET.get('S')  # 输入框UID,music_name
        WS = "" # 歌手iD
        WB = ""  # 是否男女对唱
        WT = ""  # 歌曲类型

        if 'S' in self.request.GET and self.request.GET['S']:
            S = self.request.GET['S']
            # sSq = (Q(music_part__part__in=[0, 1]),Q(music_name__icontains=S) | Q(uid=S))
            music = MusicProfiel.objects.filter(Q(music_part__part__in=[0, 1]),Q(music_name__icontains=S) | Q(uid=S),is_online=True).order_by('-rank')
        # sql = sSq
        else:
            music = MusicProfiel.objects.filter(Q(music_part__part__in=[0, 1]), is_online=True)

        search_word = {"S": S, "WS": WS, "WB": WB, "WT": WT}

        # music = MusicProfiel.objects.filter(sql).order_by('-rank')
        # music = MusicProfiel.objects.all()[:60]
        # singer_obj = Singer.objects.all()
        # singer_ser = SingerSerializer(singer_obj, many=True)
        return js_resp_htpg(music, request, MusicHtmlSerializer,  search_word=search_word,pagenum=20)


class MusicOperateNoSearch_View(APIView):

    """
    没有被唱过的歌曲搜索
    A view that returns a templated HTML representation of a given user.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/music_no_operate.html'

    def get(self, request):
        S = self.request.GET.get('S')  # 输入框UID,music_name
        WS = "" # 歌手iD
        WB = ""  # 是否男女对唱
        WT = ""  # 歌曲类型

        if 'S' in self.request.GET and self.request.GET['S']:
            S = self.request.GET['S']
            # sSq = (Q(music_part__part__in=[0, 1]),Q(music_name__icontains=S) | Q(uid=S))
            music = MusicProfiel.objects.filter(Q(music_part__part=None),Q(music_name__icontains=S) | Q(uid=S),is_online=True).order_by('-rank')
        # sql = sSq
        else:
            music = MusicProfiel.objects.filter(Q(music_part__part=None), is_online=True).order_by('-rank')

        search_word = {"S": S, "WS": WS, "WB": WB, "WT": WT}

        # music = MusicProfiel.objects.filter(sql).order_by('-rank')
        # music = MusicProfiel.objects.all()[:60]
        # singer_obj = Singer.objects.all()
        # singer_ser = SingerSerializer(singer_obj, many=True)
        return js_resp_htpg(music, request, MusicHtmlSerializer,  search_word=search_word,pagenum=20)


class Edit_MusicNoOperate(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (Check_is_operate,)

    def post(self, request, pk):

        music = MusicProfiel.objects.get(id=pk)
        obj_old = copy.deepcopy(music)
        serializer = MusicHtmlSerializer(music, data=request.data)
        if serializer.is_valid():
            serializer.save()

            if music is not None:
                datas = self.request.data
                update_fields = {"sort": datas["sort"], "new_sort": datas["new_sort"],
                                 "is_loved": datas["is_loved"], "style": datas["style"],
                                 "is_online": datas["is_online"]}

                operationlogs(self.request, obj_old, update_fields, "change")

            return json_resp(code=200,msg='ok')
        else:

            return HttpResponse(serializer.errors)



class Post_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/postrecord.html'

    def get(self, request):
        song_post = AllSongMusic.objects.all().order_by('-rank')
        singer_obj = User.objects.all()
        singer_ser = UserHtmSer(singer_obj, many=True)
        return js_resp_htpg(song_post, request, AllSongMusic_htm_Serializer, obj_singer=singer_ser.data,title="作品管理")


class DayPost_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/postrecord.html'

    def get_last_day(self):
        start = now().date()
        end = start - timedelta(days=1)

        return AllSongMusic.objects.filter(created_at__range=(end, start)).order_by('-rank')

    def get(self, request):
        song_post = self.get_last_day()
        song_count = song_post.count()
        singer_obj = User.objects.all()
        singer_ser = UserHtmSer(singer_obj, many=True)
        return js_resp_htpg(song_post, request, AllSongMusic_htm_Serializer, obj_singer=singer_ser.data,title="一天内作品")


class AllPost_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/postrecord.html'

    def get(self, request):
        song_post = AllSongMusic.objects.filter(bucket_all_vedio_name="duetin-chorus").order_by('-rank','-created_at')
        song_count = song_post.count()
        singer_obj = User.objects.all()
        singer_ser = UserHtmSer(singer_obj, many=True)
        return js_resp_htpg(song_post, request, AllSongMusic_htm_Serializer, obj_singer=singer_ser.data,title='合唱作品')


class PostSearch_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/postrecord.html'

    def get(self, request):
        S = self.request.GET.get('S')  # 输入框,music_name
        WS = self.request.GET.get('WS')  # 发布者
        WB = self.request.GET.get('WB')  # 星级
        title = self.request.GET.get('title')

        if 'S' in self.request.GET and self.request.GET['S']:
            S = self.request.GET['S']
        else:
            S=""
        if 'WS' in self.request.GET and self.request.GET['WS']:
            WS = self.request.GET['WS']
        else:
            WS=""
        if 'WB' in self.request.GET and self.request.GET['WB']:
            WB = self.request.GET['WB']
        else:
            WB=""
        sSq = (Q(music_info__music_name__icontains=S) | Q(all_music_auth__username__icontains=S))
        wSq = Q(all_music_auth_id=WS)
        wBq = Q(rating_scale=WB)

        if S and WS and WB:
            sql = sSq & wSq & wBq

        elif S and WB:
            sql = sSq & wBq
        elif S and WS:
            sql = sSq & wSq

        elif WB and WS:
            sql = wBq & wSq

        elif S:
            sql = sSq
        elif WS:
            sql = wSq
        elif WB:
            sql = wBq
        else:
            sql = (Q())
        WT = ""
        search_word = {"S": S, "WS": WS, "WB": WB, "WT": WT}

        # music1=AllSongMusic.objects.filter()[:100]
        music = AllSongMusic.objects.filter(sql)
        # music = MusicProfiel.objects.all()[:60]
        singer_obj = User.objects.all()
        singer_ser = UserHtmSer(singer_obj, many=True)
        return js_resp_htpg(music, request, AllSongMusic_htm_Serializer, obj_singer=singer_ser.data,title=title,search_word=search_word)


class Edit_Post(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)

    def post(self, request, pk):
        try:

            music = AllSongMusic.objects.get(id=pk)
            obj_old = copy.deepcopy(music)

            serializer = AllSongMusic_htm_Serializer(music, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                if music is not None:
                    datas = self.request.data
                    update_fields = {"rank": datas["rank"], "view_count_rank": datas["view_count_rank"],
                                     "is_enable": datas["is_enable"],'praise':datas['praise']}

                    operationlogs(self.request, obj_old, update_fields, "change")

                rank=self.request.data['rank']
                view_count_rank=self.request.data['view_count_rank']
                isenable=self.request.data['is_enable']


                if isenable=='1':
                    enable="是"
                else:
                    enable="否"
                praise_op=self.request.data['praise']
                redis_count = p(pk).lovedby_count()
                count = redis_count + int(praise_op)

                return json_resp(code=200,msg="ok",data={"rank":rank,"view_count_rank":view_count_rank,"isenable":enable,"praise":count})
            else:
                return HttpResponse("error")
        except:
            return HttpResponse("error")


class Del_Post(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)

    def post(self, request, pk):
        url_page = self.request.data['__next__']
        if url_page:
            this_page = int(url_page)
        else:
            this_page = 1
        try:
            music = AllSongMusic.objects.get(id=pk)

            part_music = music.music_auth_part
            if part_music:
                part_id = part_music.id
                part_music.delete()
                OperationLogs.objects.create(object_id=part_id, object_rep="partsongmusic", type="del",
                                             change_message="delete partsongmusic",
                                             user=request.user)
            else:
                pass
            music.delete()
            OperationLogs.objects.create(object_id=pk, object_rep="allsongmusic", type="del",
                                         change_message="delete allsongmusic",
                                         user=request.user)


            return HttpResponseRedirect("/operate/postrecord/?page=%d"%this_page)
        except:
            return HttpResponse("error")



class Category_Set_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/category_set.html'
    def get(self,request):

        category=AllMusicCategory.objects.select_related().all()
        return js_resp_htpg(category,request,CategorySerializer,pages=20)


class Create_Category_Set_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/category_set.html'

    def get(self,request):
        category=None
        return js_resp_htpg(category, request, CategorySerializer, pages=20)



    def post(self,request):
        serializer_new = CategorySerializer(data=request.data)

        if serializer_new.is_valid():
            serializer_new.save()
            return HttpResponseRedirect("/operate/category_set/")
        else:
            return HttpResponse("error")


class Edit_CategorySet(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)

    def post(self, request, pk):

        try:

            category = AllMusicCategory.objects.get(id=pk)
            obj_old = copy.deepcopy(category)

            serializer = CategorySerializer(category, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                if category is not None:
                    datas = self.request.data
                    update_fields = {"rank": datas["rank"], "name": datas["name"],
                                     "is_online": datas["is_online"]}

                    operationlogs(self.request, obj_old, update_fields, "change")
                # return HttpResponseRedirect("/operate/category_set/?page=%d" % this_page)

                rank = request.data['rank']
                name = request.data['name']
                is_online = request.data['is_online']

                if is_online == "1":
                    isonline = '显示'
                else:
                    isonline = "不显示"
                return json_resp(code=200, msg="ok", data={"name": name, "rank": rank, "isonline": isonline})
            else:
                return HttpResponse("error")
        except:
            return HttpResponse("error")


class Category_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/category.html'

    def get(self, request):
        song_post = AllSongMusic.objects.select_related().filter(is_enable=1).order_by('-created_at')
        # song_count = song_post.count()
        category_obj = AllMusicCategory.objects.select_related().filter(is_online=True)
        category_ser = CategorySerializer(category_obj, many=True)
        return js_resp_htpg(song_post, request, AllSongMusic_htm_Serializer, obj_singer=category_ser.data, title="分类管理")


class CategorySearch_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/category.html'

    def get(self, request):
        title = self.request.GET.get('title')
        S = self.request.GET.get('S')  # 输入框,music_name，用户名，歌曲名，ID
        WS = self.request.GET.get('WS')  # 分类
        # WB = self.request.GET.get('WB')  # 分类

        if 'S' in self.request.GET and self.request.GET['S']:
            S = self.request.GET['S']
        else:
            S = ""
        if 'WS' in self.request.GET and self.request.GET['WS']:
            WS = self.request.GET['WS']
        else:
            WS = ""

        if 'WB' in self.request.GET and self.request.GET['WB']:
            WB = self.request.GET['WB']
        else:
            WB = ""

        sSq = (Q(music_info__music_name__icontains=S) | Q(all_music_auth__username__icontains=S))
        wSq = Q(all_category__id=WS)
        # wBq = Q(all_category__id=WB)

        if S and WS:
            sql = sSq & wSq

        elif S:
            sql = sSq
        elif WS:
            sql = wSq
        else:
            sql = (Q())
        WT = ""
        search_word = {"S": S, "WS": WS, "WB": WB, "WT": WT}

        # music1=AllSongMusic.objects.filter()[:100]
        music = AllSongMusic.objects.filter(sql,is_enable=True)
        # music = MusicProfiel.objects.all()[:60]
        category_obj = AllMusicCategory.objects.select_related().filter(is_online=True)
        category_ser = CategorySerializer(category_obj, many=True)
        return js_resp_htpg(music, request, AllSongMusic_htm_Serializer, obj_singer=category_ser.data, title=title,
                            search_word=search_word)


class Edit_Category(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)

    def post(self, request, pk):

        try:

            music = AllSongMusic.objects.get(id=pk)
            obj_old = copy.deepcopy(music)

            all_id = request.data.get('all_category')
            if all_id:
                data = AllMusicCategory.objects.get(id=all_id)
            else:
                data = None
            serializer = AllSongMusic_htm_Serializer(music, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(all_category=data)

                if data is not None:
                    datas = self.request.data
                    update_fields = {"all_category": datas["all_category"]}

                    operationlogs(self.request, obj_old, update_fields, "change")
                # return HttpResponseRedirect("/operate/category/?page=%d" % this_page)
                #
                if data:
                    all_category=data.name
                else:
                    all_category="未分类"
                return json_resp(code=200,msg="",data={"all_category":all_category})
            else:
                return HttpResponse("error")
        except:
            return HttpResponse("error")





class Sing_Recommend_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/singrecommend.html'

    def get(self, request):
        music = MusicProfiel.objects.filter(Q(sort__gt=0)).order_by('-sort')
        singer_obj = Singer.objects.all()
        singer_ser = SingerSerializer(singer_obj, many=True)
        return js_resp_htpg(music, request, MusicHtmlSerializer, obj_singer=singer_ser.data,title="点歌推荐")


class Singsearch_Recommend_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/singrecommend.html'

    def get(self, request):
        S = self.request.GET.get('S')  # 输入框UID,music_name
        WS = self.request.GET.get('WS')  # 歌手iD
        WB = self.request.GET.get('WB')  # 是否男女对唱
        title=self.request.GET.get('title')

        if 'S' in self.request.GET and self.request.GET['S']:
            S = self.request.GET['S']
        if 'WS' in self.request.GET and self.request.GET['WS']:
            WS = self.request.GET['WS']
        if 'WB' in self.request.GET and self.request.GET['WB']:
            WB = self.request.GET['WB']

        sSq = (Q(music_name__icontains=S) | Q(uid=S))
        wSq = Q(singer__id=WS)
        wBq = Q(is_loved=WB)

        if S and WS and WB:
            sql = sSq & wSq & wBq

        elif S and WB:
            sql = sSq & wBq
        elif S and WS:
            sql = sSq & wSq

        elif WB and WS:
            sql = wBq & wSq

        elif S:
            sql = sSq
        elif WS:
            sql = wSq
        elif WB:
            sql = wBq
        else:
            sql = (Q())
        WT = ""
        search_word = {"S": S, "WS": WS, "WB": WB, "WT": WT}
        music = MusicProfiel.objects.filter(sql)
        # music = MusicProfiel.objects.all()[:60]
        singer_obj = Singer.objects.all()
        singer_ser = SingerSerializer(singer_obj, many=True)
        return js_resp_htpg(music, request, MusicHtmlSerializer, obj_singer=singer_ser.data,title=title,search_word=search_word)


class Edit_Sing_Recommend(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (Check_is_operate,)

    def post(self, request, pk):

        music = MusicProfiel.objects.get(id=pk)
        obj_old = copy.deepcopy(music)

        serializer = MusicHtmlSerializer(music, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if music is not None:
                datas = self.request.data
                update_fields = {"sort": datas["sort"]}

                operationlogs(self.request, obj_old, update_fields, "change")
            sort=request.data['sort']
            return json_resp(code=200,msg="ok",data={"sort":sort})
        else:
            return HttpResponse("error")


class NewSing_Recommend_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/newsingrecommend.html'

    def get(self, request):
        music = MusicProfiel.objects.filter(Q(new_sort__gt=0)).order_by('-new_sort')
        singer_obj = Singer.objects.all()
        singer_ser = SingerSerializer(singer_obj, many=True)
        return js_resp_htpg(music, request, MusicHtmlSerializer, obj_singer=singer_ser.data,title="最新歌曲推荐")


class NewSingsearch_Recommend_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/newsingrecommend.html'

    def get(self, request):
        S = self.request.GET.get('S')  # 输入框UID,music_name
        WS = self.request.GET.get('WS')  # 歌手iD
        WB = self.request.GET.get('WB')  # 是否男女对唱
        title=self.request.GET.get('title')

        if 'S' in self.request.GET and self.request.GET['S']:
            S = self.request.GET['S']
        if 'WS' in self.request.GET and self.request.GET['WS']:
            WS = self.request.GET['WS']
        if 'WB' in self.request.GET and self.request.GET['WB']:
            WB = self.request.GET['WB']

        sSq = (Q(music_name__icontains=S) | Q(uid=S))
        wSq = Q(singer__id=WS)
        wBq = Q(is_loved=WB)

        if S and WS and WB:
            sql = sSq & wSq & wBq

        elif S and WB:
            sql = sSq & wBq
        elif S and WS:
            sql = sSq & wSq

        elif WB and WS:
            sql = wBq & wSq

        elif S:
            sql = sSq
        elif WS:
            sql = wSq
        elif WB:
            sql = wBq
        else:
            sql = (Q())
        WT = ""
        search_word = {"S": S, "WS": WS, "WB": WB, "WT": WT}
        music = MusicProfiel.objects.filter(sql)
        # music = MusicProfiel.objects.all()[:60]
        singer_obj = Singer.objects.all()
        singer_ser = SingerSerializer(singer_obj, many=True)
        return js_resp_htpg(music, request, MusicHtmlSerializer, obj_singer=singer_ser.data,title=title,search_word=search_word)


class Edit_NewSing_Recommend(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)

    def post(self, request, pk):
        url_page = self.request.data['__next__']
        if url_page:
            this_page = int(url_page)
        else:
            this_page = 1
        music = MusicProfiel.objects.get(id=pk)
        obj_old = copy.deepcopy(music)
        serializer = MusicHtmlSerializer(music, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            if music is not None:
                datas = self.request.data
                update_fields = {"new_sort": datas["new_sort"]}

                operationlogs(self.request, obj_old, update_fields, "change")

            new_sort = request.data['new_sort']
            return json_resp(code=200, msg="ok", data={"new_sort": new_sort})
        else:
            return HttpResponse("error")


class Top50_recommend(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/toprecommend.html'

    def get(self, request):
        music = MusicProfiel.objects.filter(is_online=True, is_delete=False).order_by('-top_rank')
        singer_obj = Singer.objects.all()
        singer_ser = SingerSerializer(singer_obj, many=True)
        return js_resp_htpg(music, request, MusicHtmlSerializer, obj_singer=singer_ser.data,title="TOP50歌曲推荐")


class TopSingsearch_Recommend_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/toprecommend.html'

    def get(self, request):
        S = self.request.GET.get('S')  # 输入框UID,music_name
        WS = self.request.GET.get('WS')  # 歌手iD
        WB = self.request.GET.get('WB')  # 是否男女对唱
        title=self.request.GET.get('title')

        if 'S' in self.request.GET and self.request.GET['S']:
            S = self.request.GET['S']
        if 'WS' in self.request.GET and self.request.GET['WS']:
            WS = self.request.GET['WS']
        if 'WB' in self.request.GET and self.request.GET['WB']:
            WB = self.request.GET['WB']

        sSq = (Q(music_name__icontains=S) | Q(uid=S))
        wSq = Q(singer__id=WS)
        wBq = Q(is_loved=WB)

        if S and WS and WB:
            sql = sSq & wSq & wBq

        elif S and WB:
            sql = sSq & wBq
        elif S and WS:
            sql = sSq & wSq

        elif WB and WS:
            sql = wBq & wSq

        elif S:
            sql = sSq
        elif WS:
            sql = wSq
        elif WB:
            sql = wBq
        else:
            sql = (Q())
        WT = ""
        search_word = {"S": S, "WS": WS, "WB": WB, "WT": WT}
        music = MusicProfiel.objects.filter(sql)
        # music = MusicProfiel.objects.all()[:60]
        singer_obj = Singer.objects.all()
        singer_ser = SingerSerializer(singer_obj, many=True)
        return js_resp_htpg(music, request, MusicHtmlSerializer, obj_singer=singer_ser.data,title=title,search_word=search_word)


class Edit_TopSing_Recommend(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)

    def post(self, request, pk):

        music = MusicProfiel.objects.get(id=pk)
        obj_old = copy.deepcopy(music)
        serializer = MusicHtmlSerializer(music, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            if music is not None:
                datas = self.request.data
                update_fields = {"top_rank": datas["top_rank"]}

                operationlogs(self.request, obj_old, update_fields, "change")
            toprank = request.data['top_rank']
            return json_resp(code=200, msg="ok", data={"toprank": toprank})

        else:
            return HttpResponse("error")


class Newuser_recommend_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/newuserrecommend.html'

    def get(self, request):
        song_post = AllSongMusic.objects.filter(is_enable=True,is_delete=False).order_by('-is_recommend_rank','-created_at')[:50]
        # song_count = song_post.count()
        singer_obj = User.objects.all()
        singer_ser = UserHtmSer(singer_obj, many=True)
        return js_resp_htpg(song_post, request, AllSongMusic_htm_Serializer, obj_singer=singer_ser.data,title="新用户作品推荐")


class Newuser_recommendSearch_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/newuser-recommend.html'

    def get(self, request):
        S = self.request.GET.get('S')  # 输入框,music_name
        WS = self.request.GET.get('WS')  # 发布者
        WB = self.request.GET.get('WB')  # 星级
        title=self.request.GET.get('title')

        if 'S' in self.request.GET and self.request.GET['S']:
            S = self.request.GET['S']
        if 'WS' in self.request.GET and self.request.GET['WS']:
            WS = self.request.GET['WS']
        if 'WB' in self.request.GET and self.request.GET['WB']:
            WB = self.request.GET['WB']

        sSq = (Q(music_info__music_name__icontains=S) | Q(all_music_auth__username__icontains=S))
        wSq = Q(all_music_auth_id=WS)
        wBq = Q(rating_scale=WB)

        if S and WS and WB:
            sql = sSq & wSq & wBq

        elif S and WB:
            sql = sSq & wBq
        elif S and WS:
            sql = sSq & wSq

        elif WB and WS:
            sql = wBq & wSq

        elif S:
            sql = sSq
        elif WS:
            sql = wSq
        elif WB:
            sql = wBq
        else:
            sql = (Q())
        WT = ""
        search_word = {"S": S, "WS": WS, "WB": WB, "WT": WT}
        # music1=AllSongMusic.objects.filter()[:100]
        music = AllSongMusic.objects.filter(sql)
        # music = MusicProfiel.objects.all()[:60]
        singer_obj = User.objects.all()
        singer_ser = UserHtmSer(singer_obj, many=True)
        return js_resp_htpg(music, request, AllSongMusic_htm_Serializer, obj_singer=singer_ser.data,title=title,search_word=search_word)


class EditNewuser_recommend(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)

    def post(self, request, pk):
        url_page = self.request.data['__next__']
        if url_page:
            this_page = int(url_page)
        else:
            this_page = 1
        try:
            music = AllSongMusic.objects.get(id=pk)
            obj_old = copy.deepcopy(music)

            serializer = AllSongMusic_htm_Serializer(music, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                if music is not None:
                    datas = self.request.data
                    update_fields = {"is_recommend_rank": datas["is_recommend_rank"]}

                    operationlogs(self.request, obj_old, update_fields, "change")
                # return HttpResponseRedirect("/operate/newuser-recommend/?page=%d" % this_page)
                labrank=request.data['is_recommend_rank']
                return json_resp(code=200,msg="",data={"labrank":labrank})
            else:
                return HttpResponse("error")
        except:
            return HttpResponse("error")


@login_required
def Up_Mobilejson(request):
    user = request.user
    import time, os, json
    from time import strftime, localtime

    if user.has_perm('app_auth.view_operate_list'):
        if request.method == 'POST':

            try:
                jsonfiles = request.FILES.get('file', '')
                fn = time.strftime('%Y%m%d%H%M%S')
                filename = fn + jsonfiles.name
                fname = os.path.join(settings.MEDIA_ROOT, 'upfile/mobilejson/%s' % strftime('%Y/%m/%d', localtime()),
                                     filename)
                if os.path.exists(fname):
                    os.remove(fname)
                dirs = os.path.dirname(fname)
                if not os.path.exists(dirs):
                    os.makedirs(dirs)

                if os.path.isfile(fname):
                    os.remove(fname)
                content = jsonfiles.read()
                fp = open(fname, 'wb')
                fp.write(content)
                fp.close()

                with open(fname) as json_file:
                    data = json.load(json_file)

                querysetlist = []

                if data:
                    for d in data:
                        # js_d=json.loads(d)
                        # print js_d
                        print d
                        mobile_brand = d['Manufacturer']
                        # mobile_name = str(d['Name']).replace('\\', "\")
                        mobile_name = d['Name']
                        mobile_version = d['Model']
                        mobile_edition = d['OS']
                        mobile_yj_name = d['deviceName']

                        querysetlist.append(MobileVersion(mobile_brand=mobile_brand, mobile_name=mobile_name,
                                                          mobile_version=mobile_version, mobile_edition=mobile_edition,
                                                          mobile_yj_name=mobile_yj_name))

                    MobileVersion.objects.bulk_create(querysetlist)
                    successinfo = "上传成功"

                    return render_to_response('operate/include/upmobilejson.html', {
                        "title": '上传手机信息',
                        'rest': successinfo}, context_instance=RequestContext(request))
            except Exception as e:

                successinfo = "上传失败%s" % e

                return HttpResponse(successinfo)

        else:
            return render_to_response('operate/include/upmobilejson.html', {
                "title": '上传手机信息'}, context_instance=RequestContext(request))
    else:
        return HttpResponse('You are not have permission')


class MobileVersion_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/mobileversion.html'

    def get(self, request):
        obj_list = MobileVersion.objects.all()
        brand_list = []
        for obj_brand in obj_list:
            brand_list.append(obj_brand.mobile_brand)
        obj_brand_list = list(set(brand_list))
        return js_resp_htpg(obj_list, request, MobileVersionSer, obj_singer=obj_brand_list, pagenum=30)


class Mobileversearch(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/mobileversion.html'

    def get(self, request):
        S = self.request.GET.get('S')  # 输入框mobile_version
        WS = self.request.GET.get('WS')  # 手机品牌mobile_brand

        if 'S' in self.request.GET and self.request.GET['S']:
            S = self.request.GET['S']
        if 'WS' in self.request.GET and self.request.GET['WS']:
            WS = self.request.GET['WS']

        sSq = Q(mobile_version__icontains=S)
        wSq = Q(mobile_brand=WS)

        if S and WS:
            sql = sSq & wSq

        elif S:
            sql = sSq
        elif WS:
            sql = wSq

        else:
            sql = (Q())
        WT = ""
        WB = ""
        search_word = {"S": S, "WS": WS, "WB": WB, "WT": WT}
        mobile = MobileVersion.objects.filter(sql)
        ver_list = MobileVersion.objects.all()
        brand_list = []
        for obj_brand in ver_list:
            brand_list.append(obj_brand.mobile_brand)
        obj_brand_list = list(set(brand_list))
        return js_resp_htpg(mobile, request, MobileVersionSer, obj_singer=obj_brand_list, pagenum=30,search_word=search_word)


class Edit_Mobilever(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    def post(self, request, pk):
        # url=request.get_full_path()

        try:
            mobile = MobileVersion.objects.get(id=pk)

            obj_old = copy.deepcopy(mobile)  # 生成操作日志使用

            serializer = MobileVersionSer(mobile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                if mobile is not None:
                    datas = self.request.data
                    update_fields = {"delay_time": datas["delay_time"]}

                    operationlogs(self.request, obj_old, update_fields, "change")
                delaytime=request.data['delay_time']
                return json_resp(code=200,msg="",data={"delaytime":delaytime})
            else:
                return HttpResponse("error")
        except:
            return HttpResponse("error")


class CheckDb(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/checkdb.html'

    def get(self, request):
        # from khufu.settings import client_s3

        bucket_accompany = operate_s3.Bucket('duetin-accompany')
        bucket_lyrics = operate_s3.Bucket('duetin-lyrics')
        bucket_segments=operate_s3.Bucket('duetin-segments')
        l_accompany = bucket_accompany.objects.all()
        l_lyrics = bucket_lyrics.objects.all()
        l_segments=bucket_segments.objects.all()

        accompany_list = []

        for key in l_accompany:
            accompany = str(key.key).strip()
            accompany_list.append(accompany)

        lyrics_list = []

        for key in l_lyrics:
            lyric = str(key.key).strip()
            lyrics_list.append(lyric)

        segments_list = []

        for key in l_segments:
            segments = str(key.key).strip()
            segments_list.append(segments)

        obj_list = []
        my_list_q = MusicProfiel.objects.filter(is_online=True).order_by('id')
        my_list = list(my_list_q)

        for obj in my_list:
            obj_accompany = obj.bucket_accompany_key
            obj_lyrics = obj.bucket_lyrics_key
            obj_segments = obj.segments_key_name

            if obj_accompany in accompany_list:

                if obj_lyrics in lyrics_list:
                    if obj_segments in segments_list:
                        pass
                    else:
                        if obj_segments == None:
                            obj_segments = "mysql"
                        obj.segments_key_name = obj_segments + "---not found"
                        obj_list.append(obj)
                else:
                    if obj_lyrics == None:
                        obj_lyrics = "mysql"
                    obj.bucket_lyrics_key = obj_lyrics + "---not found"
                    obj_list.append(obj)

            else:
                if obj_accompany == None:
                    obj_accompany = "mysql"
                obj.bucket_accompany_key = obj_accompany + "---not found"
                obj_list.append(obj)

        # return None
        return js_resp_htpg(obj_list, request, MusicHtmlSerializer, obj_singer=obj_list, pagenum=30)

class Test(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (AllowAny,)

    def get(self, request):
        music_id_list = []
        music = AllSongMusic.objects.all()
        for obj in music:
            try:
                music_id = obj.music_auth_part.id
                music_id_list.append(music_id)

                part_music=obj.music_participant_part
                if part_music:
                    part_music_id=part_music.id
                    music_id_list.append(part_music_id)
            except:
                return HttpResponse("error")

        part_obj=PartSongMusic.objects.filter(is_delete=False)
        part_id_list=[]
        for part in part_obj:
            part_id=part.id
            part_id_list.append(part_id)


        l_set=list(set(music_id_list))

        ret_list = [item for item in part_id_list if item not in music_id_list]

        return json_resp(code=200, msg="", data={"mylist": l_set,"part_list":part_id_list,"ret_list":ret_list})

        # except:
        #     return HttpResponse("error")



class Partscore_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/partscore.html'

    def get(self, request):
        song_post = PartSongMusic.objects.all().order_by('-created_at')
        # song_count = song_post.count()
        singer_obj = User.objects.all()
        singer_ser = UserHtmSer(singer_obj, many=True)
        return js_resp_htpg(song_post, request, PartSongMusic_htm_Serializer, obj_singer=singer_ser.data,title="PART星级评分")


class Searchpartscore_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/partscore.html'

    def get(self, request):
        S = self.request.GET.get('S')  # 输入框,music_name
        WS = self.request.GET.get('WS')  # 发布者
        WB = self.request.GET.get('WB')  # 星级
        title = self.request.GET.get("title")

        if 'S' in self.request.GET and self.request.GET['S']:
            S = self.request.GET['S']
        if 'WS' in self.request.GET and self.request.GET['WS']:
            WS = self.request.GET['WS']
        if 'WB' in self.request.GET and self.request.GET['WB']:
            WB = self.request.GET['WB']

        sSq = (Q(music_info__music_name__icontains=S) | Q(music_auth__username__icontains=S))
        wSq = Q(music_auth_id=WS)
        wBq = Q(rating_scale=WB)

        if S and WS and WB:
            sql = sSq & wSq & wBq

        elif S and WB:
            sql = sSq & wBq
        elif S and WS:
            sql = sSq & wSq

        elif WB and WS:
            sql = wBq & wSq

        elif S:
            sql = sSq
        elif WS:
            sql = wSq
        elif WB:
            sql = wBq
        else:
            sql = (Q())
        WT = ""
        search_word = {"S": S, "WS": WS, "WB": WB, "WT": WT}
        # music1=AllSongMusic.objects.filter()[:100]
        music = PartSongMusic.objects.filter(sql)
        # music = MusicProfiel.objects.all()[:60]
        singer_obj = User.objects.all()
        singer_ser = UserHtmSer(singer_obj, many=True)
        return js_resp_htpg(music, request, PartSongMusic_htm_Serializer, obj_singer=singer_ser.data,title=title,search_word=search_word)


class Editpartscore(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)

    def post(self, request, pk):
        try:
            music = PartSongMusic.objects.get(id=pk)
            obj_old = copy.deepcopy(music)
            serializer = PartSongMusic_htm_Serializer(music, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                if music is not None:
                    datas = self.request.data
                    update_fields = {"rating_scale": datas["rating_scale"], "is_enable": datas["is_enable"]}

                    operationlogs(self.request, obj_old, update_fields, "change")

                is_enable=self.request.data['is_enable']
                if is_enable=="1":
                    enable="是"
                else:
                    enable="否"

                rating_scale=self.request.data['rating_scale']
                if rating_scale=="1":
                    scale="A"
                elif rating_scale=="2":
                    scale="B"
                elif rating_scale=="3":
                    scale="C"
                elif rating_scale=="4":
                    scale="D"
                elif rating_scale=="5":
                    scale="E"
                else:
                    scale="未定义"

                return json_resp(code=200,msg="",data={"isenable":enable,"scale":scale})
                # return HttpResponseRedirect("/operate/partscore/")
            else:
                return HttpResponse("error")
        except:
            return HttpResponse("error")


class Del_partpost(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)

    def post(self, request, pk):
        try:
            music = PartSongMusic.objects.get(id=pk)

            all_music = AllSongMusic.objects.filter(music_auth_part=music).first()
            all_music.delete()
            music.delete()
            OperationLogs.objects.create(object_id=pk, object_rep="partsongmusic", type="del",
                                         change_message="delete partsongmusic",
                                         user=request.user)


            return HttpResponseRedirect("/operate/partscore/")
        except:
            return HttpResponse("error")


class Post_data_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/postdata.html'

    def get(self, request):


        postdata=AllSongMusic.objects.select_related().filter(is_enable=1)
        return js_resp_htpg(postdata, request, PostData_htm_Serializer,pages=15,
                            title="合成原始数据")



class PostDataSearch_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/postdata.html'

    def get(self, request):
        title = self.request.GET.get("title")
        S = self.request.GET.get('S')  # 输入框,ID

        if 'S' in self.request.GET and self.request.GET['S']:
            S = self.request.GET['S']

        ws = Q(id=S)
        wsn=Q(all_music_auth__username__icontains=S)
        if S:
            try:
                m=int(S)
                sql = ws
            except:
                n=S
                sql = wsn
        else:
            sql = (Q())

        WT = ""
        WS=""
        WB=""
        search_word = {"S": S, "WS": WS, "WB": WB, "WT": WT}

        music = AllSongMusic.objects.filter(sql)
        return js_resp_htpg(music, request, PostData_htm_Serializer,title=title,
                            search_word=search_word)

class Del_postdata(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)

    def post(self, request, pk):
        try:
            all_music = AllSongMusic.objects.get(id=pk)
            all_music.delete()
            OperationLogs.objects.create(object_id=pk, object_rep="allsongmusic", type="del",
                                         change_message="delete allsongmusic",
                                         user=request.user)
            part_music=all_music.music_auth_part
            part_music.delete()
            OperationLogs.objects.create(object_id=pk, object_rep="partsongmusic", type="del",
                                         change_message="delete partsongmusic",
                                         user=request.user)
            return HttpResponseRedirect("/operate/postdata/")
        except:
            return HttpResponse("error")
def shuju(request):

    all_music=AllSongMusic.objects.filter(music_participant_part=None)


    for all_m in  all_music:
        photo=all_m.photo
        vedio=all_m.vedio
        try:
            part_music=all_m.music_auth_part
            if not part_music.vedio:
                part_music.vedio=vedio
                part_music.photo=photo
                part_music.save()
        except:
            pass
    return HttpResponse("ok")


class allpostdata(APIView):
    # permission_classes=(AllowAny,)
    permission_classes = (Check_is_operate,)
    def get(self,request):

        # all_music=AllSongMusic.objects.select_related().filter(Q(is_enable=1)&Q(music_auth_part__is_enable=1)&Q(music_participant_part=None)&Q(id__gt=10645)&Q(id__lt=11031))
        all_music=AllSongMusic.objects.select_related().filter(Q(is_enable=1)&Q(music_auth_part__is_enable=1)&Q(music_participant_part__id__gt=0)&Q(id__lt=11031))
        # all_music = AllSongMusic.objects.select_related().filter(all_music_auth__id=55)


        serializers=PostData_htm_Serializer(all_music,many=True)
        ser_data=serializers.data
        return json_resp(data=ser_data,code=200,msg='ok')


class Song_Case_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/song_case.html'

    def get(self, request):
        song_case = SongException.objects.all().order_by('-created_at')

        # case_ser = Create_SongExceptionSerializer(song_case, many=True)
        return js_resp_htpg(song_case, request, Create_SongExceptionSerializer,
                            title="歌曲用户报告异常")



class Song_Case_Search_View(APIView):
    """
    A view that returns a templated HTML representation of a given user.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (Check_is_operate,)

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/song_case.html'

    def get(self, request):
        # S = self.request.GET.get('S')  # 输入框UID,music_name
        WS = self.request.GET.get('WS')  # 歌手iD
        WB = self.request.GET.get('WB')  # 是否男女对唱
        # WT = self.request.GET.get('WT')  # 歌曲类型

        S=""
        WT=""

        if 'WS' in self.request.GET and self.request.GET['WS']:
            WS = self.request.GET['WS']
            wSq = Q(case_option=WS)
        else:
            wSq = Q()
        if 'WB' in self.request.GET and self.request.GET['WB']:
            WB = self.request.GET['WB']
            wBq = Q(is_settle=WB)
        else:
            wBq = Q()


        sql = wSq & wBq

        case = SongException.objects.filter(sql).order_by('-created_at')

        search_word = {"S": S, "WS": WS, "WB": WB, "WT": WT}
        return js_resp_htpg(case, request, Create_SongExceptionSerializer, search_word=search_word)


class Edit_SongCase(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)

    def post(self, request, pk):
        try:
            case = SongException.objects.get(id=pk)

            obj_old = copy.deepcopy(case)  # 生成操作日志使用
            serializer = Create_SongExceptionSerializer(case, data=request.data)
            if serializer.is_valid():
                serializer.save()

                if case is not None:
                    datas = self.request.data
                    update_fields = {"is_settle": datas["is_settle"]}

                    operationlogs(self.request, obj_old, update_fields, "change")
                #
                res = request.data.get("is_settle")
                if res == "1":
                    res_t = "已处理"
                else:
                    res_t = "未处理"
                return json_resp(code=200, msg=res_t)
            else:
                return HttpResponse("error")
        except:
            return HttpResponse("error")



class Del_Songcase_View(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)

    def post(self, request, pk):
        try:
            case = SongException.objects.get(id=pk)

            case.delete()
            # OperationLogs.objects.create(object_id=pk, object_rep="partsongmusic", type="del",
            #                              change_message="delete partsongmusic",
            #                              user=request.user)

            return HttpResponseRedirect("/operate/song_case/")
        except:
            return HttpResponse("error")


class ManualPost_View(APIView):
    """
    手动合成合唱数据
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/manualpost.html'

    def get(self, request):
        all_music = AllSongMusic.objects.select_related().filter(
            Q(is_enable=1) & Q(music_auth_part__is_enable=1) & Q(music_participant_part__id__gt=0)).order_by('id')

        return js_resp_htpg(all_music, request, All_Songmusic_Manual_htm_Serializer, pagenum=30, title=u'手动合成合唱数据')


class ManualPost_Search_View(APIView):
    """
    手动合成合唱数据搜索
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (Check_is_operate,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'operate/manualpost.html'

    def get(self, request):
        title = self.request.GET.get("title")
        S = self.request.GET.get('S')  # 输入框,ID

        if 'S' in self.request.GET and self.request.GET['S']:
            S = self.request.GET['S']

        ws = Q(id=S)
        wsn = Q(id=S)
        if S:
            try:
                m = int(S)
                sql = ws
            except:
                n = S
                sql = wsn
        else:
            sql = (Q())

        WT = ""
        WS = ""
        WB = ""
        search_word = {"S": S, "WS": WS, "WB": WB, "WT": WT}

        music = AllSongMusic.objects.filter(sql)
        return js_resp_htpg(music, request, All_Songmusic_Manual_htm_Serializer, title=title,
                            search_word=search_word)
