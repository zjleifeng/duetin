#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: views.py
@time: 2017/3/29 下午3:33
@SOFTWARE:PyCharm
"""
import datetime, hashlib, time, uuid
from django.contrib.auth import authenticate, logout, login
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from app_auth.models import ResetPasswordToken, RegisterEmailToken, InsBinding
from khafre.utils.json_response import json_resp
from .utils import is_valid_password, is_valid_username
from .serializers import UserSerializer, AccountSerializer, SuggestSerializer, FollowersSerializer, UserLoginSer, \
    UserProSerializer, User_Info_Serializer, UserInfoSerializer
from app_auth.models import User, MobileVersion
from khafre.utils.pags import js_resp_paging
from django.core.cache import caches
from khafre.tasks import following_msg
from relationships import Relationship
from khufu.settings import redis_ship
from django.db.models import Q
from khafre.tasks import send_register_url_email, send_reset_password_url_email_to
from django.contrib.auth import login
from social_django.utils import psa
from fcm_django.models import FCMDevice
from .utils import mylogin
from django.shortcuts import render
from khufu.settings import sts_client, SOCIAL_AUTH_INSTAGRAM_KEY, SOCIAL_AUTH_INSTAGRAM_SECRET
import urllib
import urllib2
import json, base64
from instagram.client import InstagramAPI
from khafre.utils.aliSTStoken import alistsauth
from khafre.utils.language import check_lan
import logzero, logging

logger_in = logzero.setup_logger(name="mylogger", logfile="/tmp/first-logger.log", level=logging.ERROR)

r = Relationship(redis_ship)
oth_db = caches['oth']


@psa('social:complete')
def register_by_access_token(request, backend, access_token, oauth_token_secret=None):
    if backend == "facebook":
        access_token = access_token
    elif backend == "twitter":
        oauth_token = access_token
        oauth_token_secret = oauth_token_secret
        access_token = {}
        access_token['oauth_token'] = oauth_token
        access_token['oauth_token_secret'] = oauth_token_secret
    elif backend == 'instagram':
        access_token = access_token
    my_user_id = request.user.id
    if my_user_id:
        my_user = request.user
    else:
        my_user = None
    try:
        user = request.backend.do_auth(access_token, user=my_user)
        if user:
            rest = {}
            token = Token.objects.get(user_id=user.pk)
            if token:
                if user.last_login:
                    rest["token"] = token
                    rest["user_id"] = user.id
                    rest["is_new"] = False
                else:
                    rest["token"] = token
                    rest["user_id"] = user.id
                    rest["is_new"] = True

                return rest
            else:
                return None
        else:
            return None

    except Exception as e:
        return 433


class FcmTokenView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        OK
        code:
        408:fcmtoken error

        :param request: 
        :return: 
        """
        code_lag = check_lan(request)

        registration_id = request.data.get("registration_id", "")
        if registration_id:
            user = request.user
            username = user.username
            fcm_obj = FCMDevice.objects.filter(user=user).first()

            if fcm_obj:
                fcm_obj.update(name=username, registration_id=registration_id)
            else:

                FCMDevice.objects.create(name=username, registration_id=registration_id, type='android',
                                         user=user)
            return json_resp(code=200, msg=code_lag['200'])
        else:
            return json_resp(code=468, msg=code_lag['468'])


