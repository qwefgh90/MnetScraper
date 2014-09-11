__author__ = 'changwoncheo'
#-*- encoding: utf-8 -*-
import csv
import math
with open("result_cosine.csv",'rb') as f:
    reader = csv.reader(f, delimiter= ',')
    userDict = {}
    for row in reader:
        user=row[0]  #user
        music=row[1]  #music
        score=row[2]  #score
        if(not user in userDict.iterkeys()):
            userDict[user] = []
        else:
            userDict[user].append([music,score])
    resultsMatrix = []
    for uidx in userDict.keys():
        simresult = {}
        fc = 0
        fa = 0;

        for musicInformation_fc in userDict[uidx]:
            fc += pow(float(musicInformation_fc[1]),2)   #fc 를 구함

        for uidx2 in userDict.keys():
            fb = 0
            for musicInformation_fb in userDict[uidx2]:
                fb += pow(float(musicInformation_fb[1]),2)  #fb 를 구하기 위해

            for musicInformation1 in userDict[uidx]:        #다음 음악
                    for musicInformation2 in userDict[uidx2]:   #다음 음악
                        if musicInformation1[0]== musicInformation2[0]:
                            fa += float(musicInformation1[1])*float(musicInformation2[1])    #vector 내적
            cosinesim = 0
            if(fb==0):
                print uidx2+ ' : fb= '+str(fb)
            if(fc==0):
                print uidx+ ' : fc= '+str(fc)
            if(fb!=0 and fc!=0):
                cosinesim = fa/(math.sqrt(fb)*math.sqrt(fc))  #cosinesim
            fa = 0
            simresult[(str(uidx),str(uidx2))] = str(cosinesim)
            import operator
        sorted_x = sorted(simresult.iteritems(), key=operator.itemgetter(1),reverse=True)
      #  print str(uidx)+':'+str(uidx2)+':'+str(sorted_x)
        resultsMatrix.append(sorted_x)
    print resultsMatrix