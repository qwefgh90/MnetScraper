# -*- encoding: utf-8 -*-
__author__ = 'changwoncheo'
#select * from rating where rmusic_prerating != 0
import MySQLdb as mdb
import sys
import csv
import json
import sys
def getAllRating():
    try:
        con = mdb.connect('210.118.74.206','root','sns','SSong',charset='utf8');
        cur = con.cursor()
        cur.execute('select ruidx,rmusic_rating,rmusic_prerating from rating where ruidx > 9002 order by ridx');
        musicIdxRows = cur.fetchall()
        with open('ratingAll.csv','w') as fileobj:
            csvWriter = csv.writer(fileobj,delimiter=',')
            csvWriter.writerows(musicIdxRows)
    except Exception,e:
        print e

def getUserRating():
    try:
        for uidx in [9053,9081,9039,9080]:
            musicIdx = []
            con = mdb.connect('210.118.74.206', 'root', 'sns', 'SSong',charset='utf8')
            cur = con.cursor()
            cur.execute("select ruidx, rmusic_rating, rmusic_prerating from rating where ruidx = "+str(uidx)+' order by ridx');
            musixIdxRows = cur.fetchall()
           # print musixIdxRows
            with open('rating'+ str(uidx) +'.csv','w') as filept:
                csvWriter = csv.writer(filept,delimiter=',')
                csvWriter.writerows(musixIdxRows)
                #9053 - 68 , 9081 - 68 , 9039 - 52 , 9080 - 51
    except Exception, e:
        print e
if __name__ =="__main__":
    #makeUserIndex();
    #getUserRating();
    getAllRating();
    sys.exit();
    try:
        musicIdx = []
        con = mdb.connect('210.118.74.206', 'root', 'sns', 'SSong',charset='utf8')
        cur = con.cursor()
        cur.execute("select ruidx,rmusic_rating,rmusic_prerating from rating where rmusic_prerating != 0");
        musixIdxRows = cur.fetchall()
       # print musixIdxRows
        with open('rating2.csv','w') as filept:
            csvWriter = csv.writer(filept,delimiter=',')
            csvWriter.writerows(musixIdxRows)
    except:
        pass
