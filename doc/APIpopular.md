# 用户API接口文档

此文档用于API接口的调试

## 接口概览  
```
/api/v1/popular/
```


##popular
### 接口地址：
```
/api/v1/popular/
```

### 接口接受方法：
```
GET
```
### GET方法  
#### 传入参数：

#### 接口返回参数  
```json
"id": 3,
    "title": "标题",
    "music_auth_part": {发起者部分歌曲信息
      "id": 1,
     
      "music_info": {歌曲信息
        "id": 2,
        "music_name": "qwe",
        "language": 0,
        "accompany": "qwew",
        "lyrics": "jkjk",
        "image": "lkjkl",
        "rank": 0,
        "created_at": "2017-04-13T08:34:09.970131Z",
        "snger_name": {歌手信息
          "id": 1,
          "singer_name": "wedfwe",
          "singer_country": "www",
          "sex": 1,
          "rank": 11,
          "photo": "wewe",
          "created_at": "2017-04-13T04:54:33.973366Z"
        }
      },
      "music_auth": {发起者信息
        "id": 1,
        "last_login": "2017-04-13T07:27:48.948011Z",
        "is_superuser": true,
        "username": "admin",
        "first_name": "",
        "last_name": "",
        "email": "wjkfnjkwe@ds.com",
        "is_staff": true,
        "is_active": true,
        "date_joined": "2017-04-12T16:37:28.581797Z",
        "groups": [],
       
      }
    },
    "music_participant_part": {
    
    },
    "photo": "图片地址",
    "vedio": "视频地址",
    "voice_url": "音频地址",
    "praise": 被赞次数,
    "view_times": 观看次数,
    "rank": 手动排序,
    "created_at": "2017-04-13T05:40:16.716864Z",加入时间
    "is_enable": true, 是否允许加入
    "all_music_comment_count": 0 , 评论次数
```
##### 如果参数全部正确  
状态码：```HTTP_201_CREATED```  

