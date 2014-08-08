__author__ = 'changwoncheo'
# -*- coding: utf-8 -*-
#음악 리스트
#http://www.melon.com/genre/song_listPaging.htm?startIndex=51&pageSize=200&classicMenuId=DP0100&subMenuId=DP0102&orderBy=ORDER_ISSUE_DATE
#pageSize를 이용해 자유롭게 가져올 수 있다.
#앨범 사진
#http://www.melon.com/album/detail.htm?albumId=2264797
from setting import *
import requests as req
from bs4 import BeautifulSoup as bs

def makeMusicElement(tr_list):
    music_set = [];
    for tr in tr_list:
        t_left_list = tr.find_all(class_='t_left')
        songname = t_left_list[0].find(class_='fc_gray').get_text()#곡명
        artist = t_left_list[1].find(id='artistName').span.get_text()#아티스트
        album = t_left_list[2].find(class_='ellipsis').get_text()#앨범
        albumidx_str = t_left_list[2].find(class_='ellipsis').a.attrs['href']#앨범 인덱스+자바스크립트
        albumidx = int(reobj_album.findall(albumidx_str)[0]) #앨범 인덱스
        albumimg_link = getImage(albumidx)#이미지 링크
        albumimg_name = reobj_filename.findall(albumimg_link)[0]#이미지 이름
        downloadSaveImage(albumimg_link,albumimg_name); #이미지 링크와 이미지 이름

        songname = tapNewlineStrip(songname)
        artist = tapNewlineStrip(artist)
        album = tapNewlineStrip(album)
        music_set.append({'songname':songname,'artist':artist,'album':album,'album_img':albumimg_name})
    return music_set;

def getImage(albumidx):
    resp = req.request('get','http://www.melon.com/album/detail.htm?albumId='+str(albumidx))
    soup = bs(resp.content,from_encoding="utf-8")
    img_link = soup.find(id='albumImgArea').img.attrs['src']
    return img_link

def downloadSaveImage(url,filename):
    try:
        print filename +' ',
        resp = req.request('get',url)
        resp.content
        with open('album/'+filename,'wb') as obj:    #사진 저장
            obj.write(resp.content)
    except Exception, e:
        print '이미지 다운로드 저장 실패\n'+str(e)

def tapNewlineStrip(str):
    return str.encode('utf-8').replace('\n','').replace('\t','')

def writeJson(fileName,dict):
    import json
    with open(fileName, 'w') as outfile:
        json.dump(dict, outfile, ensure_ascii = False, encoding = 'utf-8')

if __name__ == '__main__':
    for i in xrange(102,111):
        resp = req.request('get','http://www.melon.com/genre/song_listPaging.htm?startIndex=1&pageSize=150&classicMenuId=DP0100'+'&subMenuId=DP0'+str(i)+'&orderBy=ORDER_ISSUE_DATE')
        soup = bs(resp.content,from_encoding="utf-8")   #meta charset 이 없을 경우 직접 인코딩을 알려준다.
        #1)find tbody
        tbody = soup.tbody
        #2)find_all (tr) - (music)
        tr_list = tbody.find_all('tr')
        music_set = makeMusicElement(tr_list);
        print('추출 개수 : ' + str(len(music_set))+'개')
        writeJson(category[i],music_set);
        print category[i]

