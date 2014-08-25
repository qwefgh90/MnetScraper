__author__ = 'changwoncheo'
# -*- encoding: utf-8 -*-
from exception_setting import *
from mnet_setting import *
from setting import *
from setting import *
import requests as req
from bs4 import BeautifulSoup as bs

mnetHostUrl= 'http://mnet.interest.me'

#http://mnet.interest.me/playlist/playlist_list.asp?part=kpop&srt=2&pNum=1
#한 페이지당 50명의 DJ를 포함
def getMusicFromOneDJ(url): #DJ에서 음악 리스트 반환 #http://mnet.interest.me/playlist/album/2512, http://mnet.interest.me/playlist/album/3072
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
            if 'disabled' in songAnchorTag['class'] :#존재 하지 않을 경우
                raise Exception('곡 정보가 존재하지 않습니다.')
            songName = songAnchorTag.get_text()
            songIndex = int(reobj_album.findall(songAnchorTag.attrs['href'])[0])    #음악 인덱스
            artist = record.find(class_='MMLIArtist_Box').find_all('a')[0].get_text()
            #Album
            albumAnchorTag = record.find(class_='MMLIAlbum_Box').find_all('a')[0]   #anchor 태그
            album_link = mnetHostUrl + albumAnchorTag.attrs['href'].strip() #앨범 링크페이지
            album_name = albumAnchorTag.get_text()  #앨범이름
            album_index = int(reobjAlbumIndex.findall(album_link)[0]) #mnet 기준 인덱스
            genre,album_date,imgSrc = getAlbumInfoWithMNET(album_link)
            if(downloadSaveImageWithMNET(imgSrc,reobj_filename.findall(imgSrc)[0])==False):
                #이미지가 존재하지 않을 경우, 추후 이미지 다운로드
                pass

            musicItem = {'music':{'songIndex':songIndex,'artist':artist.encode('utf-8'),'songName':songName.encode('utf-8')
                ,'albumIndex':album_index}
                ,'album':{'albumIndex':album_index,'albumName':album_name.encode('utf-8'),'albumLink':album_link.encode('utf-8')
                ,'genre':list((gen.encode('utf-8').strip() for gen in genre)),'album_date':album_date.encode('utf-8')}}
            listOfMusicAndAlbum.append(musicItem)
        except Exception,e:
            logger.warning(GetException()),
    return {'name':userName.encode('utf-8'),'gender':userGender.encode('utf-8'),'userAlbum':listOfMusicAndAlbum}
#1000명의 DJ를 뽑아오기 위해 20개의 페이지를 탐색
def getMusicFromDJWithMnet(startIdx,endIdx,step):
    dj_result_list = []
    for page in xrange(startIdx,endIdx,step): #페이지 탐색
        url = 'http://mnet.interest.me/playlist/playlist_list.asp?part=kpop&srt=2&pNum='+str(page)
        logger.debug('['+str(threading.current_thread())+'][DJLISTPAGE] '+url)
        resp = req.request('get',url)
        dj_page = bs(resp.content,from_encoding='utf-8')
        title_generator = (i.find(class_='title') for i in dj_page.find_all(class_='album_info'))
        for item in title_generator:    #DJ 탐색
            try:
                djURL = mnetHostUrl+item.a.attrs['href'];
                logger.debug('DJ : ' + djURL)
                DJInfo = getMusicFromOneDJ(djURL) #URL
                dj_result_list.append(DJInfo)
                logger.debug(str(DJInfo['name']) + ':'+str(DJInfo['gender'])+ ':' + str(DJInfo['userAlbum'][0]))
            except Exception,e :
                logger.warning(GetException()),
            print '['+str(page)+'] '+str(DJInfo)
            #writeJson('crawlpage/mnetDJpage'+str(page)+'.JSON',DJInfo)
        logger.debug('[Write] mnetDJpage'+str(page)+'.JSON')
        writeJson('crawlpage/mnetDJpage'+str(page)+'.JSON',dj_result_list)
        dj_result_list=[]
    return dj_result_list


def getAlbumInfoWithMNET(url):  #예외처리 안하고 있다가 무슨 에러인지도 모르고 죽는 경우가 많았음.
    resp = req.request('get',url)   #앨범 주소 http://mnet.interest.me/playlist/album/241305
    album_page = bs(resp.content,from_encoding='utf-8')
    album_info_tag = ''
    album_date = ''
    genre = ''
    imgSrc = ''
    try:
        album_info_tag = album_page.find(class_ ='a_info_cont')
        album_info_tag = album_info_tag.dd.find_all('p')
    except Exception,e :
        raise Exception(url+' 앨범 정보가 존자해지 않습니다.')
    try:
        genre = album_info_tag[3].find(class_='right').get_text()#장르
        genre = getGenre(genre)
    except Exception,e :
        raise Exception(url+' 장르 정보가 존재하지 않습니다.')
    try:
        album_date = album_info_tag[1].find_all('span')[1].get_text()#발매일
        album_date = getDateFormat(album_date)
    except Exception,e :
        raise Exception(url+' 앨범 날짜가 존재하지 않습니다.')
    try:
        imgSrc = album_page.find(class_='pic_art').img.attrs['src']
    except Exception,e :
        raise Exception(url+' 앨범 이미지가 존재하지 않습니다.')
    return (genre,album_date,imgSrc)
def getGenre(genre):
    genre = genre.strip()       #공백 처리
    genre = genre.split('>')[1]
    genre = genre.split(',')
    return genre
def getDateFormat(date):
    date = date.strip()     #공백 처리
    formatDate = ''
    date_list = date.split('.')
    for (idx,date_part) in enumerate(date_list):
        if( date_part == '00') :            #01일로 보정
            date_part = '01'
        formatDate = formatDate + date_part
        if (idx != len(date_list)-1):
            formatDate  = formatDate + '-'
        else:
            if(len(date_list) < 3): #월/일이 없을 경우
                for bonus in range(3-len(date_list)):  #add date
                    formatDate = formatDate + '-' + '01'
    return formatDate
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

