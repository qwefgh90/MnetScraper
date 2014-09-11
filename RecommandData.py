__author__ = 'changwoncheo'
#-*- encoding: utf-8 -*-
import csv
import json
from collections import Counter
def csvMaker():
    '''çsv 파일을 생성한다.'''
    csvName = 'result.csv'          #result1.csv
    crawlDataFolder = 'crawlpage_modify'   #crawlpage_modify
    with open(csvName,'w') as csvobj:
        musicCount = 0
        index = 0
        rating = 5.0
        csvWriter = csv.writer(csvobj,delimiter=',')
        for pageNum in xrange(1,21,1):
            print 'current parse page : '+str(pageNum)
            with open(crawlDataFolder+'/mnetDJpage'+str(pageNum)+'.JSON','r') as pageobj:
                logJson = json.load(pageobj,'utf-8')
                for record in logJson:
                    userIdx = index #임의의 인덱스

                    for music in record['userAlbum']:#음악별
                        #print
                        genreStr = ''
                        for genre in music['album']['genre']:
                            genreStr = genreStr + ' and ' +genre.encode('utf-8')
                        csvWriter.writerow([index,music['music']['songIndex'],rating,genreStr])
                        musicCount += 1
                    index += 1
            if(pageNum%4 == 0):
               rating -= 0.5

        print 'total music count : '+str(musicCount)
def jsonGenreModifier():
        '''장르 중 'l'과 같이 분리되지 않은 장르를 분리하는 작업을 한 후 crawlpage_moidfy에 저장한다'''
        musicCount = 0
        index = 0
        rating = 5.0
        for pageNum in xrange(1,21,1):
            print 'current parse page : '+str(pageNum)
            with open('crawlpage/mnetDJpage'+str(pageNum)+'.JSON','r') as pageobj:
                with open('crawlpage_modify/mnetDJpage'+str(pageNum)+'.JSON','w') as writeobj:
                    logJson = json.load(pageobj,'utf-8')
                    for record in logJson:
                        userIdx = index #임의의 인덱스
                        for music in record['userAlbum']:#음악별
                            #print
                            genreList=[]
                            splitList=[]
                            for i in music['album']['genre']:
                                if 'l' in i:
                                    splitList = i.split('l')
                                    splitList = list((ele.strip() for ele in splitList))
                                    for genre in splitList :
                                        genreList.append(genre)
                                else :
                                    genreList.append(i.strip())
                            music['album']['genre'] = genreList
                        index += 1
                    jsonString = json.dumps(logJson,ensure_ascii=False).encode('utf-8')
                    writeobj.write(jsonString)
            if(pageNum%4 == 0):
               rating -= 0.5
        print 'total music count : '+str(musicCount)
def getPercentGenre(resultFileObj):
    crawlDataFolder ='crawlpage_modify'
    genreList=[]
    musicCount=0
    index =0
    for pageNum in xrange(1,21,1):
            #print 'current parse page : '+str(pageNum)
            with open(crawlDataFolder+'/mnetDJpage'+str(pageNum)+'.JSON','r') as pageobj:
                logJson = json.load(pageobj,'utf-8')
                for record in logJson:
                    userIdx = index #임의의 인덱스
                    for music in record['userAlbum']:#음악별
                        for genre in music['album']['genre']:
                            genreList.append(genre.encode('utf-8'))
                        #print
                        musicCount += 1
                    index += 1
    countResult = Counter(genreList)
    print '[genre database]'
    resultFileObj.write('[genre database]\r\n')
    for name in countResult.keys():
        #print name
        genreListLength = len(genreList)#total genre count
        countResult[name] = round((countResult[name]/(genreListLength*1.0))*100,4)  #calculate average
        print name+':'+str(countResult[name])+'%'
        resultFileObj.write(name+':'+str(countResult[name])+'%\r\n')

def getPercentDate(resultFileObj):
    crawlDataFolder ='crawlpage_modify'
    dateList=[]
    musicCount=0
    index =0
    for pageNum in xrange(1,21,1):
            #print 'current parse page : '+str(pageNum)
            with open(crawlDataFolder+'/mnetDJpage'+str(pageNum)+'.JSON','r') as pageobj:
                logJson = json.load(pageobj,'utf-8')
                for record in logJson:
                    userIdx = index #임의의 인덱스
                    for music in record['userAlbum']:#음악별
                        date = music['album']['album_date']
                        date = date.encode('utf-8').split('-')[0];
                        date = str((int(date)/10)*10)
                        dateList.append(date)
                        #print
                        musicCount += 1
                    index += 1
    countResult = Counter(dateList)
    print '[date database]'
    resultFileObj.write('[date database]\r\n')
    for name in countResult.keys():
        #print name
        dateListLength = len(dateList)#total genre count
        countResult[name] = round((countResult[name]/(dateListLength*1.0))*100,4)  #calculate average
        print name+':'+str(countResult[name])+'%'
        resultFileObj.write(name+':'+str(countResult[name])+'%\r\n')
def getMusicCount(resultFileObj):
    crawlDataFolder ='crawlpage_modify'
    musicList=[]
    musicCount=0
    index =0
    for pageNum in xrange(1,21,1):
            #print 'current parse page : '+str(pageNum)
            with open(crawlDataFolder+'/mnetDJpage'+str(pageNum)+'.JSON','r') as pageobj:
                logJson = json.load(pageobj,'utf-8')
                for record in logJson:
                    userIdx = index #임의의 인덱스
                    for music in record['userAlbum']:#음악별
                        musicList.append(music['music']['songIndex'])
                        #print
                        musicCount += 1
                    index += 1
    #print name
    musicCount = len(set(musicList))
    logCount = len(musicList)
    print '[log database]'
    resultFileObj.write('[log database]\r\n')

    print 'musicCount : ' +str(musicCount)
    resultFileObj.write('musicCount : ' +str(musicCount)+'\r\n')
    print 'logCount : ' +str(logCount)
    resultFileObj.write('logCount : ' +str(logCount)+'\r\n')
    print 'music/log : '+str((musicCount/(logCount*1.0))*100)+'%'
    resultFileObj.write('music/log : '+str((musicCount/(logCount*1.0))*100)+'%\r\n')
if __name__ =='__main__':
    #jsonGenreModifier()
    csvMaker()
    with open('db_information.txt','w') as dbobj:
    #    getPercentGenre(dbobj)
    #    getPercentDate(dbobj)
    #    getMusicCount(dbobj)
        pass