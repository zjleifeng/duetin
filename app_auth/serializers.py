#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: serializers.py
@time: 2017/3/29 下午3:32
@SOFTWARE:PyCharm
"""
from django.contrib.auth.models import Group
from rest_framework import serializers
from app_auth.models import User, Fans, Suggest,InsBinding
import re
from dao.models.music import AllSongMusic
from relationships import Relationship
import redis
from khufu.settings import redis_ship,userpic_url
from social_django.models import UserSocialAuth


r = Relationship(redis_ship)


class FansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fans
        fields = ('id', 'owner_id', 'follower_id')
        # depth = 3


class FollowersSerializer(serializers.ModelSerializer):
    """序列化某人的粉丝"""

    is_following = serializers.SerializerMethodField()
    picture=serializers.SerializerMethodField()
    is_showbtn=serializers.SerializerMethodField()
    username=serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id','is_showbtn', 'username','nickname', 'picture', 'is_following')

    def get_username(self,obj):
        if obj:
            try:
                socal_user=UserSocialAuth.objects.get(user=obj)
                return ""
            except:
                return obj.username

    def get_is_following(self, obj):
        user = self.context['request'].user
        user_id = user.id
        if r(user_id).is_following(obj.id):
            return True
        else:
            return False

    def get_is_showbtn(self,obj):
        user = self.context['request'].user
        user_id = user.id
        if user_id==obj.id:
            return False
        else:
            return True

    def get_picture(self,obj):
        if obj.picture_key_name:
            pic=userpic_url+obj.picture_key_name
        else:
            if obj.picture:
                pic=obj.picture
            else:
                pic=''
        return pic

class FollowingSerializer(serializers.ModelSerializer):
    """序列化某人关注的人"""

    class Meta:
        model = Fans

        fields = ('id', 'follower_id')

class UserLoginSer(serializers.ModelSerializer):
    """登录获取到的数据"""
    picture=serializers.SerializerMethodField()
    user_id=serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('user_id', 'username', 'email', 'nickname', 'resume', 'picture','sex','birth','new_birth')

    def get_picture(self,obj):
        if obj.picture_key_name:
            pic=userpic_url+obj.picture_key_name
        else:
            if obj.picture:
                pic=obj.picture
            else:
                pic=''
        return pic

    def get_user_id(self,obj):
        user_id=obj.id
        return user_id


class UserHtmSer(serializers.ModelSerializer):
    """
    html 作品管理中user信息
    """
    class Meta:
        model = User
        fields = ('id', 'username')

class UserSerializer(serializers.ModelSerializer):
    """自己的个人中心"""
    post_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    picture=serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'nickname', 'resume', 'picture', 'sex',
                  'date_joined', 'is_email_val', 'post_count',
                  'following_count', 'followers_count','is_following')




    def get_post_count(self, obj):
        return obj.my_all_post.filter(is_delete=False).count()

    def get_following_count(self, obj):
        # return obj.fans_owner.all().count()
        return r(obj.id).following_count()

    def get_followers_count(self, obj):
        # return obj.fans_follower.all().count()
        return r(obj.id).follower_count()

    def get_is_following(self,obj):

        return True

    def get_picture(self,obj):
        if obj.picture_key_name:
            pic=userpic_url+obj.picture_key_name
        else:
            if obj.picture:
                pic=obj.picture
            else:
                pic=''
        return pic

    def update(self, instance, validated_data):
        instance.resume = validated_data.get('resume', instance.resume)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class UserInfoSerializer(serializers.ModelSerializer):

    """
    查询自己的昵称，生日，性别是否填
    """
    class Meta:
        model = User
        fields = ('id', 'nickname', 'sex','birth',"new_birth")



class UserProSerializer(serializers.ModelSerializer):
    """自己的个人中心"""

    post_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    photo=serializers.SerializerMethodField()
    is_bdins=serializers.SerializerMethodField()
    picture=serializers.SerializerMethodField()
    username=serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'nickname', 'resume','photo', 'picture', 'sex','birth','region',
                  'date_joined', 'is_email_val', 'post_count','background_key_name',"new_birth",
                  'following_count', 'followers_count', 'is_following','is_email_val','picture_key_name','is_bdins')
    def get_username(self,obj):
        if obj:
            try:
                socal_user=UserSocialAuth.objects.get(user=obj)
                return ""
            except:
                return obj.username

    def get_post_count(self, obj):
        return obj.my_all_post.filter(is_delete=False).count()

    def get_following_count(self, obj):
        return r(obj.id).following_count()

    def get_followers_count(self, obj):
        return r(obj.id).follower_count()

    def get_is_following(self,obj):
        return True

    def get_photo(self,obj):
        if obj.picture_key_name:
            pic=userpic_url+obj.picture_key_name
        else:
            pic=obj.picture
        return pic

    def get_picture(self,obj):
        if obj.picture_key_name:
            pic=userpic_url+obj.picture_key_name
        else:
            if obj.picture:
                pic=obj.picture
            else:
                pic=''
        return pic

    def get_is_bdins(self,obj):
        ins_user = InsBinding.objects.filter(user=obj,provider='instagram').exists()
        if ins_user:
            return True
        else:
            return False


    def update(self, instance, validated_data):
        instance.resume = validated_data.get('resume', instance.resume)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.email = validated_data.get('email', instance.email)
        instance.birth=validated_data.get('birth',instance.birth)
        instance.new_birth=validated_data.get('new_birth',instance.new_birth)
        instance.region=validated_data.get('region',instance.region)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.picture_key_name=validated_data.get('picture_key_name',instance.picture_key_name)
        instance.background_key_name=validated_data.get('background_key_name',instance.background_key_name)

        instance.save()
        return instance

class AccountSerializer(serializers.ModelSerializer):
    """他人个人中心"""

    post_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    picture=serializers.SerializerMethodField()
    is_bdins=serializers.SerializerMethodField()
    username=serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'nickname', 'resume', 'picture', 'sex','birth',
                  'date_joined', 'is_email_val', 'post_count','new_birth',
                  'following_count', 'followers_count', 'is_following','is_email_val','is_bdins')

    def get_username(self,obj):
        if obj:
            try:
                socal_user=UserSocialAuth.objects.get(user=obj)
                return ""
            except:
                return obj.username

    def get_post_count(self, obj):
        return obj.my_all_post.filter(is_delete=False).count()

    def get_following_count(self, obj):
        # return obj.fans_owner.all().count()
        return r(obj.id).following_count()

    def get_followers_count(self, obj):
        # return obj.fans_follower.all().count()
        return r(obj.id).follower_count()

    def get_is_following(self, obj):
        user = self.context['request'].user
        user_id = user.id
        if user_id==obj.id:
            return True
        else:
            if r(user_id).is_following(obj.id):
                return True
            else:
                return False

    def get_picture(self,obj):
        if obj.picture_key_name:
            pic=userpic_url+obj.picture_key_name
        else:
            if obj.picture:
                pic=obj.picture
            else:
                pic=''
        return pic

    def get_is_bdins(self,obj):
        ins_user = InsBinding.objects.filter(user=obj,provider='instagram').exists()
        if ins_user:
            return True
        else:
            return False

class SuggestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggest
        fields = ('id', 'title', 'context', 'owner')
        owner = serializers.ReadOnlyField(source='owner.username')

    def create(self, validated_data):
        return Suggest.objects.create(**validated_data)



class User_Info_Serializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()
    picture = serializers.SerializerMethodField()
    username=serializers.SerializerMethodField()

    class Meta:
        model=User
        fields=('id','username','nickname','picture','is_following')
    def get_username(self,obj):
        if obj:
            try:
                socal_user=UserSocialAuth.objects.get(user=obj)
                return ""
            except:
                return obj.username

    def get_picture(self,obj):
        if obj.picture_key_name:
            pic=userpic_url+obj.picture_key_name
        else:
            if obj.picture:
                pic=obj.picture
            else:
                pic=''
        return pic

    def get_is_following(self, obj):
        user = self.context['request'].user
        user_id = user.id
        if user_id==obj.id:
            return True
        else:
            if r(user_id).is_following(obj.id):
                return True
            else:
                return False