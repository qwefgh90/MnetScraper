#-*- encoding: utf-8 -*-
#MySQL-python을 설치하기 위해 mac용 mysql 패키지를 설치하고 http://friendlybit.com/tutorial/install-mysql-python-on-mac-os-x-leopard/
#http://gpiot.com/blog/mac-os-x-lion-the-perfect-setup-for-python-django/
#위 링크에 나온 export DYLD_LIBRARY_PATH=/usr/local/mysql/lib:$DYLD_LIBRARY_PATH
#를 선언한 후 setup.py를 실행하여 설치한다.
#!/usr/bin/python
# -*- coding: utf-8 -*-

#회원가입
#앨범등록
#음악등록
#래이팅 등록

import MySQLdb as mdb
import sys
import json
def makeUserIndex():
    uindex = 1;
    crawlDataFolder = '../crawlpage_modify'   #crawlpage_modify
    for pageNum in xrange(1,21,1):
            print 'current parse page : '+str(pageNum)
            with open(crawlDataFolder+'/mnetDJpage'+str(pageNum)+'.JSON','r') as pageobj:
                logJson = json.load(pageobj,'utf-8')
                for record in logJson:
                    record['uindex']=uindex
                    uindex += 1
                with open(crawlDataFolder+'/mnetDJpage'+str(pageNum)+'_uid.JSON','w') as writeobj:
                    jsonString = json.dumps(logJson,ensure_ascii=False).encode('utf-8')
                    writeobj.write(jsonString)



def registerUser(con):
    cur = con.cursor()
    crawlDataFolder = '../crawlpage_modify'   #crawlpage_modify
    for pageNum in xrange(1,21,1):
            print 'current parse page : '+str(pageNum)
            with open(crawlDataFolder+'/mnetDJpage'+str(pageNum)+'_uid.JSON','r') as pageobj:
                logJson = json.load(pageobj,'utf-8')
                for record in logJson:
                    genderVal = 0;
                    if( record['gender'].encode('utf-8') =='남'):
                        genderVal=1
                    else:
                        genderVal=0
                    name = record['name'].encode('utf-8');
                    #print name
                    import random
                    cur.execute("set names utf8")
                    query = '''insert into user(uid,unick,upasswd,ugender,uage) values (%s,%s,sha1(%s),%s,%s)'''
                    cur.execute(query,('user'+str(record['uindex']),
                                name, '0000', int(genderVal), int(10+random.random()*40)))
    con.commit()

def registerAlbum(con):
    cur = con.cursor()
    crawlDataFolder = '../crawlpage_modify'   #crawlpage_modify
    for pageNum in xrange(1,21,1):
            print 'current parse page : '+str(pageNum)
            with open(crawlDataFolder+'/mnetDJpage'+str(pageNum)+'_uid.JSON','r') as pageobj:
                logJson = json.load(pageobj,'utf-8')
                for record in logJson:
                    userAlbum = record['userAlbum']
                    for song in userAlbum:
                        album = song['album']
                        #print name
                        import random
                        cur.execute("set names utf8")
                        query = '''insert into album(aidx,aimg_path,atitle,adate,agenre,adate_year) values(%s,%s,%s,%s,%s,%s)'''
                        try:
                            date = album['album_date'].encode('utf-8').split('-')[0];
                            date = str((int(date)/10)*10)
                            cur.execute(query,(album['albumIndex'],str(album['albumIndex'])+'.jpg',
                                               album['albumName'],album['album_date'],
                                               album['genre'][0],##genre waring 장르는 리스트 형태이다.
                                               # #[0]번 인덱스를 장르로 저장한다. (이전에 공개한 장르 비율이 영향을 받음)
                                               date))
                        except Exception,e:
                            print e

    con.commit()

def registerMusic(con):
    cur = con.cursor()
    crawlDataFolder = '../crawlpage_modify'   #crawlpage_modify
    for pageNum in xrange(1,21,1):
            print 'current parse page : '+str(pageNum)
            with open(crawlDataFolder+'/mnetDJpage'+str(pageNum)+'_uid.JSON','r') as pageobj:
                logJson = json.load(pageobj,'utf-8')
                for record in logJson:
                    userAlbum = record['userAlbum']
                    for song in userAlbum:
                        album = song['album']
                        music = song['music']
                        #print name
                        import random
                        cur.execute("set names utf8")
                        query = '''insert into music(midx,maidx,mtitle,martist,mgenre,mdate_year) values(%s,%s,%s,%s,%s,%s)'''
                        try:
                            date = album['album_date'].encode('utf-8').split('-')[0];
                            date = str((int(date)/10)*10)
                            cur.execute(query,(music['songIndex'],music['albumIndex'],
                                               music['songName'],music['artist'],
                                               album['genre'][0],##genre waring 장르는 리스트 형태이다.
                                               # #[0]번 인덱스를 장르로 저장한다. (이전에 공개한 장르 비율이 영향을 받음)
                                               date))
                        except Exception,e:
                            print e
    con.commit()
def registerLog(con):
    uidx = 8003;
    rating = 5.0;
    cur = con.cursor()
    crawlDataFolder = '../crawlpage_modify'   #crawlpage_modify
    for pageNum in xrange(1,21,1):
            print 'current parse page : '+str(pageNum)
            with open(crawlDataFolder+'/mnetDJpage'+str(pageNum)+'_uid.JSON','r') as pageobj:
                logJson = json.load(pageobj,'utf-8')
                for record in logJson:
                    userAlbum = record['userAlbum']
                    for song in userAlbum:
                        album = song['album']
                        music = song['music']
                        #print name
                        import random
                        cur.execute("set names utf8")
                        query = '''insert into rating(ruidx,rmidx,rmusic_rating) values(%s,%s,%s)'''
                        try:
                            cur.execute(query,(uidx,music['songIndex'],rating))
                            pass
                        except Exception,e:
                            print e

                    uidx += 1
                    #print uidx, rating
            if(pageNum % 4 == 0):
                                rating -= 0.5
    con.commit()
if __name__ =="__main__":
    #makeUserIndex();
    try:
        con = mdb.connect('210.118.74.206', 'root', 'sns', 'SSong',charset='utf8')
        registerLog(con)
        #con.query("SELECT * from user")
        #esult = con.use_result()
        print result.fetch_row()

    except mdb.Error, e:

        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:

        if con:
            con.close()