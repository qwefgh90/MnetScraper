__author__ = 'changwoncheo'
# -*- encoding: utf-8 -*-
from mnet_setting import *
from setting import *
from setting import *
import requests as req
from bs4 import BeautifulSoup as bs

mnetHostUrl= 'http://mnet.interest.me'

#http://mnet.interest.me/playlist/playlist_list.asp?part=kpop&srt=2&pNum=1
#한 페이지당 50명의 DJ를 포함
def getMusicFromOneDJ(url): #DJ에서 음악 리스트 반환 #http://mnet.interest.me/playlist/album/2811
    listOfMusicAndAlbum = []  #음악 리스트
    resp = req.request('get',url)
    song_page = bs(resp.content)
    userInfo = song_page.find(class_='name').get_text();
    userInfo = tapNewlineStrip(userInfo).split('|')
    #print userInfo
    userName = userInfo[0]
    userGender = userInfo[1]
    records = song_page.find(class_='MMLTable jQMMLTable').table.tbody.find_all('tr')
    for record in records:  #음악 태그 리스트 (1개~100개....)
        try:
            #Song
            songAnchorTag = record.find(class_='MMLITitleSong_Box').find_all('a')[1]
            songName = songAnchorTag.get_text()
            songIndex = int(reobj_album.findall(songAnchorTag.attrs['href'])[0])    #음악 인덱스
            artist = record.find(class_='MMLIArtist_Box').find_all('a')[0].get_text()
            #Album
            albumAnchorTag = record.find(class_='MMLIAlbum_Box').find_all('a')[0]   #anchor 태그
            album_link = mnetHostUrl + albumAnchorTag.attrs['href'].strip() #앨범 링크페이지
            album_name = albumAnchorTag.get_text()  #앨범이름
            album_index = int(reobjAlbumIndex.findall(album_link)[0]) #mnet 기준 인덱스
            imgSrc = getAlbumImageWithMNET(album_link)
            downloadSaveImageWithMNET(imgSrc,reobj_filename.findall(imgSrc)[0])
            musicItem = {'music':{'songIndex':songIndex,'artist':artist,'songName':songName,'albumIndex':album_index}
                ,'album':{'albumIndex':album_index,'albumName':album_name,'albumLink':album_link}}
            listOfMusicAndAlbum.append(musicItem)
        except Exception,e:
            logger.warning('[곡 정보가 존재하지 않는 경우...] \n'+str(e)),
    return {'name':userName,'gender':userGender,'useralbum':listOfMusicAndAlbum}
#1000명의 DJ를 뽑아오기 위해 20개의 페이지를 탐색
def getMusicFromDJWithMnet():
    dj_result_list = []
    for page in xrange(1,21,1): #페이지 탐색
        url = 'http://mnet.interest.me/playlist/playlist_list.asp?part=kpop&srt=2&pNum='+str(page)
        logger.debug('[DJLISTPAGE] '+url)
        resp = req.request('get',url)
        dj_page = bs(resp.content,from_encoding='utf-8')
        title_generator = (i.find(class_='title') for i in dj_page.find_all(class_='album_info'))
        for item in title_generator:    #DJ 탐색
            djURL = mnetHostUrl+item.a.attrs['href'];
            logger.debug('DJ : ' + djURL)
            DJInfo = getMusicFromOneDJ(djURL) #URL
            dj_result_list.append(DJInfo)
        logger.debug('[Write] mnetDJpage'+str(page)+'.JSON')
        writeJson('crawlpage/mnetDJpage'+str(page)+'.JSON',dj_result_list)
        dj_result_list=[]
    return dj_result_list


def getAlbumImageWithMNET(url):
    resp = req.request('get',url)
    album_page = bs(resp.content,from_encoding='utf-8')
    imgSrc = album_page.dt.img.attrs['src']
    return imgSrc

def downloadSaveImageWithMNET(url,filename):
    try:
        #logger.debug(url + ' : ' + filename)
        resp = req.request('get',url)
        with open('album/'+filename,'wb') as obj:    #사진 저장
            obj.write(resp.content)
    except Exception, e:
        logger.warning('이미지 다운로드 저장 실패\n'+str(e))
        return False
    return True

