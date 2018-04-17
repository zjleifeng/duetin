 #所有接口前api/v1/
 
 ##用户模块接口
 
```json

account/register/               #注册接口 提交方法:POST 数据username,email,password
account/token/                  #用户名密码登，获取token：POST 数据username,password
account/login/                  #登录接口 提交方法:POST 数据`username`  or `email` and `password`  返回用所有信息以及token
account/logout/                 #注销接口 提交方法:POST （暂时不用）
account/profile/              #个人用户中心 提交方法:GET(查看) PUT(更新个人资料   参数：必须参数body(picture，email,resume,sex)外加一个识别字段slug(tx，email,resume,sex)  更改参数'picture','email','resume','sex')  
account/profile/users/(?P<pk>\d+)/     #查看某用户个人中心 提交方法:GET(查看 用户ID)
account/profile/followers/(?P<pk>\d+)/         #查看某用户的粉丝 提交方法:GET(查看 用户的ID)
account/profile/following/(?P<pk>\d+)/        #查看某用户所关注的人 提交方法:GET(查看 用户ID)
account/profile/follower_edit/(?P<pk>\d+)/    #关注某人 提交方法POST(被关注者ID)
account/change_password/                      #更改密码 t提交方法POST(修改密码 'current_password','new_password','confirm_new_password')
account/suggest/                              #提交建议  提交方法POST(提交建议内容'context')
account/find_password/                        #通过邮箱找回密码   提交方法POST(找回密码,字段'email')
account/register-by-token/     #通过第三方登录，POST数据"backend"：登录后端为哪里（twitter或者facebook），"access_token","oauth_token_secret":twitter需要，
                                返回json：：token ,is_new（判断是否为新用户，若是新用户，则需要修改用户名,用下面接口）
account/new-user-edit/         #第三方登录的新用户，需要修改用户名和密码，     POST（参数 username，password）,头部需要带上token验证                     




```


##主页面接口POPULAR

```json
music/allmusic_h5/      #分享的HTML播放页面（前段不需要处理）
music/popular/          #加载主页视频 提交方法GET()
music/all_music_detail/(?P<pk>[0-9]+)/    #播放摸个视频 提交方法GET(加载某视频信息播放)
                                          #PUT对此视频进行praise赞，comment评论,share分享等操作
                                          # put参数slug(praise,comment,share)当参数为comment,必须在加一个参数content为评论内容            
music/del_music/<pk>/     #删除视频 请求方法PUT,视频id。删除视频必须是本人发布的视频，否则无权限
music/search/         #主页面搜索功能    提交方法POST(提交参数'word':搜索关键词，"slug":搜索哪个页面:people,sing)
```


##唱歌页面接口SING

```json
sing/banner/        #加载banner接口GET(可单独调用也可不用。主页面加载默认已经加载不需要调用)
sing/sing_index/(?P<slug>\w+)/        #唱歌主页面加载数据   请求方法GET(slug值为'pop'或者'new'对应相应接口)
sing/search_sing/                     #唱歌搜索功能      提交方法   POST(请求字段'word')
sing/sing_song/(?P<pk>[0-9]+)/        #唱歌加载数据      点击唱歌
                                    请求方法GET  url参数PK:歌曲表ID ，若返回数据result中含有is_loved=True,则这首歌为男女对唱歌曲，需要用户选择进入哪一个部分，0标识男，1标识女。
                                    用户选择之后，PUT方法，带参数part（0和1标识男女部分），
                                     返回：若为第一个唱歌者返回musicinfo表 ，若合唱返回partmusicsong表信息，resule中包含participant_part信息：
                                        participant_part：为空则表示这首歌没有人唱过，则第一个唱，若不为空则是PART表部分的PK
                                    PUT：当歌曲为男女对唱时候，需要用户选择那一部分之后，带上part参数重新获取歌曲信息
                                          返回信息与get非男女对唱歌曲一样的信息
        
                                    POST  URL参数PK：音乐信息ID  所需参数：title：标题（str），socre:得分（int），part:合唱歌曲的哪个部分(若A部分0，B部分1，即为GET到的PART数据），
                                      is_enable:是否公开（bool，True或者False）,vedio:录制的视频MP4文件
                                      
music/sing_join/(?P<pk>[0-9]+)/(?P<part>[0-1])/                      #直接选择加入的视频   如：播放某个视频，直接选择左边或者右边点击加入                
music/report_song/<pk>/      #举报歌曲POST（参数，type：举报类型:(0 .Music Quality   1.Lyric Quality  2.Partner Complaint）)

```


