#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: views.py
@time: 2017/6/19 下午12:47
@SOFTWARE:PyCharm
"""
from django.contrib.auth.decorators import login_required

from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponse
from khufu import settings
import os
from time import strftime, localtime
import xlrd,xlwt,StringIO
import time
from dao.models.music import Singer, MusicProfiel


def vote(request):
    user = request.user
    if user.is_authenticated() and user.has_perm('app_auth.view_operate_list'):
        return True
    else:
        return False


@login_required
def upsinger_file(request):
    """
    上传歌手信息
    :param request: 
    :return: 
    """
    if vote(request):

        if request.method == 'POST':
            try:
                xlsfiles = request.FILES.get('file', '')
                fn = time.strftime('%Y%m%d%H%M%S')
                filename = fn + xlsfiles.name
                fname = os.path.join(settings.MEDIA_ROOT, 'upfile/singer/%s' % strftime('%Y/%m/%d', localtime()),
                                     filename)
                if os.path.exists(fname):
                    os.remove(fname)
                dirs = os.path.dirname(fname)
                if not os.path.exists(dirs):
                    os.makedirs(dirs)

                if os.path.isfile(fname):
                    os.remove(fname)
                content = xlsfiles.read()
                fp = open(fname, 'wb')
                fp.write(content)
                fp.close()

                book = xlrd.open_workbook(fname)
                sheet = book.sheet_by_index(0)
                singer_list = []
                for row_index in range(1, sheet.nrows):
                    record = sheet.row_values(row_index, 0)

                    try:
                        singer_dict = {}
                        # xxx=str(record[0])
                        uid = str(record[0]).strip()
                        singer_name = str(record[1]).strip()
                        monthly = int(record[2])
                        singer_dict['uid'] = uid
                        singer_dict['singer_name'] = singer_name
                        singer_dict['monthly'] = monthly
                        singer_list.append(singer_dict)

                    except Exception as e:

                        successinfo = "上传失败%s" % e

                        return render_to_response('include/upfile/upsingerfile.html', {
                            "title": '导入歌手信息', 'rest': successinfo}, context_instance=RequestContext(request))

                querysetlist = []
                for i in singer_list:
                    querysetlist.append(Singer(singer_name=i['singer_name'], uid=i['uid'], rank=i['monthly']))
                Singer.objects.bulk_create(querysetlist)

                successinfo = "上传成功"

                return render_to_response('include/upfile/upsingerfile.html', {
                    "title": '导入歌手信息',
                    'rest': successinfo, 'singer_list': singer_list}, context_instance=RequestContext(request))
            except Exception as e:
                successinfo = "上传失败%s" % e

                return render_to_response('include/upfile/upsingerfile.html', {
                    "title": '导入歌手信息', 'rest': successinfo}, context_instance=RequestContext(request))

        else:

            return render_to_response('include/upfile/upsingerfile.html', {
                "title": '导入供应商信息'}, context_instance=RequestContext(request))
    else:
        return HttpResponse('You are not have permission')


@login_required
def upmusic_file(request):
    """
    上传music信息
    :param request: 
    :return: 
    """
    if vote(request):

        if request.method == 'POST':
            try:
                xlsfiles = request.FILES.get('file', '')
                fn = time.strftime('%Y%m%d%H%M%S')
                filename = fn + xlsfiles.name
                fname = os.path.join(settings.MEDIA_ROOT, 'upfile/music/%s' % strftime('%Y/%m/%d', localtime()),
                                     filename)
                if os.path.exists(fname):
                    os.remove(fname)
                dirs = os.path.dirname(fname)
                if not os.path.exists(dirs):
                    os.makedirs(dirs)

                if os.path.isfile(fname):
                    os.remove(fname)
                content = xlsfiles.read()
                fp = open(fname, 'wb')
                fp.write(content)
                fp.close()

                book = xlrd.open_workbook(fname)
                sheet = book.sheet_by_index(0)
                obj_list = []
                for row_index in range(1, sheet.nrows):
                    record = sheet.row_values(row_index, 0)

                    try:
                        obj_dict = {}
                        uid = int(record[0])

                        singer_list = str(record[1]).split("/")

                        music_name = str(record[2]).strip()
                        rank = int(record[3])
                        original_name=str(record[4]).strip()
                        if original_name:
                            original = "https://s3-ap-southeast-1.amazonaws.com/duetin-original/" + str(record[4])
                        else:
                            original=''
                        accompany_name=str(record[5]).strip()
                        if accompany_name:
                            accompany = "https://s3-ap-southeast-1.amazonaws.com/duetin-accompany/" + str(record[5])
                        else:
                            accompany=''
                        lyc_name=str(record[6]).strip()
                        if lyc_name:
                            lyc = "https://s3-ap-southeast-1.amazonaws.com/duetin-lyrics/" + str(record[6])
                        else:
                            lyc=''
                        music_image = str(record[7]).strip()
                        if music_image:
                            image = "https://s3-ap-southeast-1.amazonaws.com/duetin-music-image/" + str(record[7])
                        else:
                            image = ""
                        # kgame = "http://ortujz8x2.bkt.gdipper.com/kgame/kg/" + str(record[7])
                        is_online_str=str(record[8]).strip()
                        if is_online_str=='YES':
                            is_online=True
                        else:
                            is_online=False
                        is_loved_str=str(record[9]).strip()
                        if is_loved_str=='YES':
                            is_loved=True
                        else:
                            is_loved=False

                        segments = str(record[10]).strip()
                        if segments:
                            segments_url = "https://s3-ap-southeast-1.amazonaws.com/duetin-segments/" + str(record[6])
                        else:
                            segments_url = ''
                        default_dir = {"music_name": music_name, "uid": uid,
                                       "Original_file": original,
                                       "bucket_original_key": original_name,
                                       "accompany": accompany,
                                       "bucket_accompany_key": accompany_name,
                                       "lyrics": lyc, "bucket_lyrics_key": lyc_name, "rank": rank,
                                       "image": image, "is_online": is_online,"bucket_image_key":music_image,
                                       "is_loved": is_loved,"segments_key_name":segments,"segments":segments_url}
                        music = MusicProfiel.objects.update_or_create(uid=uid, defaults=default_dir, )
                        music_l = list(music)
                        music_obj = music_l[0]
                        for singer in singer_list:
                            singer_obj = Singer.objects.get(uid=singer)
                            music_obj.singer.add(singer_obj)

                            # obj_dict['uid'] = uid
                            # obj_dict['music_name'] = music_name
                            # obj_dict['rank'] = rank
                            # obj_dict['original'] = "http://ortujz8x2.bkt.gdipper.com/original/mp3/"+original
                            # obj_dict['lyc'] = "http://ortujz8x2.bkt.gdipper.com/lyrics/lyc/"+lyc
                            # obj_dict['accompany'] = "http://ortujz8x2.bkt.gdipper.com/accompany/mp3/"+accompany
                            # obj_dict['kgame'] = "http://ortujz8x2.bkt.gdipper.com/kgame/kg/"+kgame
                            # obj_list.append(obj_dict)

                    except Exception as e:

                        successinfo = "上传失败%s,uid:%s" % (e, uid)

                        return render_to_response('include/upfile/upmusicfile.html', {
                            "title": '导入信息', 'rest': successinfo}, context_instance=RequestContext(request))

                querysetlist = []
                # for i in obj_list:
                #
                #     querysetlist.append(MusicProfiel(music_name=i['music_name'], uid=i['uid'],
                #                                      Original_file=i['original'], accompany=i['accompany'],
                #                                      k_game=i['kgame'], lyrics=i['lyc'], rank=i['rank']))
                #     querysetlist.append(MusicProfiel.singer.add(singer_obj))
                # MusicProfiel.objects.bulk_create(querysetlist)

                successinfo = "上传成功"

                return render_to_response('include/upfile/upmusicfile.html', {
                    "title": '导入信息',
                    'rest': successinfo, 'obj_list': obj_list}, context_instance=RequestContext(request))
            except Exception as e:
                successinfo = "上传失败%s:读取文件失败" % e

                return render_to_response('include/upfile/upmusicfile.html', {
                    "title": '导入信息', 'rest': successinfo}, context_instance=RequestContext(request))

        else:

            return render_to_response('include/upfile/upmusicfile.html', {
                "title": '导入信息'}, context_instance=RequestContext(request))
    else:
        return HttpResponse('You are not have permission')


@login_required
def upmusictime_file(request):
    """
    上传music信息
    :param request: 
    :return: 
    """
    if vote(request):

        if request.method == 'POST':
            try:
                xlsfiles = request.FILES.get('file', '')
                fn = time.strftime('%Y%m%d%H%M%S')
                filename = fn + xlsfiles.name
                fname = os.path.join(settings.MEDIA_ROOT, 'upfile/musictime/%s' % strftime('%Y/%m/%d', localtime()),
                                     filename)
                if os.path.exists(fname):
                    os.remove(fname)
                dirs = os.path.dirname(fname)
                if not os.path.exists(dirs):
                    os.makedirs(dirs)

                if os.path.isfile(fname):
                    os.remove(fname)
                content = xlsfiles.read()
                fp = open(fname, 'wb')
                fp.write(content)
                fp.close()

                book = xlrd.open_workbook(fname)
                sheet = book.sheet_by_index(0)
                obj_list = []
                for row_index in range(1, sheet.nrows):
                    record = sheet.row_values(row_index, 0)

                    try:
                        uid = int(record[0])

                        music_time_a = int(record[1])

                        music_time_b = int(record[2])



                        default_dir = {"time_a":music_time_a,"time_b":music_time_b}
                        music = MusicProfiel.objects.update_or_create(uid=uid, defaults=default_dir, )

                    except Exception as e:

                        successinfo = "上传失败%s,uid:%s" % (e, uid)

                        return render_to_response('include/upfile/upmusictimefile.html', {
                            "title": '导入信息', 'rest': successinfo}, context_instance=RequestContext(request))


                successinfo = "上传成功"

                return render_to_response('include/upfile/upmusictimefile.html', {
                    "title": '导入信息',
                    'rest': successinfo, 'obj_list': obj_list}, context_instance=RequestContext(request))
            except Exception as e:
                successinfo = "上传失败%s:读取文件失败" % e

                return render_to_response('include/upfile/upmusictimefile.html', {
                    "title": '导入信息', 'rest': successinfo}, context_instance=RequestContext(request))

        else:

            return render_to_response('include/upfile/upmusictimefile.html', {
                "title": '导入信息'}, context_instance=RequestContext(request))
    else:
        return HttpResponse('You are not have permission')


@login_required
def conversion_toid(request):
    style_red = xlwt.easyxf(" pattern: pattern solid,fore-colour 0x0A;")
    if request.method == 'POST':
        try:
            xlsfiles = request.FILES.get('file', '')
            fn = time.strftime('%Y%m%d%H%M%S')
            filename = fn + xlsfiles.name
            fname = os.path.join(settings.MEDIA_ROOT, 'upfile/music_toid/%s' % strftime('%Y/%m/%d', localtime()),
                                 filename)
            if os.path.exists(fname):
                os.remove(fname)
            dirs = os.path.dirname(fname)
            if not os.path.exists(dirs):
                os.makedirs(dirs)

            if os.path.isfile(fname):
                os.remove(fname)
            content = xlsfiles.read()
            fp = open(fname, 'wb')
            fp.write(content)
            fp.close()

            book = xlrd.open_workbook(fname)
            sheet = book.sheet_by_index(0)
            singer_all = Singer.objects.all()
            list_list = []
            for row_index in range(1, sheet.nrows):
                obj_list = []

                record = sheet.row_values(row_index, 0)

                try:
                    obj_dict = {}

                    # singer_list = str(record[1]).split("/")
                    music_name = str(record[0]).strip()
                    singer_list = str(record[1]).split("/")
                    # singer_name=singer_all.filter(singer_name=)
                    out_id_list = []

                    for s in singer_list:

                        singer_obj = singer_all.filter(singer_name=s)
                        if singer_obj.count() > 1:
                            out_id = "重名"
                        elif singer_obj.count() == 1:
                            out_id = Singer.objects.get(singer_name=s).uid
                        else:
                            out_id = "无此歌手"
                        # out_id_list.append(s)
                        # singer_all_str=singer_all_str+"/"+out_id
                        out_id_list.append(str(out_id))
                    a = '/'.join(out_id_list)
                    obj_list.append(music_name)
                    obj_list.append(a)
                    list_list.append(obj_list)
                    # music = Music.objects.update_or_create(music_name=music_name,
                    #                                        music_singer=original)
                    # music_l = list(music)
                    # music_obj = music_l[0]
                    # for singer in singer_list:
                    #     singer_obj = Singer.objects.get(uid=singer)
                    #     music_obj.singer.add(singer_obj)
                except Exception as e:

                    successinfo = "上传失败%s" % e

                    # return render_to_response('upmusicfile.html', context_instance=RequestContext(request))
                    return HttpResponse(successinfo)

            ws = xlwt.Workbook(encoding='utf-8')

            sheet = ws.add_sheet(u'歌手id对应', cell_overwrite_ok=True)
            first_col = sheet.col(0)  # xlwt中是行和列都是从0开始计算的
            sec_col = sheet.col(1)

            first_col.width = 256 * 20
            sec_col.width = 256 * 20

            sheet.write(0, 0, u"歌曲名")
            sheet.write(0, 1, u"歌手id")

            # 写入数据
            excel_row = 1
            for obj in list_list:

                musicname = obj[0]
                singer_id_str = obj[1]

                if "重名" in singer_id_str or "无此歌手" in singer_id_str:
                    # singer_id_str=id+"/"

                    sheet.write(excel_row, 0, musicname)
                    sheet.write(excel_row, 1, singer_id_str, style_red)
                else:
                    sheet.write(excel_row, 0, musicname)
                    sheet.write(excel_row, 1, singer_id_str)

                excel_row += 1
            fname = 'music_toid.xls'
            output = StringIO.StringIO()
            ws.save(output)
            output.seek(0)
            response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=%s' % fname
            response.write(output.getvalue())
            return response

        except Exception as e:
            successinfo = "失败%s:读取文件失败" % e

            return render_to_response('include/upfile/conversion.html', context_instance=RequestContext(request))

    else:

        return render_to_response('include/upfile/conversion.html', context_instance=RequestContext(request))


def file_down(request):
    from django.http import HttpResponseRedirect
    return HttpResponseRedirect("https://s3-ap-southeast-1.amazonaws.com/duetin/duetin-android.apk")
