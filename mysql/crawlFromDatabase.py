__author__ = 'changwoncheo'

# -*- encoding: utf-8 -*-
import MySQLdb as mdb
import sys
import csv
import json
if __name__ =="__main__":
    #makeUserIndex();
    try:
        crawlDataFolder = 'crawlpage_modify'   #crawlpage_modify
        musicIdx = []
        con = mdb.connect('210.118.74.206', 'root', 'sns', 'SSong',charset='utf8')
        cur = con.cursor()
        cur.execute("SELECT mIdx from music");
        musixIdxRows = cur.fetchall()
        musicIdxList = list(([row[0]] for row in musixIdxRows))
        cur.execute("SELECT uIdx from user");
        rows = cur.fetchall()
        uIdxList = list((row[0] for row in rows))
        yesCount = 0;
        noCount = 0;
        for userIdx in uIdxList :
            cur.execute("SELECT rmIdx, rmusic_rating from rating where ruIdx = "+str(userIdx));
            indexRatinginRatingRows = cur.fetchall()
            indexRatinginRatingList = list(indexRatinginRatingRows)
            musicIdxinRatingList = list((musicIdxinRating[0] for musicIdxinRating in indexRatinginRatingList))
            for mIdx in musicIdxList:
                for musicIdxIndex,musicIdxinRating in enumerate(musicIdxinRatingList):
                    # print mIdx,musicIdxIndex, musicIdxinRating
                    #print musicIdxinRating
                    if(mIdx[0] == musicIdxinRating): #
                        mIdx.append(indexRatinginRatingList[musicIdxIndex][1])
                        yesCount+=1
                        break
                else :
                    mIdx.append(0)
                    noCount+=1
        with open('resultForR.csv','w') as resultObj:
            csvWriter = csv.writer(resultObj,delimiter=',')
            username = list (('user'+str(uIdx) for uIdx in uIdxList))
            username.insert(0,'USER')
            csvWriter.writerow(username)
            csvWriter.writerows(musicIdxList)
        #print musicIdxList[0:3];
    except mdb.Error, e:

        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:

        if con:
            con.close()