class Mobile_Version_view(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        OK
        code:
        408:fcmtoken error

        :param request: 
        :return: 
        """

        code_lag = check_lan(request)
        devicename = request.data.get('devicename', None)
        if devicename:
            dn = base64.urlsafe_b64decode(str(devicename))
        else:
            dn = None

        model_name = request.data.get('model', None)
        if model_name:
            mn = base64.urlsafe_b64decode(str(model_name))
        else:
            mn = None

        manufacturer = request.data.get('manufacturer', None)
        if manufacturer:
            mf = base64.urlsafe_b64decode(str(manufacturer))
        else:
            mf = None
        os_name = request.data.get('os', None)
        if os_name:
            os_n = base64.urlsafe_b64decode(str(os_name))
        else:
            os_n = None
        mobile_l = MobileVersion.objects.filter(mobile_yj_name=dn, mobile_version=mn, mobile_brand=mf,
                                                mobile_edition=os_n).first()
        if mobile_l:
            mobile_id = mobile_l
        else:
            mobile_id = MobileVersion.objects.create(mobile_yj_name=dn, mobile_version=mn, mobile_brand=mf,
                                                     mobile_edition=os_n)

        user_id = request.user.id
        try:
            myuser = User.objects.get(id=user_id)
            myuser.mobile = mobile_id
            myuser.save()
        except:
            return json_resp(code=472, msg=code_lag['472'])

        return json_resp(code=200, msg="ok")


class register_by_token(APIView):
    """
    OK

    第三方登录
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        code_lag = check_lan(request)
        backend = self.request.data.get('backend')
        access_token = self.request.data.get('access_token')
        oauth_token_secret = self.request.data.get('oauth_token_secret')

        try:

            if backend == 'facebook':

                rest = register_by_access_token(request, backend, access_token)

            elif backend == 'twitter':
                rest = register_by_access_token(request, backend, access_token, oauth_token_secret)
            elif backend == 'instagram':
                rest = register_by_access_token(request, backend, access_token)


            else:
                rest = None
        except:
            return json_resp(code=467, msg=code_lag['467'])

        if rest:
            token = rest['token']
            is_new = rest['is_new']
            user_id = rest['user_id']
            try:
                user = User.objects.get(id=user_id)
                serializer = UserLoginSer(user)
                data = serializer.data
                data['token'] = token.key
                data['is_new'] = is_new
                data['uid'] = user_id
                mylogin(request, user)
            except:
                return json_resp(code=467, msg=code_lag['467'])

            return json_resp(code=200, msg='ok', data=data)
        else:
            return json_resp(code=466, msg=code_lag['466'])


class Newuser_Edit_View(APIView):
    """
    OK
    第三方登录新用户第一次登录修改信息
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            return self.request.auth.user
        except User.DoesNotExist:
            return None

    def post(self, request):
        code_lag = check_lan(request)
        if request.user.social_auth.exists():
            username = self.request.data.get("username")
            password = self.request.data.get('password')
            if username and password:
                exist_username = User.objects.filter(username=username).exists()

                if exist_username:
                    return json_resp(code=464, msg=code_lag['464'])
                elif not is_valid_password(password):
                    return json_resp(code=476, msg=code_lag['476'])
                else:
                    user = request.user
                    if user:
                        user.set_password(password)
                        user.username = username
                        user.save()
                        return json_resp(code=200, msg='ok')

            else:
                return json_resp(code=466, msg=code_lag['466'])
        else:
            return json_resp(code=467, msg=code_lag['467'])


class Social_login_View(APIView):
    """
    废弃接口
    """
    permission_classes = (AllowAny,)

    def mima(self):
        import random
        n = 10  # 固定密码位数，n=10
        l = list(range(0, 10))
        for x in range(65, 91):
            l.append(chr(x))
        for x in range(97, 123):
            l.append(chr(x))
        key = ''
        for i in range(n):
            key = key + str(random.choice(l))
        return key

    def name(self):
        import random
        n = 5  # 固定密码位数，n=10
        l = list(range(0, 10))
        for x in range(65, 91):
            l.append(chr(x))
        for x in range(97, 123):
            l.append(chr(x))
        key = ''
        for i in range(n):
            key = key + str(random.choice(l))
        return key

    def post(self):

        data = self.request.data
        backend = data['backend']
        uid = data['uid']
        extra_data = data['extra_data']
        access_token = extra_data['access_token']
        username = extra_data['username']
        touxiang = extra_data['touxiang']
        email = extra_data['email']

        password = self.mima()
        from social_django.models import UserSocialAuth
        haso = UserSocialAuth.objects.filter(uid=uid).first()
        if haso:
            token = haso.user.auth_token.key
            return json_resp(code=200, msg="", data={"token": token})
        else:
            if email:
                hasemail = User.objects.filter(email=email)
                if hasemail:
                    email = None

            if username:
                while User.objects.filter(username=username).first():
                    username = username + self.name()

                creatUser = User.objects.create_user(username=username, password=password, nickname=username,
                                                     email=email, tx=touxiang)

                UserSocialAuth.objects.create(user=creatUser, provider=backend, uid=uid, extra_data=extra_data)
                token = creatUser.auth_token.key
                # token=Token.objects.filter(user_id=creatUser.id).first()
                if token:
                    return json_resp(code=200, msg="", data={"token": token})
                else:
                    return json_resp(code=200, msg='no token')
            return json_resp(code=200, msg='no username')


class LoginView(APIView):
    """
    OK

    CODE

    409：not_this_username
    410：password_error
    用户登录

    """
    permission_classes = (AllowAny,)

    def post(self, request):
        code_lag = check_lan(request)
        if request.user.is_authenticated():
            return json_resp(code=466, msg=code_lag['466'])
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        # registration_id = request.data.get("registration_id", '')

        if username:
            exist_username = User.objects.filter(username=username).exists()
            exist_email = User.objects.filter(email=username).exists()

            if not exist_username and not exist_email:
                return json_resp(code=470, msg=code_lag['470'])
        else:
            return json_resp(code=461, msg=code_lag['461'])

        if password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            else:
                return json_resp(code=471, msg=code_lag['471'])
        else:
            return json_resp(code=462, msg=code_lag['462'])

        token = Token.objects.get(user_id=user.pk)
        serializer = UserLoginSer(user)
        data = serializer.data
        data["token"] = token.key
        return json_resp(code=200, msg='ok', data=data)


class LogoutView(APIView):
    """用户注销"""

    # Precondition:
    #   1. 使用者必須是已登入狀態, Oauth 使用者也可以登出
    #   2. 欄位: 沒有額外需求

    def __logout(self, request):
        if not request.user.is_authenticated():
            return json_resp(code=400, msg='user not login')
        logout(request)
        return json_resp(code=200, msg='ok')

    """
    def get(self, request):
        return self.__logout(request)
    """

    def post(self, request):
        return self.__logout(request)


class GeneralSignUpView(APIView):
    """
    用户注册
    email，username,password
    email和username不能重复。
    返回：code状态码，msg信息,context其他附加信息,
    code状态码：
    {
    460：already_login
    461:not username
    462:email_format_error
    463:email_hasregister
    464:username_hasregister
    465:username_format_error
    466:password_format_error
    467:create user error
    420:not data
    }
    result={user_id:用户id, username:用户名，email:邮箱，nickname:昵称，tx:头像，token:token信息}

    """
    permission_classes = (AllowAny,)

    def __response_block_already_login(self, request):
        return json_resp(code=460, msg='already_login')

    def __create_register_url(self, user):

        email = user.email
        url_seed = (email + time.ctime() + "#$@%$").encode("utf-8")
        url_token = hashlib.sha256(url_seed).hexdigest()

        entry_token_seed = str(uuid.uuid1()).encode("utf-8")
        entry_token = hashlib.md5(entry_token_seed).hexdigest()[10:16]

        current_time = timezone.localtime(timezone.now())
        accessible_time = current_time + datetime.timedelta(hours=24)

        # TODO 感覺上，因為已經知道 user 了，利用 user.resetpasswordtoken 似乎會比較快？
        # 但是會觸發 RelatedObjectDoesNotExist, 目前還不知道怎麼抓取
        rt, created = RegisterEmailToken.objects.get_or_create(user=user)
        rt.dynamic_url = url_token
        rt.entry_token = entry_token
        rt.expire_time = accessible_time

        try:
            rt.save()
        except:
            # IntegrityError
            # TODO 處理 dynamic url not unique
            rt = None

        return rt

    def put(self, request):
        code_lag = check_lan(request)
        email = request.data.get('email', '')

        if email:
            try:
                email = email.lower()
                validate_email(email)
                exist_email = User.objects.filter(email=email).exists()
                if exist_email:
                    return json_resp(code=463, msg=code_lag['463'])
                else:
                    return json_resp(code=200, msg='ok')
            except ValidationError:
                return json_resp(code=465, msg=code_lag['465'])
        else:
            return json_resp(code=465, msg=code_lag['465'])

    def post(self, request):
        code_lag = check_lan(request)
        if request.user.is_authenticated():
            return self.__response_block_already_login(request)
        email = request.data.get('email', '')
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        registration_id = request.data.get("registration_id", "")

        if username:
            username = username.lower()
            exist_username = User.objects.filter(username=username).exists()
            if exist_username:
                return json_resp(code=464, msg=code_lag['464'])
            else:
                if not is_valid_username(username):
                    return json_resp(code=465,
                                     msg=code_lag['465'])

        else:
            return json_resp(code=461, msg=code_lag['461'])

        if password:
            if not is_valid_password(password):
                return json_resp(code=465, msg=code_lag['465'])
        else:
            return json_resp(code=462, msg=code_lag['462'])

        if email:
            try:
                email = email.lower()

                validate_email(email)
                exist_email = User.objects.filter(email=email).exists()
                if exist_email:
                    return json_resp(code=463, msg=code_lag['463'])

            except ValidationError:
                return json_resp(code=465, msg=code_lag['465'])
        else:
            return json_resp(code=465, msg=code_lag['465'])

        try:

            myuser = User.objects.create_user(username=username, password=password,
                                              email=email)
        except:
            return json_resp(code=467, msg=code_lag['467'])
        user = authenticate(username=username, password=password)

        login(request, user)
        token = Token.objects.get(user_id=myuser.id)

        fcm_obj = FCMDevice.objects.filter(user=myuser)
        if fcm_obj:
            fcm_obj.update(name=username, registration_id=registration_id)
        else:

            FCMDevice.objects.create(name=username, registration_id=registration_id, type='android',
                                     user=myuser)

            #
        serializer = UserSerializer(myuser)
        if self.__create_register_url(myuser) is None:
            return json_resp(code=200, msg='register ok but send email error',
                             data={"token": token.key, "result": serializer.data})
        else:

            user_id = myuser.id

            send_register_url_email.delay(user_id)
            # return json_resp(code=400, msg="send reg mail error")

            return json_resp(code=200, msg='OK', data={"token": token.key, "result": serializer.data})


class RegisterEmailView(APIView):
    """邮箱验证"""
    permission_classes = (AllowAny,)

    def get(self, request, url_token, entry_token):
        # Dynamic URL Token Validation

        try:
            user_register_email_token = RegisterEmailToken.objects.get(dynamic_url=url_token)
        except RegisterEmailToken.DoesNotExist:
            return render(self.request, 'result.html', {"error": "The link is invalid"})

        # check Dynamic URL lifetime
        if timezone.now() > user_register_email_token.expire_time:
            return render(self.request, 'result.html',
                          {"error": "The link has expired. Please open the APP to verify it"})

        if user_register_email_token.user.is_email_val == True:
            return render(self.request, 'result.html', {"error": "The mailbox has been validated！"})

        # Empty Data Validation
        # if entry_token == "":
        #     return Response({"error": "请填写验证码"},
        #                     status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        entry_token_invalid = (entry_token != user_register_email_token.entry_token)
        if entry_token_invalid:
            return render(self.request, 'result.html', {"error": "The link is invalid"})

        token_user = user_register_email_token
        token_user.user.is_email_val = True
        token_user.is_activate = False
        token_user.save()
        token_user.user.save()

        return render(self.request, 'result.html', {"error": "Success!"})


class ChangePasswordView(APIView):
    """
    OK
    CODE
    416:old password error
    修改密码"""
    # Precondition:
    #   1. 使用者必須為登入狀態才可以更改密碼
    #   2. Oauth 使用者不可以更改密碼
    #
    # 修改完 Password 預設會被登出
    # 即使 Cookies 有記住新密碼也是一樣。

    permission_classes = (IsAuthenticated,)

    # def __response_block_oauth_account(self, request):
    #     return json_resp(code=400, msg='social user can not changepassword!')

    def post(self, request):
        code_lag = check_lan(request)
        current_password = request.data.get('current_password', '')
        new_password = request.data.get('new_password', '')
        confirm_new_password = request.data.get('confirm_new_password', '')

        if current_password == "" or new_password == "" or confirm_new_password == "":
            return json_resp(code=462, msg=code_lag['462'])

        if new_password != confirm_new_password:
            return json_resp(code=485, msg=code_lag['485'])

        if not is_valid_password(new_password):
            return json_resp(code=465, msg=code_lag['465'])

        user = request.user
        if not user.check_password(current_password):
            return json_resp(code=474, msg=code_lag['474'])

        user.set_password(new_password)
        user.save()
        logout(request)

        return json_resp(code=200, msg='ok')


class FindPasswordView(APIView):
    """
    通过邮箱找回密码
    OK
    code
    411:not_this_email_in_system
    """
    permission_classes = (AllowAny,)

    # Precondition:
    #   1. Oauth 使用者不可以尋找密碼
    #   2. 要填的資料: email
    #   填完後送出後，會寄一封信件給 user, 內容夾帶著 reset password
    #   的連結。

    def __create_reset_password_url(self, user):
        # TODO 怎麼 handle 創建失敗呢？

        email = user.email
        url_seed = (email + time.ctime() + "#$@%$").encode("utf-8")
        url_token = hashlib.sha256(url_seed).hexdigest()

        entry_token_seed = str(uuid.uuid1()).encode("utf-8")
        entry_token = hashlib.md5(entry_token_seed).hexdigest()[10:16]

        current_time = timezone.localtime(timezone.now())
        accessible_time = current_time + datetime.timedelta(minutes=10)

        # TODO 感覺上，因為已經知道 user 了，利用 user.resetpasswordtoken 似乎會比較快？
        # 但是會觸發 RelatedObjectDoesNotExist, 目前還不知道怎麼抓取
        rt, created = ResetPasswordToken.objects.get_or_create(user=user)
        rt.dynamic_url = url_token
        rt.entry_token = entry_token
        rt.expire_time = accessible_time

        try:
            rt.save()
        except:
            # IntegrityError
            # TODO 處理 dynamic url not unique
            rt = None

        return rt

    def post(self, request):
        email = request.data.get('email', '')
        code_lag = check_lan(request)
        if email == "":
            return json_resp(code=465, msg=code_lag['465'])

        try:
            validate_email(email)
        except ValidationError:
            return json_resp(code=465, msg=code_lag['465'])

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return json_resp(code=475, msg=code_lag['475'])

            # 因為 Oauth 帳戶沒有密碼，所以不提供這功能
        # if user.social_auth.exists():
        #     return json_resp(code=400, msg='social user')
        self.__create_reset_password_url(user)

        send_reset_password_url_email_to.delay(user.id)
        return json_resp(code=200, msg='ok')


class ResetPasswordView(APIView):
    """通过邮箱中的链接网页重设密码"""
    permission_classes = (AllowAny,)

    # Precondition:
    #   1. 使用者不可為登入狀態
    #   2. Oauth 使用者不可以尋找密碼
    #
    #   不讓已登入的人來找密碼
    #   設定成功之後，沒有限制重置次數（在允許時間內都可以)

    def __response_block_already_login(self, request):
        return render(self.request, 'result.html', {"error": "User logged in"})

    def get(self, request, url_token):
        if request.user.is_authenticated():
            return self.__response_block_already_login(request)

        return render(request, "resetpwd.html")

    def post(self, request, url_token):
        if request.user.is_authenticated():
            return self.__response_block_already_login(request)

        # Dynamic URL Token Validation
        try:
            user_reset_password_token = ResetPasswordToken.objects.get(dynamic_url=url_token)
        except ResetPasswordToken.DoesNotExist:
            return render(self.request, 'resetpwd.html', {"error": "Invalid link"})

        # check Dynamic URL lifetime
        if timezone.now() > user_reset_password_token.expire_time:
            return render(self.request, 'resetpwd.html', {"error": "Verify that the connection has exceeded time"})

        new_password = request.data.get('new_password', '')
        confirm_new_password = request.data.get('confirm_new_password', '')
        entry_token = request.data.get('entry_token', '')

        # Empty Data Validation
        if new_password == "" or confirm_new_password == "" or entry_token == "":
            return render(self.request, 'resetpwd.html', {"error": "Please fill in the complete information"})

        password_confirm_failed = (new_password != confirm_new_password)
        entry_token_invalid = (entry_token != user_reset_password_token.entry_token)
        if password_confirm_failed or entry_token_invalid:
            return render(self.request, 'resetpwd.html',
                          {"error": "The input is inconsistent or the code error is incorrect"})

        if not is_valid_password(new_password):
            return render(self.request, 'resetpwd.html', {"error": "Wrong password format"})

        # Reset Password
        user = user_reset_password_token.user
        user.set_password(new_password)
        user.save()

        return render(self.request, 'resetpwd.html', {"error": "Successful"})


class FollowersView(APIView):
    """
    OK
    code
    420: not data
    查看某人粉丝
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        followers = r(pk).followers()

        # if followers:
        followers_id_list = list(followers)
        user_list = User.objects.filter(id__in=followers_id_list)

        return js_resp_paging(user_list, request, FollowersSerializer, pages=20)

        # else:
        #     return json_resp(code=200, msg='ok')


class FollowingView(APIView):
    """
    OK

    查看某人关注的人
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):

        following = r(pk).following()
        if following:
            following_list = list(following)

            user_list = User.objects.filter(id__in=following_list)

            return js_resp_paging(user_list, request, FollowersSerializer, pages=15)
        else:
            return json_resp(code=420, msg='not data')


class InviteFolloeView(APIView):
    """
    ok

    查看某人关注的人和关注他的人的集合
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        my_id = request.user.id
        following = r(my_id).following()
        followers = r(my_id).followers()

        all_followers = following | followers

        if all_followers:
            all_followers_list = list(all_followers)
            if str(my_id) in all_followers_list:
                all_followers_list.remove(str(my_id))
            user_list = User.objects.filter(id__in=all_followers_list)

            return js_resp_paging(user_list, request, FollowersSerializer, pages=15)
        else:
            return json_resp(code=200, msg='ok')


class SearchUserView(APIView):
    """
    OK
    CODE
    415:NO ENTER
    根据用户名搜索用户
    """
    permission_classes = (IsAuthenticated,)

    def get_queryset_users(self, word):
        queryset_user = User.objects.filter(Q(username__istartswith=word))
        if queryset_user:
            return queryset_user
        else:
            return None

    def post(self, request):
        word = request.data.get("username", "")
        code_lag = check_lan(request)
        # if word:
        user_info = self.get_queryset_users(word)
        if user_info:
            return js_resp_paging(objs=user_info, request=request, serializer_obj=User_Info_Serializer)
        else:
            return json_resp(code=200, msg="ok")
            # else:
            #     return json_resp(code=486, msg=code_lag['486'])


class FollowView(APIView):
    """
    OK

    关注用户
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        code_lag = check_lan(request)
        owner_id = request.user.id
        isFollowed = int(request.data.get("isFollowed"))

        try:
            to_user = User.objects.get(id=pk)
            if isFollowed == 0:
                r(owner_id).unfollow(pk)
                return json_resp(code=200, msg='ok')
            elif isFollowed == 1:
                if owner_id == int(pk):
                    pass
                else:
                    r(owner_id).follow(pk)
                    following_msg.delay(request.user.id, to_user.id)

                return json_resp(code=200, msg='ok')
            else:

                return json_resp(code=499, msg=code_lag['499'])
        except User.DoesNotExist:
            return json_resp(code=466, msg=code_lag['466'])


class ProfileView(APIView):
    """
    OK
    411: not_this_email_in_system
    412: parameter “slug”error
    用户个人信息中心
    """
    permission_classes = (IsAuthenticated,)
    from rest_framework.versioning import AcceptHeaderVersioning
    versioning_class = AcceptHeaderVersioning

    def get_object(self):
        try:
            user = self.request.user
            return user
        except User.DoesNotExist:

            return None

    def get(self, request):

        code_lag = check_lan(request)

        user = self.get_object()
        if user:
            serializer = UserProSerializer(user, context={'request': request})
            return json_resp(code=200, msg=code_lag['200'], data=serializer.data)
        else:
            return json_resp(code=code_lag['466'], msg='user error')

    def check_email(self, email):
        """修改email检查是否重名"""
        new_email = email
        try:
            validate_email(new_email)
            myuser = self.request.user
            users = User.objects.filter(email=new_email)
            for u in users:
                u_id = u.id
                if u_id == myuser.id:
                    pass
                else:
                    return False

            return True
        except ValidationError:
            return False

    def __create_register_url(self, user):

        email = user.email
        url_seed = (email + time.ctime() + "#$@%$").encode("utf-8")
        url_token = hashlib.sha256(url_seed).hexdigest()

        entry_token_seed = str(uuid.uuid1()).encode("utf-8")
        entry_token = hashlib.md5(entry_token_seed).hexdigest()[10:16]

        current_time = timezone.localtime(timezone.now())
        accessible_time = current_time + datetime.timedelta(hours=24)

        # TODO 感覺上，因為已經知道 user 了，利用 user.resetpasswordtoken 似乎會比較快？
        # 但是會觸發 RelatedObjectDoesNotExist, 目前還不知道怎麼抓取
        rt, created = RegisterEmailToken.objects.get_or_create(user=user)
        rt.dynamic_url = url_token
        rt.entry_token = entry_token
        rt.expire_time = accessible_time

        try:
            rt.save()
        except:
            # IntegrityError
            # TODO 處理 dynamic url not unique
            rt = None

        return rt

    def put(self, request):
        code_lag = check_lan(request)
        user = self.get_object()
        tx = request.data.get("picture", "")
        back_pic = request.data.get('background', '')

        if back_pic:
            request.data['background_key_name'] = back_pic

        if tx:
            picture = 'http://userpic.duetin.com/' + str(tx)
            request.data['picture'] = picture
            request.data['picture_key_name'] = tx

        is_mail_val = user.is_email_val
        mail = request.data.get("email", "")
        if mail:
            if not self.check_email(mail):
                return json_resp(code=463, msg='email_hasregister')

        serializer = UserProSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if is_mail_val:
                pass
            else:

                if mail:
                    if self.__create_register_url(user) is None:
                        return json_resp(code=200, msg='send email error')
                    else:
                        user_id = user.id

                        send_register_url_email.delay(user_id)

            return json_resp(code=200, msg='ok')
        else:
            return json_resp(code=472, msg=code_lag['472'])
            #
            # slug = request.data.get('slug', '')
            # if slug == 'tx':
            #     serializer = UserSerializer(user, data=request.data, partial=True)
            #     if serializer.is_valid():
            #         serializer.save()
            #         return json_resp(code=200, msg='ok', data="")
            #     return json_resp(code=400, msg=serializer.errors)
            # elif slug == 'email':
            #     email = request.data.get('email', "")
            #     if email:
            #         try:
            #             validate_email(email)
            #             exist_email = User.objects.filter(email=email).exists()
            #             if exist_email:
            #                 return json_resp(code=403, msg="email_hasregister")
            #
            #         except ValidationError:
            #             return json_resp(code=402, msg="email_format_error")
            #
            #     serializer = UserProSerializer(user, data=request.data, partial=True)
            #
            #     if serializer.is_valid():
            #         serializer.save()
            #
            #         send_register_url_email.delay(user.id)
            #         return json_resp(code=200, msg='ok', data="")
            #     else:
            #         return json_resp(code=400, msg=serializer.errors)
            # elif slug == 'resume':
            #     resume = request.data.get("resume", "")
            #     if len(resume) > 150:
            #         return json_resp(code=425, msg="resume too long str")
            #     serializer = UserSerializer(user, data=request.data, partial=True)
            #     if serializer.is_valid():
            #         serializer.save()
            #         return json_resp(code=200, msg='ok', data="")
            #     return json_resp(code=400, msg=serializer.errors)
            # elif slug == 'sex':
            #     serializer = UserProSerializer(user, data=request.data, partial=True)
            #     if serializer.is_valid():
            #         serializer.save()
            #         return json_resp(code=200, msg='ok', data="")
            #     return json_resp(code=400, msg=serializer.errors)
            # else:
            #     return json_resp(code=412, msg='no slug:{}'.format(slug))


class First_User_Info_View(APIView):
    """
    OK
    返回用户个人信息，判断是否第一次登录，
    昵称，性别，生日
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            user = self.request.user
            return user
        except User.DoesNotExist:

            return None

    def get(self, request):
        code_lag = check_lan(request)
        user = self.get_object()
        if user:
            serializer = UserInfoSerializer(user, context={'request': request})
            return json_resp(code=200, msg='ok', data=serializer.data)
        else:
            return json_resp(code=466, msg=code_lag['466'])


class First_Edit_Pro_View(APIView):
    """
    OK
    第一次登录填写用户性别生日和昵称
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            user = self.request.user
            return user
        except User.DoesNotExist:
            return None

    def post(self, request):
        code_lag = check_lan(request)
        user = self.get_object()
        birth_o = request.data.get('birth')

        if birth_o:
            try:
                time_in = int(birth_o)
                timeStamp = time_in
                timeStamp /= 1000.0
                timearr = time.localtime(timeStamp)
                otherStyleTime = time.strftime("%Y/%m/%d", timearr)
                request.data['birth'] = otherStyleTime
                request.data['new_birth'] = time_in
            except:

                timeArray = time.strptime(birth_o, "%Y/%m/%d")
                birth = int(time.mktime(timeArray))
                request.data['new_birth'] = birth * 1000
                request.data['birth'] = str(birth_o)

        if user:
            serializer = UserProSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return json_resp(code=200, msg='ok')
            else:
                return json_resp(code=472, msg=code_lag['472'])

        else:
            return json_resp(code=466, msg=code_lag['466'])

            # def post(self, request):
            #     logger_in.error("start")
            #     code_lag = check_lan(request)
            #     user = self.get_object()
            #     birth_o = request.data.get('birth')
            #     birth_n=request.data.get('new_birth')
            #
            #     logger_in.error(type(birth_o))
            #     logger_in.error(birth_o)
            #     logger_in.error(type(birth_n))
            #
            #     logger_in.error(birth_n)
            #
            #     if birth_o:
            #         try:
            #             timeArray = time.strptime(birth_o, "%Y/%m/%d")
            #             birth = int(time.mktime(timeArray))
            #             request.data['new_birth'] = birth
            #         except:
            #             logger_in.error("birth_o")
            #             return json_resp(code=499, msg=birth_o)
            #     if birth_n:
            #         try:
            #             time_in=int(birth_n)
            #             time_str = datetime.datetime.fromtimestamp(time_in).strftime('%Y/%m/%d')
            #             request.data['birth']=time_str
            #
            #         except:
            #             logger_in.error("birth_n")
            #
            #             return json_resp(code=499, msg='birth_n')
            #
            #
            #     if user:
            #         serializer = UserProSerializer(user, data=request.data, partial=True)
            #         if serializer.is_valid():
            #             serializer.save()
            #             return json_resp(code=200, msg='ok')
            #         else:
            #             return json_resp(code=472, msg=code_lag['472'])
            #
            #     else:
            #         return json_resp(code=466, msg=code_lag['466'])


class ProfileUserView(APIView):
    """
    OK
    code

    413:id error
    他人用户中心
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        code_lag = check_lan(request)
        user = self.get_object(pk)
        if user:
            serializer = AccountSerializer(user, context={'request': request})
            return json_resp(code=200, msg='ok', data=serializer.data)
        else:
            return json_resp(code=472, msg=code_lag['472'])


class SuggestView(APIView):
    """
    OK

    用户建议"""
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        code_lag = check_lan(request)
        data = request.data
        data['owner'] = request.user.id
        serializer = SuggestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return json_resp(code=200, msg='OK')
        return json_resp(code=499, msg=code_lag['499'])


class Get_STStokenView(APIView):
    """
        OK
        获取S3临时token

        """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        code_lag = check_lan(request)
        user_name = request.user.username
        user_id = request.user.id
        rolesessionname = str(user_id) + "-" + user_name

        try:
            assumedRoleObject = sts_client.assume_role(
                RoleArn="arn:aws:iam::843144932323:role/adam",
                RoleSessionName=rolesessionname
                # Policy='{"Version":"2012-10-17", "Statement": [ {"Effect": "Allow", "Action": ["s3:GetBucketLocation",
                # "s3:ListAllMyBuckets"], "Resource": "arn:aws:s3:::*"}, {"Effect": "Allow", "Action": [
                # "s3:ListBucket"],
                #  "Resource": ["arn:aws:s3:::hasdemo"]}, {"Effect": "Allow", "Action": ["s3:PutObject", "s3:GetObject",
                # "s3:DeleteObject"], "Resource":["arn:aws:s3:::hasdemo/aec96c30-4784-11e6-bdf4-0800200c9a66/*"]} ]}'
            )
            credentials = assumedRoleObject['Credentials']

            aws_access_key_id = credentials['AccessKeyId']
            aws_secret_access_key = credentials['SecretAccessKey']
            aws_session_token = credentials['SessionToken']

            data = {"aws_access_key_id": aws_access_key_id, "aws_secret_access_key": aws_secret_access_key,
                    "aws_session_token": aws_session_token}

            return json_resp(code=200, msg='ok', data=data)
        except:
            return json_resp(code=499, msg=code_lag['499'])


class SendMSG(APIView):
    def post(self, request):
        # from push_notifications.models import APNSDevice, GCMDevice
        # fcm_device = GCMDevice.objects.create(registration_id="token", cloud_message_type="FCM", user=request.user)

        # device = GCMDevice.objects.get(registration_id="token")
        # device.send_message("You've got mail")
        event = request.data
        import json
        json_string = json.dumps(event)
        evt = json.loads(json_string)
        from fcm_django.models import FCMDevice
        # device = FCMDevice.objects.filter(user=request.user.id)

        # device.send_message(title='title', body='message')

        # from fcm.utils import get_device_model
        # Device = get_device_model()
        #
        # my_phone = Device.objects.get(name='test')
        # xx = my_phone.send_message({'message': 'my test message'}, collapse_key='something')
        # from fcm_django.models import FCMDevice
        # data = {
        #     "to": "bk3RNwTe3H0:CI2k_HHwgIpoDKCIZvvDMExUdFQ3P1...",
        #     "notification": {
        #         "body": "great match!",
        #         "title": "Portugal vs. Denmark",
        #         "icon": "myicon"
        #     }
        # }
        # device = FCMDevice.objects.all().first()
        #

        device = FCMDevice.objects.get(id=24)

        # device.send_message("Title")
        device.send_message(data={"test": "test"})
        # device.send_message(title="Title", body="Message", data={"test": "test"})
        return json_resp(code=200, msg='ok')


class Get_IP(APIView):
    def get(self, request):

        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        return json_resp(code=200, msg='ok', data={"ip": ip})


class User_List_View(APIView):
    """
    OK
    2018/3/12
    添加好友，显示用户列表
    """
    permission_classes = (IsAuthenticated,)

    def get_queryset_users(self, word):
        queryset_user = User.objects.filter(Q(username__istartswith=word))
        if queryset_user:
            return queryset_user
        else:
            return None

    def get(self, request):

        user_list = User.objects.select_related().filter(is_active=1).order_by('-add_user_rank', '-last_login')

        return js_resp_paging(objs=user_list, request=request, serializer_obj=User_Info_Serializer, pages=100)


class User_Recommend_View(APIView):
    """
    OK
    2018/3/12
    推荐给新用户的用户
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_list = User.objects.select_related().filter(is_active=1, is_recommend=1).order_by('-new_user_rank',
                                                                                               '-last_login')
        return js_resp_paging(objs=user_list, request=request, serializer_obj=User_Info_Serializer, pages=100)


class NewUser_FollowView(APIView):
    """
    OK

    关注用户  新用户推荐中关注，多人同时关注  
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user_list = User.objects.select_related().filter(is_active=1, is_recommend=1).order_by('-new_user_rank',
                                                                                               '-last_login')
        return user_list

    def post(self, request):
        code_lag = check_lan(request)
        owner_id = request.user.id
        user_id = request.data.get('user_id')
        isFollowed = int(request.data.get("isFollowed"))

        if user_id == 'followall':
            user_list = self.get_object()
            for obj_user in user_list:
                if r(owner_id).is_following(obj_user.id):
                    pass
                else:
                    r(owner_id).follow(obj_user.id)
                    following_msg.delay(owner_id, obj_user.id)
            return json_resp(code=200, msg='ok')


        elif user_id == "unfollowall":
            user_list = self.get_object()
            for obj_user in user_list:
                if r(owner_id).is_following(obj_user.id):
                    r(owner_id).unfollow(obj_user.id)
                else:
                    pass
            return json_resp(code=200, msg='ok')

        else:

            try:
                to_user = User.objects.get(id=user_id)
                if isFollowed == 0:
                    r(owner_id).unfollow(user_id)
                    return json_resp(code=200, msg='ok')
                elif isFollowed == 1:
                    r(owner_id).follow(user_id)

                    following_msg.delay(request.user.id, to_user.id)

                    return json_resp(code=200, msg='ok')
                else:

                    return json_resp(code=499, msg=code_lag['499'])
            except User.DoesNotExist:
                return json_resp(code=499, msg=code_lag['499'])


class Reg_Ins(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        code_lag = check_lan(request)
        code = request.GET.get('code')
        if code:
            return json_resp(code=200, msg='ok', data={"code": code})
        else:
            return json_resp(code=499, msg=code_lag['499'])


class Get_Token_Byins(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        code = request.data.get('code', '')
        code_lag = check_lan(request)
        if code:
            try:
                url = 'https://api.instagram.com/oauth/access_token'
                values = {
                    'client_id': SOCIAL_AUTH_INSTAGRAM_KEY,
                    'client_secret': SOCIAL_AUTH_INSTAGRAM_SECRET,
                    'redirect_uri': 'http://duetin.com/api/v1/account/reg_ins/',
                    'code': code,
                    'grant_type': 'authorization_code'
                }
                data = urllib.urlencode(values)
                req = urllib2.Request(url, data)
                response = urllib2.urlopen(req)
                response_string = response.read()
                insta_data = json.loads(response_string)
                access_token = insta_data['access_token']
                pic = insta_data['user']['profile_picture']
                uid = insta_data['user']['id']
                backend = 'instagram'

                return json_resp(code=200, msg='ok',
                                 data={"access_token": access_token, "backend": backend, 'uid': uid})
            except:
                return json_resp(code=499, msg=code_lag['499'])
        else:
            return json_resp(code=499, msg=code_lag['499'])


class Binding_Ins_View(APIView):
    """
    OK
    绑定ins帐号
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        code_lag = check_lan(request)
        access_token = request.data.get('access_token')
        uid_str = request.data.get('uid')

        try:
            uid = int(uid_str)
        except:
            return json_resp(code=499, msg=code_lag['499'])

        backend = 'instagram'

        user = request.user
        ins_user = InsBinding.objects.filter(user=user, provider='instagram').exists()
        if ins_user:
            return json_resp(code=477, msg=code_lag['477'])
        else:
            try:
                InsBinding.objects.create(provider=backend, uid=uid, access_token=access_token, user=request.user)

                return json_resp(code=200, msg='ok')
            except:
                return json_resp(code=481, msg=code_lag['481'])


class Release_Ins_View(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        code_lag = check_lan(request)
        try:
            ins_user = InsBinding.objects.get(provider='instagram', user=user)
            ins_user.delete()
            return json_resp(code=200, msg='ok')
        except:
            return json_resp(code=478, msg=code_lag['478'])


class Ins_Photo(APIView):
    """
    OK获取ins的图片
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        code_lag = check_lan(request)
        user = request.user
        try:
            ins_user = InsBinding.objects.get(user=user, provider='instagram')
        except:
            return json_resp(code=478, msg=code_lag['478'])
        if ins_user:
            # extra_data = ins_user.extra_data
            access_token = ins_user.access_token
            ins_id = ins_user.uid

            try:

                api = InstagramAPI(access_token=access_token, client_id=SOCIAL_AUTH_INSTAGRAM_KEY,
                                   client_secret=SOCIAL_AUTH_INSTAGRAM_SECRET)
                recent_media, next_ = api.user_recent_media(user_id=ins_id, count=15)
                ins_user = api.user(user_id=ins_id)
                ins_picture = ins_user.profile_picture
                ins_username = ins_user.username
            except:
                return json_resp(code=482, msg=code_lag['482'])
            photos = []
            for media in recent_media:
                nei_data = {}
                nei_data['photo'] = media.images['standard_resolution'].url
                created_time = media.created_time
                nei_data['created_time'] = created_time
                photos.append(nei_data)

            json_data = {"ins_id": ins_id, "ins_username": ins_username, 'ins_picture': ins_picture, "photo": photos}
            return json_resp(code=200, msg="ok", data=json_data)


class User_Ins_Photo(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        code_lag = check_lan(request)
        try:
            user = User.objects.get(id=pk)

        except:
            return json_resp(code=466, msg=code_lag['466'])

        try:
            ins_user = InsBinding.objects.get(user=user, provider='instagram')
        except:
            return json_resp(code=478, msg=code_lag['478'])
        if ins_user:
            # extra_data = ins_user.extra_data
            access_token = ins_user.access_token
            ins_id = ins_user.uid

            try:
                api = InstagramAPI(access_token=access_token, client_id=SOCIAL_AUTH_INSTAGRAM_KEY,
                                   client_secret=SOCIAL_AUTH_INSTAGRAM_SECRET)
                recent_media, next_ = api.user_recent_media(user_id=ins_id, count=8)

                ins_user = api.user(user_id=ins_id)
                ins_picture = ins_user.profile_picture
                ins_username = ins_user.username
            except Exception as e:
                # pass
                return json_resp(code=482, msg=code_lag['482'])

            photos = []
            for media in recent_media:
                nei_data = {}
                nei_data['photo'] = media.images['standard_resolution'].url
                created_time = media.created_time
                nei_data['created_time'] = created_time
                photos.append(nei_data)

            json_data = {"ins_id": ins_id, "ins_username": ins_username, 'ins_picture': ins_picture, "photo": photos}
            return json_resp(code=200, msg="ok", data=json_data)


class Ali_Oss_Auth_View(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        oss_auth = alistsauth(request)
        if oss_auth:
            return json_resp(code=200, msg='ok', data=oss_auth)
        else:
            return json_resp(code=499, msg="unknow error")


class testutc(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        obj_users = User.objects.filter(birth__isnull=False)

        for obj in obj_users:
            birth_str = obj.birth
            try:
                timeArray = time.strptime(birth_str, "%Y/%m/%d")
                birth = int(time.mktime(timeArray))
                obj.new_birth = birth*1000
                obj.save()
            except:

                pass

        return json_resp(code=200, msg='ok')
